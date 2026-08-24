from datetime import datetime
from src.models.task import Task, TaskStatus, create_task


class TestTaskStatus:
    def test_enum_values(self):
        assert TaskStatus.TODO.value == "TODO"
        assert TaskStatus.IN_PROGRESS.value == "IN_PROGRESS"
        assert TaskStatus.IN_REVIEW.value == "IN_REVIEW"
        assert TaskStatus.DONE.value == "DONE"

    def test_all_statuses(self):
        assert len(TaskStatus) == 4


class TestTask:
    def test_create_dataclass(self):
        task = Task(
            id="abc123",
            title="Test task",
            description="A test",
            status=TaskStatus.TODO,
            assignee="Session A",
        )
        assert task.id == "abc123"
        assert task.title == "Test task"
        assert task.status == TaskStatus.TODO
        assert task.assignee == "Session A"
        assert task.branch is None
        assert task.pr_url is None

    def test_optional_fields(self):
        task = Task(
            id="x",
            title="t",
            description="d",
            status=TaskStatus.DONE,
            assignee=None,
            branch="feature/T01",
            pr_url="https://github.com/test/repo/pull/1",
        )
        assert task.branch == "feature/T01"
        assert task.pr_url == "https://github.com/test/repo/pull/1"

    def test_created_at_default(self):
        task = Task(id="x", title="t", description="d", status=TaskStatus.TODO, assignee=None)
        assert isinstance(task.created_at, datetime)


class TestCreateTask:
    def test_factory_defaults(self):
        task = create_task("My task", "Description")
        assert len(task.id) == 8
        assert task.title == "My task"
        assert task.description == "Description"
        assert task.status == TaskStatus.TODO
        assert task.assignee is None

    def test_factory_with_assignee(self):
        task = create_task("T", "D", assignee="Session B")
        assert task.assignee == "Session B"

    def test_unique_ids(self):
        t1 = create_task("A", "a")
        t2 = create_task("B", "b")
        assert t1.id != t2.id
