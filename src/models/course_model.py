from src.core.configs import settings

from sqlalchemy import Column, Integer, String


class CourseModel(settings.DBBaseModel):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), index=True)
    lessons = Column(Integer)
    hours = Column(Integer)
