"""
The step context is a context manager that is used to supervise a single step
of a digital worker. It is used in lieu of the ``@step`` decorator for
situations when you do not want to write a function for a step. For example,
it is very useful when iterating over a list of items:

.. code-block:: python

    from thoughtful.supervisor import supervise, step_scope

    def times_two(integers: list) -> None:
        return integers * 2

    def times_three(integer: int) -> None:
        return integer * 3

    def main():
        num_list = [1, 2, 3, 4, 5]

        with step_scope("1.1"):
            num_list = times_two(num_list)

        for num in num_list:
            with step_scope("1.2"):
                num = times_three(num)

    if __name__ == '__main__':
        with supervise():
            main()

Aside: There are a few scenarios where this is actually more convenient than
using the decorator on a lower level. Thanks to the fact that we can yield
the ``self`` object from a context manager, we can use this to update
attributes such as the record status, the step status, and is even a bit
cleaner when setting the record ID.
"""

from __future__ import annotations

import copy
import warnings
from types import TracebackType
from typing import List, Optional, Type, Union

from thoughtful.supervisor.recorder import Recorder
from thoughtful.supervisor.reporting.record import Record
from thoughtful.supervisor.reporting.report_builder import ReportBuilder
from thoughtful.supervisor.reporting.report_builder import StepReportBuilder
from thoughtful.supervisor.reporting.status import Status
from thoughtful.supervisor.reporting.timer import Timer
from thoughtful.supervisor.streaming.callback import StreamingCallback


class StepContext:
    """
    A context manager for a step that is running inside another step.
    This is an alternative to ``@step`` decorator when you don't want
    to write an entire function for a step.
    """

    def __init__(
        self,
        builder: ReportBuilder,
        recorder: Recorder,
        *step_id,
        record_id: Optional[str] = None,
        streaming_callback: Optional[StreamingCallback] = None,
    ):
        """
        Args:
            builder: Where the step report will be written.
            recorder: Where messages and data logs will be written.
            *step_id: The step id of this step, ie `"1.1"`
            record_id: An optional ID of the record being actively processed
            streaming_callback (StreamingCallback, optional): If set, streams
                the status of work report steps to that callback handler.
                Defaults to `None`.
        """
        if len(step_id) > 1:
            warnings.warn(
                "Passing multiple step ids to StepContext is deprecated. "
                "Instead, pass a single step id string with dots, ie '1.1'",
                DeprecationWarning,
            )

        self.uuid = ".".join([str(n) for n in step_id])
        self.report_builder = builder
        self.recorder = recorder
        self.timer = Timer()
        self._status_override: Optional[Status] = None
        self.record_id: Optional[str] = record_id
        self.records: List[Record] = []
        self.streaming_callback = streaming_callback
        self.step_report_builder: StepReportBuilder

    def __enter__(self):
        """
        Logic for when this context is first started.

        Returns:
            MainContext: This instance.
        """
        start_time = self.timer.start()
        record = Record(self.record_id, Status.RUNNING) if self.record_id else None

        if self.record_id:
            warnings.simplefilter("once", DeprecationWarning)
            warnings.warn(
                "Using `record_id` in a step context is deprecated and will be "
                "removed in a later release. Use `set_record_status` instead.",
                DeprecationWarning,
            )
            warnings.simplefilter("default", DeprecationWarning)

        self.step_report_builder = StepReportBuilder(
            step_id=self.uuid,
            start_time=start_time,
            status=Status.RUNNING,
            message_log=self.recorder.messages,
            data_log=self.recorder.data,
            record=record,
        )
        if self.streaming_callback:
            self.streaming_callback.post_step_update(
                self.step_report_builder.to_report()
            )
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """
        Runs when the context is about to close, whether caused
        by a raised Exception or now.

        Returns:
            bool: True if the parent caller should ignore the
                Exception raised before entering this function
                (if any), False otherwise.
        """
        timed_info = self.timer.end()
        if self._status_override:
            step_status = self._status_override
        else:
            step_status = Status.FAILED if exc_type else Status.SUCCEEDED

        # Update step report with finished step details
        self.step_report_builder.end_time = timed_info.end
        self.step_report_builder.status = step_status

        # Append all step reports to the parent workflow
        final_report_builders = self.__create_final_workflow(
            legacy_record_status=step_status
        )
        self.report_builder.workflow.extend(final_report_builders)

        # Stream reports if requested
        if self.streaming_callback:
            for builder in final_report_builders:
                self.streaming_callback.post_step_update(builder.to_report())

        # Return False so that any exceptions inside this context
        # are still raised after this function ends
        return False

    def error(self) -> None:
        """
        Sets the status of this step to `Status.FAILED` in its `StepReport`.

        .. code-block:: python

            with step_scope("1.1") as s:
                ...  # do some stuff
                s.error()

        .. code-block:: json

            {
                "workflow": [
                    {
                        "step_id": "1.1",
                        "step_status": "failed"
                    }
                ]
            }
        """
        self.set_status(Status.FAILED)

    def set_status(self, status: Union[str, Status]) -> None:
        """
        Override the step context's status to be in the status of ``status``

        Args:
            status (str, Status): The status to set the step to

        .. code-block:: python

            with step_scope("1.1") as s:
                ...  # do some stuff
                s.set_status("warning")

        .. code-block:: json

            {
                "workflow": [
                    {
                        "step_id": "1.1",
                        "step_status": "warning"
                    }
                ]
            }
        """
        # Convert the status to the correct type if necessary
        safe_status = Status(status)
        self._status_override = safe_status

    def set_record_status(
        self, status: Union[str, Status], record_id: str = ""
    ) -> None:
        """
        Override a step context's record to be in the status of ``status``

        Args:
            status (str, Status): The status to set the record to
            record_id (str): The ID of the record

        .. code-block:: python

            with step_scope("1.1") as s:
                ...  # do some stuff
                s.set_record_status("warning", "record01")

        .. code-block:: json

            {
                "workflow": [
                    {
                        "step_id": "1.1",
                        "step_status": "succeeded",
                        "record": {
                            "id": "kaleb_cool_guy",
                            "status": "warning"
                        }
                    }
                ]
            }

        """
        # Convert the status to the correct type if necessary
        safe_status = Status(status)
        record_id_to_update = record_id or self.record_id

        if not record_id:
            warnings.simplefilter("once", DeprecationWarning)
            warnings.warn(
                "Setting a record status *without* the `record_id` param is "
                "deprecated and will be removed in a future release",
                DeprecationWarning,
            )
            warnings.simplefilter("default", DeprecationWarning)

        if not record_id_to_update:
            warnings.warn(
                "Setting a record status for a step without "
                "a record ID will have no effect",
                UserWarning,
            )

        new_record = Record(record_id=record_id_to_update, status=safe_status)
        self.records.append(new_record)

    def __create_final_workflow(
        self, legacy_record_status: Status
    ) -> List[StepReportBuilder]:
        # Create a step report builder for every record, or create a single step
        # report if no records
        workflow: List[StepReportBuilder] = []
        for record in self.records:
            new_builder = copy.deepcopy(self.step_report_builder)
            new_builder.record = record
            workflow.append(new_builder)

        # If you're using the old way, and passing in a record ID at the step
        # context entrance, *and* you didn't override the status above, then
        # find the status based on if this context had an exception
        if self.record_id:
            # Check that the record wasn't already reported
            record_ids_already_reported = [
                step_builder.record.record_id for step_builder in workflow
            ]
            if self.record_id not in record_ids_already_reported:
                warnings.simplefilter("once", DeprecationWarning)
                warnings.warn(
                    "Using `record_id` in a step context is deprecated and "
                    "will be removed in the future. Use `StepContext::set_record_status` instead.",
                    DeprecationWarning,
                )

                # Create the new record report
                new_record = Record(
                    record_id=self.record_id, status=legacy_record_status
                )

                new_record_builder = copy.deepcopy(self.step_report_builder)
                new_record_builder.record = new_record
                new_record_builder.status = legacy_record_status
                workflow.append(new_record_builder)

        # Create the "final" step report builder that reports the whole step's
        # status without any records attached
        #
        # This builder "closes out" the step
        closed_step_builder = copy.deepcopy(self.step_report_builder)
        closed_step_builder.record = None
        workflow.append(closed_step_builder)

        return workflow


if __name__ == "__main__":
    report_builder = ReportBuilder()
    r = Recorder()

    substep = StepContext

    with substep(report_builder, r, 1) as s:
        print("hello world")

        with substep(report_builder, r, 1, 1) as s2:
            print("inner step")

    print(report_builder.workflow)
