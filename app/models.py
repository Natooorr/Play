from dataclasses import dataclass
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


Status = Literal["pending", "in_progress", "completed"]


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    status: Status = "pending"
    priority: int = Field(default=1, ge=1, le=5)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value):
        if value is not None and not value.strip():
            raise ValueError("title must not be blank")
        return value


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[Status] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value):
        if value is not None and not value.strip():
            raise ValueError("title must not be blank")
        return value


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "pending"
    priority: int = 1

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
        }
