from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    DONE = "DONE"


@dataclass
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus
    assignee: Optional[str]
    branch: Optional[str] = None
    pr_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


def create_task(title: str, description: str, assignee: Optional[str] = None) -> Task:
    return Task(
        id=uuid.uuid4().hex[:8],
        title=title,
        description=description,
        status=TaskStatus.TODO,
        assignee=assignee,
    )
