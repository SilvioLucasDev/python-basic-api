from typing import Optional

from pydantic import BaseModel as SchemaBaseModel, field_validator


class CourseSchema(SchemaBaseModel):
    id: Optional[int] = None
    title: str
    lessons: int
    hours: int

    class Config:
        orm_mode = True

    @field_validator('title')
    def validate_title(cls, value: str):
        if len(value) < 3:
            raise ValueError(
                "O título do curso deve ter no mínimo 3 caractere")
        return value
