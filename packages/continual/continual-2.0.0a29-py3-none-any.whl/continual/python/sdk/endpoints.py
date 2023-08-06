from __future__ import annotations
from typing import Iterator, List, Optional

from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.artifacts import ArtifactsManager
from continual.python.sdk.checks import ChecksManager
from continual.python.sdk.metadata import MetadataManager
from continual.python.sdk.metrics import MetricsManager


class EndpointManager(Manager):
    """Manages Endpoint resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/endpoints/{endpoint}"

    def create(
        self,
        id: Optional[str] = None,
        model_version: Optional[str] = None,
        uri: Optional[str] = None,
        state: Optional[str] = "ACTIVE",
        tags: Optional[dict[str, str]] = None,
        replace_if_exists: bool = False,
    ) -> Endpoint:
        """Create an Endpoint.

        Arguments:
            id: Endpoint name or id.
            model_version: Name of the model version to use on the endpoint
            uri: URI of the endpoint
            state: State of the endpoint
            tags: A dict of tags to add to this endpoint.
            replace_if_exists: If true, update the existing endpoint if it exists, else throw an error.

        Returns
            An Endpoint.
        """
        req = management_pb2.CreateEndpointRequest(
            parent=self.parent,
            endpoint=Endpoint(
                run=self.run_name,
                model_version=self.name(
                    model_version, self.parent, f"{self.parent}/versions/id"
                ),
                uri=uri,
                state=state,
                tags=tags,
            ).to_proto(),
            endpoint_id=id,
            replace_if_exists=replace_if_exists,
        )
        resp = self.client._management.CreateEndpoint(req)
        return Endpoint.from_proto(resp, client=self.client)

    def get(self, id: str) -> Endpoint:
        """Get an Endpoint.

        Arguments:
            id: Endpoint name or id.

        Returns
            An Endpoint.
        """
        req = management_pb2.GetEndpointRequest(name=self.name(id))
        resp = self.client._management.GetEndpoint(req)
        return Endpoint.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        latest: bool = True,
        order_by: Optional[str] = None,
        all_projects: bool = False,
    ) -> List[Endpoint]:
        """List Endpoints.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
            all_projects: Whether to include all instances of this resource from the project or just from the current parent.

        Returns:
            A list of Endpoints.
        """
        req = management_pb2.ListEndpointsRequest(
            parent=self.parent,
            latest=latest,
            order_by=order_by,
            page_size=page_size,
            all_projects=all_projects,
        )
        resp = self.client._management.ListEndpoints(req)
        return [Endpoint.from_proto(u, client=self.client) for u in resp.endpoints]

    def list_all(self) -> Iterator[Endpoint]:
        """List all Endpoints.

        Pages through all Endpoint using an iterator.

        Returns:
            A iterator of all Endpoint.
        """

        def next_page(next_page_token):
            req = management_pb2.ListEndpointsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListEndpoints(req)
            return (
                [Endpoint.from_proto(u, client=self.client) for u in resp.endpoints],
                resp.next_page_token,
            )

        return Pager(next_page)

    def update(self, endpoint: Endpoint, paths: List[str]) -> Endpoint:
        """Update an Endpoint.

        Arguments:
            endpoint: Endpoint object with updated fields.
            paths: List of fields to update.

        Returns
            An Endpoint.
        """
        req = management_pb2.UpdateEndpointRequest(
            endpoint=endpoint.to_proto(),
            update_paths=paths,
            run=self.run_name,
        )
        resp = self.client._management.UpdateEndpoint(req)
        return Endpoint.from_proto(resp, client=self.client)

    def delete(self, id: str):
        """Delete an Endpoint.

        Arguments:
            id: Endpoint name or id.
        """
        req = management_pb2.DeleteEndpointRequest(name=self.name(id))
        self.client._management.DeleteEndpoint(req)


class Endpoint(Resource, types.Endpoint):
    """Endpoint resource."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/endpoints/{endpoint}"

    _manager: EndpointManager
    """Endpoint manager"""

    _metrics: MetricsManager
    """Metrics Manager"""

    _artifacts: ArtifactsManager
    """Artifacts Manager"""

    _metadata: MetadataManager
    """Metadata Manager"""

    _checks: ChecksManager

    def _init(self):
        self._manager = EndpointManager(
            parent=self.parent, client=self.client, run_name=self.run
        )
        self._artifacts = ArtifactsManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._metadata = MetadataManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._metrics = MetricsManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._checks = ChecksManager(
            parent=self.name, client=self.client, run_name=self.run
        )

    @property
    def artifacts(self) -> ArtifactsManager:
        """Artifacts Manager."""
        return self._artifacts

    @property
    def metadata(self) -> MetadataManager:
        """Metadata Manager."""
        return self._metadata

    @property
    def metrics(self) -> MetricsManager:
        """Metrics Manager."""
        return self._metrics

    @property
    def checks(self) -> ChecksManager:
        """Checks manager."""
        return self._checks

    def update(self, paths: List[str]) -> Endpoint:
        """Update Endpoint.

        Arguments:
            paths: A list of paths to be updated.

        Returns:
            An updated Endpoint.

        Examples:
            >>> ...
        """
        return self._manager.update(paths=paths, endpoint=self)
