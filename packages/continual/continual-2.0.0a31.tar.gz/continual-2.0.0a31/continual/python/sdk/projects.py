from __future__ import annotations
from typing import List, Optional
from google.protobuf import field_mask_pb2
from continual.python.sdk.environments import EnvironmentManager
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager


class ProjectManager(Manager):
    """Manages project resources."""

    name_pattern: str = "projects/{project}"

    def create(
        self,
        organization: str,
        id: Optional[str] = "",
        display_name: Optional[str] = "",
        tags: Optional[dict[str, str]] = None,
        replace_if_exists: Optional[bool] = False,
    ) -> Project:
        """Create an project.

        New projects are identified by a unique project id that is
        generated from the display name. However project ids are globally unique across
        all organizations.

        Arguments:
            organization: Organization resource name.
            display_name: Display name.
            id : Project id.
            tags: Tags to add to the project.

        Returns:
            A new project.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> client.projects.create(display_name="example-proj", organization=org.name)
            <Project object {'name': 'projects/example_proj', 'display_name': 'example-proj',
            'organization': 'organizations/ceddjsa5lsrtvmkpogm0',
            'summary': {'feature_set_health': {'healthy_count': 0, 'unhealthy_count': 0, 'critical_count': 0}, '
            model_health': {'healthy_count': 0, 'unhealthy_count': 0, 'critical_count': 0}, 'feature_set_count': 0,
            'feature_set_row_count': '0', 'feature_set_bytes': '0', 'feature_count': 0, 'connection_count': 0, 'model_count': 0,
            'model_version_count': 0, 'experiment_count': '0', 'prediction_count': '0'}, 'update_time': '2022-12-15T08:25:29.713213Z',
            'create_time': '2022-12-15T08:25:29.707384Z', 'default_environment': 'projects/example_proj/environments/production'}>
        """
        if tags and not all(
            [isinstance(k, str) and isinstance(v, str) for k, v in tags.items()]
        ):
            raise ValueError("Tags must be a dict of str: str")
        req = management_pb2.CreateProjectRequest(
            project=Project(
                display_name=display_name,
                organization=organization,
                tags=tags,
            ).to_proto(),
            project_id=id,
            replace_if_exists=replace_if_exists,
        )

        resp = self.client._management.CreateProject(req)
        return Project.from_proto(resp, client=self.client)

    def get(self, id: str) -> Project:
        """Get project.

        Arguments:
            id: Project name or id.

        Returns
            A project.

        Example:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.name)
            >>> client.projects.get(id=proj.name).display_name
            'example-proj'
        """

        req = management_pb2.GetProjectRequest(name=self.name(id))
        resp = self.client._management.GetProject(req)
        return Project.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: Optional[str] = None,
        latest: bool = True,
    ) -> List[Project]:
        """List projects.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.

        Returns:
            A list of projects.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> projs = [client.projects.create(f"project-{i}", organization=org.name) for i in range(10)]
            >>> [c.display_name for client.projects.list(page_size=10)]
            ['project-0', 'project-1', 'project-2', 'project-3', 'project-4', 'project-5', 'project-6', 'project-7', 'project-8', 'project-9']
        """

        req = management_pb2.ListProjectsRequest(
            parent=self.parent, page_size=page_size, order_by=order_by, latest=latest
        )
        resp = self.client._management.ListProjects(req)
        return [Project.from_proto(x, client=self.client) for x in resp.projects]

    def list_all(self) -> Pager[Project]:
        """List all projects.

        Pages through all projects using an iterator.

        Returns:
            A iterator of all projects.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> projs = [client.projects.create(f"project-{i}", organization=org.name) for i in range(5)]
            >>> [c.display_name for client.projects.list_all()]
            ['project-0', 'project-1', 'project-2', 'project-3', 'project-4']
        """

        def next_page(next_page_token):
            req = management_pb2.ListProjectsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListProjects(req)
            return (
                [Project.from_proto(x, client=self.client) for x in resp.projects],
                resp.next_page_token,
            )

        return Pager(next_page)

    def delete(self, id: str) -> None:
        """Delete an project.

        Arguments:
            id: Project name or id.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> projs = [client.projects.create(display_name=f"project-{i}", organization=org.id) for i in range(10)]
            >>> [client.projects.delete(id=proj.id)  for proj in client.projects.list_all()]
            [None, None, None, None, None, None, None, None, None, None]
            >>> len([org  for org in client.projects.list_all()])
            0
        """

        req = management_pb2.DeleteProjectRequest(name=self.name(id))
        self.client._management.DeleteProject(req)

    def update(
        self,
        id: str,
        display_name: Optional[str] = None,
    ) -> Project:
        """Update project.

        Arguments:
            id: The project's id.
            display_name:  Display name.

        Returns:
            Updated project.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="name_wiht_typo", organization=org.id)
            >>> client.projects.update(id=proj.name, display_name="name_without_typo").display_name
            'name_without_typo'
        """
        paths = []
        if display_name is not None:
            paths.append("display_name")

        req = management_pb2.UpdateProjectRequest(
            update_mask=field_mask_pb2.FieldMask(paths=paths),
            project=Project(name=self.name(id), display_name=display_name).to_proto(),
        )
        resp = self.client._management.UpdateProject(req)
        return Project.from_proto(resp, client=self.client)

    def update(
        self,
        paths: List[str],
        project: Project,
    ) -> Project:
        """Update Project.

        Arguments:
            paths: A list of paths to be updated.
            project: Project object containing updated fields.

        Returns:
            An updated Project.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
        """

        req = management_pb2.UpdateProjectRequest(
            project=project.to_proto(),
            update_paths=paths,
            run=self.run_name,
        )
        resp = self.client._management.UpdateProject(req)
        return Project.from_proto(resp, client=self.client)


class Project(Resource, types.Project):
    """Project resource."""

    name_pattern: str = "projects/{project}"

    _manager: ProjectManager

    _environments: EnvironmentManager

    def _init(self):
        self._manager = ProjectManager(parent=self.parent, client=self.client)
        self._environments = EnvironmentManager(parent=self.name, client=self.client)

    @property
    def environments(self) -> EnvironmentManager:
        """Environments manager."""
        return self._environments

    def delete(self) -> None:
        """Delete project.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.id)
            >>> proj.delete()
            >>> len([proj for proj in client.projects.list_all()])
            0
        """
        self._manager.delete(self.name)

    def update(self, paths: List[str] = None) -> Project:
        """Update project.

        Arguments:
            paths: A list of paths to be updated

        Returns:
            Updated project.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.id)
            >>> new_proj = proj.update(display_name="updated-example-proj")
            >>> new_proj.display_name
            'updated-proj-name'
        """
        return self._manager.update(project=self, paths=paths)
