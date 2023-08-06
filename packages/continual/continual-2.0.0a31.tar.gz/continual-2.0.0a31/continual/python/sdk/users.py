from __future__ import annotations
from typing import List, Optional
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager


class UserManager(Manager):
    """Manages user resources."""

    name_pattern: str = "users/{user}"

    def get(
        self,
        id: str,
    ) -> User:
        """Get user.

        Arguments:
            id: Fully qualified user name or id.

        Returns
            A User.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> client.users.get(id='zxNbTXkbxLeyjb3SUhJ2fR')
            User object {'name': 'users/zxNbTXkbxLeyjb3SUhJ2fR', 'email': 'test@continual.ai',
            'email_verified': True, 'full_name': 'test user', 'update_time': '2022-12-15T01:00:20.707583Z',
            'create_time': '2022-12-15T01:00:20.707583Z', 'trial_available': True, 'first_name':
            'test', 'last_name': 'user', 'bio': '', 'location': '', 'password': '',
            'service_account': False, 'disabled': False}>
        """

        req = management_pb2.GetUserRequest(name=self.name(id))
        resp = self.client._management.GetUser(req)
        return User.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: Optional[str] = None,
        latest: bool = True,
    ) -> List[User]:
        """List users.

        Arguments:
            page_size: Number of itmes to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.

        Returns:
            A list of users.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config (first user)
            >>> second_user = client.register(first_name='second', last_name='user', email='test2@continual.ai', password='test123')
            >>> [u.email for u in client.users.list(page_size=10)] # Orders by 'create_time' by default
            ['test@continual.ai', 'test2@continual.ai']
            >>> [u.email for u in client.users.list(page_size=10, latest=False)] # Ascending order
            ['test2@continual.ai', 'test@continual.ai']
        """
        req = management_pb2.ListUsersRequest(
            page_size=page_size, order_by=order_by, latest=latest
        )
        resp = self.client._management.ListUsers(req)
        return [User.from_proto(u, client=self.client) for u in resp.users]

    def list_all(self) -> Pager[User]:
        """List all users.

        Pages through all users using an iterator.

        Returns:
            A iterator of all users.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config (first user)
            >>> client.register(first_name='second', last_name='user', email='test2@continual.ai', password='test123') # Second user
            >>> client.users.list_all()
            <continual.python.sdk.iterators.Pager object at 0x7f82d469f8b0>
            >>> [u.email for u in client.users.list_all()]
            ['test2@continual.ai', 'test@continual.ai']
        """

        def next_page(next_page_token):
            req = management_pb2.ListUsersRequest(page_token=next_page_token)
            resp = self.client._management.ListUsers(req)
            return (
                [User.from_proto(u, client=self.client) for u in resp.users],
                resp.next_page_token,
            )

        return Pager(next_page)

    def delete(self, id: str) -> None:
        """Delete a user. (Admin only)

        Arguments:
            id: Name or id.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config (first user)
            >>> second_user = client.register(first_name='second', last_name='user', email='test2@continual.ai', password='test123') # Second user
            >>> client.users.delete(id=second_user.name)
        """

        req = management_pb2.DeleteUserRequest(name=self.name(id))
        self.client._management.DeleteUser(req)

    def update(
        self,
        paths: List[str],
        user: User,
    ) -> User:
        """Update User.

        Arguments:
            paths: A list of paths to update.
            user: A User object with updated field values.

        Returns:
            Updated user.
        """
        req = management_pb2.UpdateUserRequest(
            update_paths=paths, user=user.to_proto(), run=self.run_name
        )
        resp = self.client._management.UpdateUser(req)
        return User.from_proto(resp, client=self.client)


class User(Resource, types.User):
    """User resource."""

    name_pattern = "users/{users}"

    _manager: UserManager
    """Users Manager."""

    def _init(self):
        self._manager = UserManager(parent=self.parent, client=self.client)

    def delete(self) -> None:
        """Delete user."""
        self._manager.delete(self.name)

    def update(
        self,
        paths: List[str] = None,
    ) -> User:
        """Update user.

        Arguments:
            paths: A list of paths to update.

        Returns:
            Updated user.

        Examples:
            >>> from continual import Client
            >>> client = Client(verify=False)
            >>> user = client.register(first_name='test', last_name='user', email='test@continual.ai', password='test123')
            >>> user.first_name, user.last_name
            ('test', 'user')
            >>> updated_user = user.update(first_name='not test')
            >>> updated_user.first_name, updated_user.last_name
            ('not_test', 'user')
        """
        return self._manager.update(user=self, paths=paths)
