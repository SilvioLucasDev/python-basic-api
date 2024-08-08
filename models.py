from typing import Optional

from pydantic import BaseModel, field_validator


class Course(BaseModel):
    id: Optional[int] = None
    title: str
    lessons: int
    hours: int

    @field_validator('title')
    def validate_title(cls, value: str):
        if len(value) < 3:
            raise ValueError(
                "O título do curso deve ter no mínimo 3 caracteres")
        return value

    @field_validator('lessons')
    def validate_lessons(cls, value: int):
        if value < 1:
            raise ValueError("O número de aulas deve ser maior que 0")
        return value

    @field_validator('hours')
    def validate_hours(cls, value: int):
        if value < 1:
            raise ValueError("O número de horas deve ser maior que 0")
        return value


courses = [
    Course(id=1, title="Programação em Python", lessons=112, hours=58),
    Course(id=2, title="Banco de Dados", lessons=56, hours=20),
]
