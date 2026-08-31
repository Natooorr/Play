from dataclasses import dataclass, field
from typing import Optional


# NOTE: status is just a free string, not an enum, so "done", "Done", "DONE"
# are all technically "valid" values. This is intentional (bad practice).
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "pending"
    priority: int = 1

    def to_dict(self):
        # manual dict conversion instead of using dataclasses.asdict, for no good reason
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
        }


def validate_task_data(data: dict) -> Optional[str]:
    """Returns an error message string if invalid, otherwise None.

    Very loose validation on purpose - doesn't check priority range,
    doesn't check status against allowed values, doesn't strip whitespace
    from title so " " passes as a valid title.
    """
    if "title" not in data:
        return "title is required"
    # bug: empty string check is wrong, only catches None not ""
    if data.get("title") is None:
        return "title cannot be empty"
    return None
