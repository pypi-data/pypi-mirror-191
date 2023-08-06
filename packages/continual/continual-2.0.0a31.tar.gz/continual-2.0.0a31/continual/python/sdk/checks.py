from __future__ import annotations
from typing import List, Optional
from continual.python.sdk.iterators import Pager

from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.events import EventManager
from continual.rpc.management.v1 import management_pb2, types

CHUNK_SIZE = 117440512  # 112 MB in bytes, chosen arbitrarily


class ChecksManager(Manager):
    """Manages checks."""

    # the name pattern for a check depends on the resource it was created for
    name_pattern: str = ""

    def get(self, id: str) -> Check:
        """Get check.
        Arguments:
            id: Check name or id.
        Returns
            A Check.
        Examples:
            >>> ... # Assume client, project, environment, and dataset are defined
            >>> dataset_version = dataset.dataset_versions.create()
            >>> dc = dataset_version.checks.create(display_name="Check Null Values", group_name="test", outcome="PASSED", summary="No null values", state="PASS")
            >>> dataset_version.checks.get(id=dc.id)
            <Check object {'name': 'projects/continual_test_proj/environments/production/datasets/test_dataset/versions/cegaeq25lsrt9r5a8ma0/checks/cegai425lsrt9r5a8md0',
            'run_name': 'projects/continual_test_proj/environments/production/runs/cegaeq25lsrt9r5a8m80', 'group_name': 'test', 'outcome': 'PASSED',
            'summary': 'No null values', 'create_time': '2022-12-19T18:10:24.774076Z', 'display_name': 'Check Null Values', 'duration': 0.0,
            'errors': [], 'warnings': [], 'infos': [], 'artifact_name': ''}>
        """

        req = management_pb2.GetCheckRequest(
            name=self.name(
                id,
                parent=self.parent,
                name_pattern=f"{self.parent}/checks/{id}",
            )
        )
        check = self.client._management.GetCheck(req)
        return Check.from_proto(check, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: str = None,
        latest: bool = True,
    ) -> List[Check]:
        """List checks.
        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
        Returns:
            A list of Checks.
        Examples:
            >>> ... # Assume client, project, environment, and dataset are defined
            >>> dataset_version = dataset.dataset_versions.create()
            >>> checks = [dataset_version.checks.create(display_name=f"Test {i}", group_name="test", outcome=f"{('PASSED' if i%2 == 1 else 'FAILED')}", summary=f"Test {i} passed.") for i in range(5)]
            >>> [check.outcome for check in dataset_version.checks.list(page_size=10)]
            [<CheckOutcome.FAILED: 'FAILED'>, <CheckOutcome.PASSED: 'PASSED'>, <CheckOutcome.FAILED: 'FAILED'>, <CheckOutcome.PASSED: 'PASSED'>, <CheckOutcome.FAILED: 'FAILED'>]
            >>> [check.outcome for check in dataset_version.checks.list(page_size=10, order_by='outcome')]
            [<CheckOutcome.FAILED: 'FAILED'>, <CheckOutcome.PASSED: 'PASSED'>]
        """
        req = management_pb2.ListChecksRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            latest=latest,
        )
        resp = self.client._management.ListChecks(req)
        return [Check.from_proto(x, client=self.client) for x in resp.checks]

    def list_all(self) -> Pager[Check]:
        """List all checks.
        Pages through all checks using an iterator.
        Returns:
            A iterator of all checks.
        Examples:
            >>> ... # Assume client, project, environment, and dataset are defined
            >>> dataset_version = dataset.dataset_versions.create()
            >>> checks = [dataset_version.checks.create(display_name=f"Test {i}", group_name="test", outcome='PASSED', summary=f"Test {i} passed.") for i in range(5)]
            >>> [check.summary for check in dataset_version.checks.list_all()]
            ['Test 0 passed.', 'Test 1 passed.', 'Test 2 passed.', 'Test 3 passed.', 'Test 4 passed.']
        """

        def next_page(next_page_token):
            req = management_pb2.ListChecksRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListChecks(req)
            return (
                [Check.from_proto(x, client=self.client) for x in resp.checks],
                resp.next_page_token,
            )

        return Pager(next_page)

    def create(
        self,
        display_name: str,
        outcome: str,
        message: str = "",
        current_value: float = 0.0,
        baseline_value: float = 0.0,
        id: Optional[str] = None,
        replace_if_exists: bool = False,
    ) -> Check:
        """Create a Check.
        Arguments:
            display_name: Display name of the check.
            outcome: whether the check PASSED, FAILED, or was SKIPPED.
            message: A message describing the check.
            current_value: A numeric value that is the current value that is the basis for the check
            baseline_value: A numeric value that is being compared the current value.
            id: Optional ID of the check.
            replace_if_exists: If true, replace the check if it already exists.

        Returns:
            Check object.
        Examples:
            >>> ... # Assume client, project, environment, and dataset are defined
            >>> dataset_version = dataset.dataset_versions.create()
            >>> dataset_version.checks.create(
            ...         display_name="Check Missing Index",
            ...         outcome="PASSED",
            ...         message="No missing indices",
            ...         current_value=0.5,
            ...         baseline_value=0.45,
            ...     )
            <Check object {'name': 'projects/cfe4f5lvn3dbhpkhmq50/environments/production/datasets/docds-train/versions/cfir5glvn3d45h6t2jv0/checks/cfir5ntvn3d45h6t2k0g', 'display_name': 'Check Missing Index', 'message': 'No missing indices', 'current_value': 0.5, 'baseline_value': 0.45, 'update_time': '2023-02-10T02:58:39.424586Z', 'create_time': '2023-02-10T02:58:39.424586Z', 'run': '', 'outcome': 'PASSED'}>"""
        req = management_pb2.CreateCheckRequest(
            parent=self.parent,
            check=Check(
                display_name=display_name,
                outcome=outcome,
                message=message,
                run_name=self.run_name,
                current_value=float(current_value)
                if isinstance(current_value, int)
                else current_value,
                baseline_value=float(baseline_value)
                if isinstance(baseline_value, int)
                else baseline_value,
            ).to_proto(),
            check_id=id,
            replace_if_exists=replace_if_exists,
        )
        resp = self.client._management.CreateCheck(req)
        return Check.from_proto(resp, client=self.client)

    def update(
        self,
        paths: List[str],
        check: Check,
    ) -> Check:
        """Update Check.

        Arguments:
            paths: A list of paths to be updated.
            check: Check object containing updated fields.

        Returns:
            An updated Check.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
        """

        req = management_pb2.UpdateCheckRequest(
            check=check.to_proto(),
            update_paths=paths,
            run=self.run_name,
        )
        resp = self.client._management.UpdateCheck(req)
        return Check.from_proto(resp, client=self.client)


class Check(Resource, types.Check):
    """Check check."""

    # the name pattern for check depends on the resource it was created for
    name_pattern: str = ""
    _manager: ChecksManager

    events: EventManager
    """Event manager."""

    def _init(self):
        self._manager = ChecksManager(parent=self.parent, client=self.client)

    def update(self, paths: List[str]) -> Check:
        """Update Check.

        Arguments:
            paths: A list of paths to be updated.

        Returns:
            An updated Check.

        Examples:
            >>> ...
        """
        return self._manager.update(paths=paths, check=self)
