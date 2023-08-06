from __future__ import annotations

from typing import List, Optional
from continual.python.sdk.batchpredictions import (
    BatchPredictionManager,
)
from continual.python.sdk.events import EventManager
from continual.python.sdk.checks import ChecksManager
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.experiments import ExperimentManager
from continual.python.sdk.promotions import PromotionManager
from continual.python.sdk.metrics import MetricsManager
from continual.python.sdk.artifacts import ArtifactsManager

from continual.python.sdk.metadata import MetadataManager


class ModelVersionManager(Manager):
    """Manages Model Version resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/versions/{version}"

    def create(
        self,
        id: Optional[str] = "",
        state: Optional[str] = "CREATED",
        error_message: Optional[str] = "",
        stack_trace: Optional[str] = "",
        performance_metric_name: Optional[str] = "",
        performance_metric_val: Optional[float] = 0.0,
        tags: Optional[dict[str, str]] = None,
        replace_if_exists: Optional[bool] = False,
    ) -> ModelVersion:
        """Create a model version for local development

        Arguments:
            id: Optional model version id.
            state: Optional model version state.
            error_message: Error message associated with this model version
            stack_trace: Stack trace associated with an error.
            performance_metric_name: Name of the primary metric.
            performance_metric_val: Value of the primary metric.
            tags: Optional tags to associate with this model version.
            replace_if_exists: If true, update the model version if it already exists.

        Returns
            A Model Version.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model.model_versions.create()
            <ModelVersion object {'name': 'projects/test_proj_4/environments/test_env/models/my_model/versions/ceg98ea5lsrt9r5a8l10',
            'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0',
            'state': 'CREATED', 'create_time': '2022-12-19T16:41:29.232614Z', 'update_time': '2022-12-19T16:41:29.232614Z',
            'experiment_name': '', 'error_message': '', 'stack_trace': '', 'training_row_count': '0', 'validation_row_count': '0',
            'test_row_count': '0', 'performance_metric': '', 'performance_metric_val': 0.0, 'promotion': '', 'promoted': False}>
        """
        if tags and not all(
            [isinstance(k, str) and isinstance(v, str) for k, v in tags.items()]
        ):
            raise ValueError("Tags must be a dict of str: str")
        req = management_pb2.CreateModelVersionRequest(
            parent=self.parent,
            model_version=ModelVersion(
                run=self.run_name,
                state=state,
                error_message=error_message,
                stack_trace=stack_trace,
                performance_metric_name=performance_metric_name,
                performance_metric_val=performance_metric_val,
                tags=tags,
            ).to_proto(),
            model_version_id=id,
            replace_if_exists=replace_if_exists,
        )
        resp = self.client._management.CreateModelVersion(req)
        return ModelVersion.from_proto(resp, client=self.client)

    def get(self, id: str) -> ModelVersion:
        """Get model version.

        Arguments:
            id: Model name or id.

        Returns
            An Model Version.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> model.model_versions.get(model_version.id)
            <ModelVersion object {'name': 'projects/test_proj_4/environments/test_env/models/my_model/versions/ceg98ea5lsrt9r5a8l10',
            'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0',
            'state': 'CREATED', 'create_time': '2022-12-19T16:41:29.232614Z', 'update_time': '2022-12-19T16:41:29.232614Z',
            'experiment_name': '', 'error_message': '', 'stack_trace': '', 'training_row_count': '0', 'validation_row_count': '0',
            'test_row_count': '0', 'performance_metric': '', 'performance_metric_val': 0.0, 'promotion': '', 'promoted': False}>
        """
        req = management_pb2.GetModelVersionRequest(name=self.name(id))
        resp = self.client._management.GetModelVersion(req)
        return ModelVersion.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: str = None,
        latest: bool = True,
        all_projects: bool = False,
    ) -> List[ModelVersion]:
        """List model versions.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
            all_projects: Whether to include all instances of this resource from the project or just from the current parent.

        Returns:
            A list of model versions.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> models = [model.model_versions.create() for _ in range(3)]
            >>> first_model_version = model.model_versions.list(page_size=10)[0]               # Get first model version
            >>> latest_model_version = model.model_versions.list(page_size=10, latest=True)[0] # Get latest model version
        """
        req = management_pb2.ListModelVersionsRequest(
            parent=self.parent,
            page_size=page_size,
            all_projects=all_projects,
            order_by=order_by,
            latest=latest,
        )
        resp = self.client._management.ListModelVersions(req)
        return [
            ModelVersion.from_proto(x, client=self.client) for x in resp.model_versions
        ]

    def list_all(self) -> Pager[ModelVersion]:
        """List all model versions.

        Pages through all model versions using an iterator.

        Returns:
            A iterator of all model versions.

        Examples:
            >>> ... # Assume client, project, environment are defined
            >>> run = env.runs.create("My run")
            >>> model = run.models.get("my_model")
            >>> dvs = [model.model_versions.create() for _ in range(3)]
            >>> len(list(model.model_versions.list_all())) # List all model versions
            3
        """

        def next_page(next_page_token):
            req = management_pb2.ListModelVersionsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListModelVersions(req)
            return (
                [
                    ModelVersion.from_proto(x, client=self.client)
                    for x in resp.model_versions
                ],
                resp.next_page_token,
            )

        return Pager(next_page)

    def update(
        self,
        paths: List[str],
        model_version: ModelVersion,
    ) -> ModelVersion:
        """Update model version.

        Arguments:
            paths: A list of paths to be updated.
            model_version: Model version object containing updated fields.

        Returns:
            An updated model version.

        Examples:
            >>> ... # Assume client, project, and environment are defined.

        """

        req = management_pb2.UpdateModelVersionRequest(
            model_version=model_version.to_proto(),
            update_paths=paths,
            run=self.run_name,
        )
        resp = self.client._management.UpdateModelVersion(req)
        return ModelVersion.from_proto(resp, client=self.client)


class ModelVersion(Resource, types.ModelVersion):
    """Model version resource."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/versions/{version}"

    _manager: ModelVersionManager

    _experiments: ExperimentManager

    _events: EventManager

    _promotions: PromotionManager

    _checks: ChecksManager

    _batch_predictions: BatchPredictionManager

    _metrics: MetricsManager

    _artifacts: ArtifactsManager

    _metadata: MetadataManager

    def _init(self):
        self._manager = ModelVersionManager(
            parent=self.parent, client=self.client, run_name=self.run
        )
        self._promotions = PromotionManager(
            parent=self.parent, client=self.client, run_name=self.run
        )
        self._batch_predictions = BatchPredictionManager(
            parent=self.parent, client=self.client, run_name=self.run
        )
        self._experiments = ExperimentManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._events = EventManager(
            parent=self.name, client=self.client, run_name=self.run
        )
        self._metrics = MetricsManager(
            parent=self.name, client=self.client, run_name=self.run
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

    @property
    def promotions(self) -> PromotionManager:
        """Promotion manager."""
        return self._promotions

    @property
    def batch_predictions(self) -> BatchPredictionManager:
        """Batch Prediction manager."""
        return self._batch_predictions

    @property
    def experiments(self) -> ExperimentManager:
        """Experiment manager."""
        return self._experiments

    @property
    def metrics(self) -> MetricsManager:
        """Metrics manager."""
        return self._metrics

    @property
    def artifacts(self) -> ArtifactsManager:
        """Artifacts manager."""
        return self._artifacts

    @property
    def checks(self) -> ChecksManager:
        """Checks manager."""
        return self._checks

    @property
    def metadata(self) -> MetadataManager:
        """Metadata manager."""
        return self._metadata

    @property
    def events(self) -> EventManager:
        """Event manager."""
        return self._events

    def update(
        self,
        state: Optional[str] = None,
        error_message: Optional[str] = None,
        stack_trace: Optional[str] = None,
        performance_metric_name: Optional[str] = None,
        performance_metric_val: Optional[float] = None,
        feature_importances: Optional[List[dict[str, float]]] = None,
        signature: Optional[dict[str, List[dict[str, str]]]] = None,
    ):

        paths = []
        if state:
            paths.append("state")
            self.state = state
        if error_message:
            paths.append("error_message")
            self.error_message = error_message
        if stack_trace:
            paths.append("stack_trace")
            self.stack_trace = stack_trace
        if performance_metric_name:
            paths.append("performance_metric_name")
            self.performance_metric_name = performance_metric_name
        if performance_metric_val:
            paths.append("performance_metric_val")
            self.performance_metric_val = performance_metric_val
        if feature_importances:
            paths.append("feature_importance")
            self.feature_importances = []
            for fi in feature_importances:
                if "feature" in fi and "importance" in fi:
                    self.feature_importances.append(
                        types.FeatureImportance(
                            feature=fi["feature"], importance=fi["importance"]
                        )
                    )
        if signature:
            paths.append("signature")
            pb_signature = types.ModelVersionSignature(inputs=[], outputs=[])
            if "inputs" in signature:
                for input in signature["inputs"]:
                    if "name" in input and "type" in input:
                        pb_signature.inputs.append(
                            types.ModelVersionSignatureInput(
                                name=input["name"], type=input["type"]
                            )
                        )
            if "outputs" in signature:
                for output in signature["outputs"]:
                    if "type" in output:
                        pb_signature.outputs.append(
                            types.ModelVersionSignatureOutput(type=output["type"])
                        )

            self.signature = pb_signature

        if len(paths) > 0:
            self._manager.update(paths=paths, model_version=self)
