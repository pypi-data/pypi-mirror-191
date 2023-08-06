"""
This module handles the actual assembly of the run report. It converts each of
the step reports into a ``StepReport`` object and then converts the run
to a ``Report`` object containing the list of ``StepReport`` objects.

It returns this ``Report`` object as the final product of the run.
"""

from __future__ import annotations

import datetime
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from thoughtful.supervisor.manifest import StepId
from thoughtful.supervisor.recorder import DataLog, MessageLog
from thoughtful.supervisor.reporting.record import Record
from thoughtful.supervisor.reporting.report import Report
from thoughtful.supervisor.reporting.status import Status
from thoughtful.supervisor.reporting.step_report import StepReport
from thoughtful.supervisor.reporting.timer import Timer


@dataclass
class StepReportBuilder:
    """
    Builds a dynamic digital worker step. This is similar to the ``StepReport``
    except that this is higher level in that it contains unflattened data
    structures, such as ``Record`` objects. It has functionality
    to produce a ``StepReport`` from itself.
    """

    step_id: str
    """
    str: The ID of the step.
    """

    start_time: datetime.datetime
    """
    datetime.datetime: The start time of the step.
    """

    status: Status
    """
    Status: The status of the step.
    """

    end_time: Optional[datetime.datetime] = None
    """
    datetime.datetime: The end time of the step.
    """

    message_log: MessageLog = field(default_factory=list)
    """
    MessageLog: The message log of the step.
    """

    data_log: DataLog = field(default_factory=list)
    """
    DataLog: The data log of the step.
    """

    record: Optional[Record] = None
    """
    Record, optional: The record of the step.
    """

    def to_report(self) -> StepReport:
        """
        An easily "jsonable" final report on this step's execution.

        Returns:
            StepReport: A final report on this step's execution.
        """

        # Build the report
        return StepReport(
            step_id=self.step_id,
            status=self.status,
            start_time=self.start_time,
            end_time=self.end_time,
            message_log=self.message_log,
            data_log=self.data_log,
            record=self.record,
        )


RecordId = str


@dataclass
class ReportBuilder:
    """
    A work report builder that creates a new work report as a digital worker
    is executed.
    """

    timer: Timer = field(default_factory=Timer)
    """
    Timer: The timer used to time the execution of the workflow.
    """

    workflow: List[StepReportBuilder] = field(default_factory=list)
    """
    List[StepReportBuilder]: The list of step reports.
    """

    timer_start: float = time.perf_counter()
    """
    float: The start time of the workflow.
    """

    status: Optional[Status] = None
    """
    Status, optional: The status of the run.
    """

    # These steps will be overridden with the specified status when the
    # `Report` is written
    _step_statuses_to_override: Dict[StepId, Status] = field(default_factory=dict)
    """
    Dict[StepId, Status]: The statuses to override for each step
    """

    _record_statuses_to_override: Dict[StepId, Dict[RecordId, Status]] = field(
        default_factory=lambda: defaultdict(dict)
    )
    """
    Dict[StepId, Dict[RecordId, Status]]: The statuses to override for each
    record
    """

    run_had_exception: bool = False
    """
    Boolean value to indicate if the run terminated on an exception.
    """

    _run_status_override: Optional[Status] = None
    """
    Override the status of the run to be in the status of `status`.
    """

    def __post_init__(self):
        self.timer.start()

    def fail_step(self, step_id: str) -> None:
        """
        Override a step to be in the `StepStatus.ERROR` state. Note: this
        overrides every step with this ID, so if the step ran multiple times
        in the workflow, they will all be marked as failed.

        Args:
            step_id (str): The step id to override.
        """
        self.set_step_status(step_id=step_id, status=Status.FAILED)

    def set_step_status(self, step_id: str, status: Union[Status, str]) -> None:
        """
        Override a step to be in the status of `status`. Note: this
        overrides every step with this ID, so if the step ran multiple times
        in the workflow, they will all be marked as this `status`.

        Args:
            step_id (str): The step id to override.
            status (Status | str): The status to override the step to.
        """
        # Convert the status to the correct type if necessary
        safe_status = Status(status)
        self._step_statuses_to_override[step_id] = safe_status

    def set_record_status(
        self, step_id: str, record_id: str, status: Union[Status, str]
    ) -> None:
        """
        Override a record to be in the status of `status`. Note: this
        overrides every step with this step ID and this record ID, so if the
        step ran multiple times in the workflow, they will all be marked as
        this `status`.

        Args:
            step_id (str): The step id a specific step that contains this record
            record_id (str): The id of the record to override.
            status (Status | str): The status to override the record to.
        """
        # Convert the status to the correct type if necessary
        safe_status = Status(status)
        self._record_statuses_to_override[step_id][record_id] = safe_status

    def set_run_status(self, status: Union[Status, str]) -> None:
        """
        Manually set the status of the bot run. If not set, the run
        status will be determined automatically

        Args:
            status (Union[Status, str]): The status to override the run to.
        """
        # Convert the status to the correct type if necessary
        safe_status = Status(status)
        self._run_status_override = safe_status

    def to_report(self) -> Report:
        """
        Convert supervisor workflow to work report. It is here that we
        convert the entire workflow to a list of ``StepReport`` objects.
        After which, we pass over the entire list overriding the record
        and step statuses according to the ``_step_statuses_to_override``
        and ``_record_statuses_to_override`` dictionaries.

        Returns:
            Report: The finalized work report.
        """
        timed = self.timer.end()

        # Update step reports with any overridden statuses
        steps = [x.to_report() for x in self.workflow]
        for step_report in steps:
            # Update step statuses
            if step_report.step_id in self._step_statuses_to_override:
                new_status = self._step_statuses_to_override[step_report.step_id]
                step_report.status = new_status
            # Update the record statuses
            if step_report.step_id in self._record_statuses_to_override:
                records = self._record_statuses_to_override[step_report.step_id]
                if step_report.record.record_id in records:
                    new_status = records[step_report.record.record_id]
                    step_report.record.status = new_status

        # Set the run status
        self.status = Status.FAILED if self.run_had_exception else Status.SUCCEEDED
        if self._run_status_override is not None:
            self.status = self._run_status_override

        return Report(
            start_time=timed.start,
            end_time=timed.end,
            workflow=steps,
            status=self.status,
        )
