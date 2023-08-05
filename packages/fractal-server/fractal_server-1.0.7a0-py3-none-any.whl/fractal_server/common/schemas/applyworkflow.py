from datetime import datetime
from typing import List
from typing import Optional

from sqlmodel import SQLModel


__all__ = (
    "ApplyWorkflowBase",
    "ApplyWorkflowCreate",
    "ApplyWorkflowRead",
)


class ApplyWorkflowBase(SQLModel):
    """
    Base class for ApplyWorkflow

    Attributes:
        input_dataset_id: TBD
        output_dataset_id: TBD
        workflow_id: TBD
        overwrite_input: TBD
        worker_init: TBD
        working_dir: TBD
        working_dir_user: TBD
    """

    project_id: int
    input_dataset_id: int
    output_dataset_id: Optional[int]
    workflow_id: Optional[int]
    overwrite_input: bool = False
    worker_init: Optional[str]
    working_dir: Optional[str]
    working_dir_user: Optional[str]


class ApplyWorkflowCreate(ApplyWorkflowBase):
    pass


class ApplyWorkflowRead(ApplyWorkflowBase):
    id: int
    start_timestamp: datetime
    status: str
    log: Optional[str]
    history: Optional[List[str]]

    def sanitised_dict(self):
        d = self.dict()
        d["start_timestamp"] = str(self.start_timestamp)
        return d
