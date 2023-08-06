from __future__ import annotations
from typing import List, Optional
from continual.python.sdk.batchpredictions import (
    BatchPredictionManager,
)
from continual.python.sdk.checks import ChecksManager
from continual.python.sdk.data_profiles import DataProfilesManager
from continual.python.sdk.metrics import MetricsManager
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.artifacts import ArtifactsManager
from continual.python.sdk.metadata import MetadataManager
from continual.python.sdk.dataset_version_assignments import (
    DatasetVersionAssignmentManager,
)


class DatasetVersionManager(Manager):
    """Manages Dataset Version resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/datasets/{dataset}/versions/{version}"

    def create(
        self,
        id: Optional[str] = "",
        tags: Optional[dict[str, str]] = None,
        replace_if_exists: bool = False,
    ) -> DatasetVersion:
        """Create a dataset version for local development

        Arguments:
            id: An optional DatasetVersion id.
            tags: A dict of tags to add to the dataset version.
            replace_if_exists: If True, update the dataset version if it already exists.

        Returns
            A Dataset Version.

        Examples:
            >>> ... # Assume client, project, environment are defined
            >>> run = env.runs.create(description="My run")
            >>> dataset = run.datasets.get("my_dataset")
            >>> dataset_version = dataset.dataset_versions.create()
            <DatasetVersion object {'name': 'projects/test_proj_4/environments/test_env/datasets/mydataset/versions/ceg9f2i5lsrt9r5a8l8g',
            'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0', 'create_time': '2022-12-19T16:55:38.879936Z',
            'update_time': '2022-12-19T16:55:38.879936Z'}>
        """
        if tags and not all(
            [isinstance(k, str) and isinstance(v, str) for k, v in tags.items()]
        ):
            raise ValueError("Tags must be a dict of str: str")

        req = management_pb2.CreateDatasetVersionRequest(
            parent=self.parent,
            dataset_version=DatasetVersion(
                run=self.run_name, current_run=self.run_name, tags=tags
            ).to_proto(),
            dataset_version_id=id,
            replace_if_exists=replace_if_exists,
        )
        resp = self.client._management.CreateDatasetVersion(req)
        return DatasetVersion.from_proto(
            resp, client=self.client, current_run=self.run_name
        )

    def get(self, id: str) -> DatasetVersion:
        """Get dataset version.

        Arguments:
            id: Dataset name or id.

        Returns
            An Dataset Version.

        Examples:
            >>> ... # Assume client, project, environment are defined
            >>> run = env.runs.create("My run")
            >>> dataset = run.datasets.get("my_dataset")
            >>> dataset_version = dataset.dataset_versions.create()
            >>> dataset.dataset_versions.get(id=dataset_version.name) # Get dataset version by name
            <DatasetVersion object {'name': 'projects/test_proj_4/environments/test_env/datasets/mydataset/versions/ceg9f2i5lsrt9r5a8l8g',
            'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0', 'create_time': '2022-12-19T16:55:38.879936Z',
            'update_time': '2022-12-19T16:55:38.879936Z'}>
            >>> dataset.dataset_versions.get(id=dataset_version.id)   # Get dataset version by id
            <DatasetVersion object {'name': 'projects/test_proj_4/environments/test_env/datasets/mydataset/versions/ceg9f2i5lsrt9r5a8l8g',
            'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0', 'create_time': '2022-12-19T16:55:38.879936Z',
            'update_time': '2022-12-19T16:55:38.879936Z'}>
        """
        req = management_pb2.GetDatasetVersionRequest(name=self.name(id))
        resp = self.client._management.GetDatasetVersion(req)
        return DatasetVersion.from_proto(
            resp, client=self.client, current_run=self.run_name
        )

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: str = None,
        latest: bool = True,
    ) -> List[DatasetVersion]:
        """List dataset versions.

        Arguments:
            page_size: Number of items to return.

        Returns:
            A list of dataset versions.

        Examples:
            >>> ... # Assume client, project, environment are defined
            >>> run = env.runs.create("My run")
            >>> dataset = run.datasets.get("my_dataset")
            >>> dvs = [dataset.dataset_versions.create() for _ in range(3)]
            >>> first_dataset_version = dataset.dataset_versions.list(page_size=10)[0]               # Get first dataset version
            >>> latest_dataset_version = dataset.dataset_versions.list(page_size=10, latest=True)[0] # Get latest dataset version
        """
        req = management_pb2.ListDatasetVersionsRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            latest=latest,
        )
        resp = self.client._management.ListDatasetVersions(req)
        return [
            DatasetVersion.from_proto(x, client=self.client, current_run=self.run_name)
            for x in resp.dataset_versions
        ]

    def list_all(self) -> Pager[DatasetVersion]:
        """List all dataset versions.

        Pages through all dataset versions using an iterator.

        Returns:
            A iterator of all dataset versions.

        Examples:
            >>> ... # Assume client, project, environment are defined
            >>> run = env.runs.create("My run")
            >>> dataset = run.datasets.get("my_dataset")
            >>> dvs = [dataset.dataset_versions.create() for _ in range(3)]
            >>> len(list(dataset.dataset_versions.list_all())) # List all dataset versions
            3
        """

        def next_page(next_page_token):
            req = management_pb2.ListDatasetVersionsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListDatasetVersions(req)
            return (
                [
                    DatasetVersion.from_proto(
                        x, client=self.client, current_run=self.run_name
                    )
                    for x in resp.dataset_versions
                ],
                resp.next_page_token,
            )

        return Pager(next_page)

    def update(
        self,
        dataset_version: DatasetVersion,
        paths: List[str],
    ) -> DatasetVersion:
        """Update DatasetVersion.

        Arguments:
            paths: A list of paths to be updated.
            dataset_version: DatasetVersion object containing updated fields.

        Returns:
            An updated DatasetVersion.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
        """

        req = management_pb2.UpdateDatasetVersionRequest(
            dataset_version=dataset_version.to_proto(),
            update_paths=paths,
            run=self.run_name,
        )
        resp = self.client._management.UpdateDatasetVersion(req)
        return DatasetVersion.from_proto(
            resp, client=self.client, current_run=self.run_name
        )


class DatasetVersion(Resource, types.DatasetVersion):
    """Dataset version resource."""

    name_pattern: str = "projects/{project}/environments/{environment}/datasets/{dataset}/versions/{version}"
    _manager: DatasetVersionManager
    """Dataset version manager."""

    _checks: ChecksManager
    """Checks Manager"""

    _data_profiles: DataProfilesManager
    """Data Profiles Manager"""

    _assignments: DatasetVersionAssignmentManager
    """Dataset Version Assignment Manager"""

    _metrics: MetricsManager
    """Metrics Manager"""

    _artifacts: ArtifactsManager
    """Artifacts Manager"""

    _metadata: MetadataManager
    """Metadata Manager"""

    def _init(self):
        self._manager = DatasetVersionManager(
            parent=self.parent, client=self.client, run_name=self.run
        )
        self._artifacts = ArtifactsManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._metadata = MetadataManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._checks = ChecksManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._data_profiles = DataProfilesManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._batch_predictions = BatchPredictionManager(
            parent=self.parent, client=self.client, run_name=self.run
        )
        self._metrics = MetricsManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._assignments = DatasetVersionAssignmentManager(
            parent=self.name, client=self.client, run_name=self.current_run
        )

    @property
    def artifacts(self) -> ArtifactsManager:
        """Artifacts manager."""
        return self._artifacts

    @property
    def metadata(self) -> MetadataManager:
        """Metadata manager."""
        return self._metadata

    @property
    def checks(self) -> ChecksManager:
        """Checks manager."""
        return self._checks

    @property
    def data_profiles(self) -> DataProfilesManager:
        """Data Profiles manager."""
        return self._data_profiles

    @property
    def batch_predictions(self) -> BatchPredictionManager:
        """Batch Predictions manager."""
        return self._batch_predictions

    @property
    def metrics(self) -> MetricsManager:
        """Metrics manager."""
        return self._metrics

    @property
    def assignments(self) -> DatasetVersionAssignmentManager:
        """Dataset Version Assignment manager."""
        return self._assignments

    def update(self, paths: List[str]) -> DatasetVersion:
        """Update DatasetVersion.

        Arguments:
            paths: A list of paths to be updated.

        Returns:
            An updated DatasetVersion.

        Examples:
            >>> ...
        """
        return self._manager.update(paths=paths, dataset_version=self)
