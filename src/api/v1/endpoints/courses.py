from typing import List, Union

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Path
from fastapi import Query
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.course_model import CourseModel
from src.schemas.course_schema import CourseSchema
from src.core.deps import get_session

router = APIRouter()


@router.get("/", summary="Listar cursos", description="Retorna todos os cursos cadastrados")
async def get_courses(title: str = Query(None, title="Título do curso", description="Filtro por título", min_length=3), db: AsyncSession = Depends(get_session)) -> Union[List[CourseSchema], dict[int, CourseSchema]]:
    async with db as session:
        query = select(CourseModel)

        if title:
            query = query.where(CourseModel.title.like(f"%{title}%"))

        result = await session.execute(query)
        courses = result.scalars().all()

        if not courses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Curso não encontrado"
            )

        return courses


@router.get("/{course_id}", summary="Obter curso", description="Retorna um curso específico")
async def get_course(course_id: int = Path(..., title="ID do curso", description="Deve ser maior ou igual a 1", ge=1), db: AsyncSession = Depends(get_session)) -> CourseSchema:
    async with db as session:
        query = select(CourseModel).where(CourseModel.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Curso não encontrado"
            )

        return course


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Criar curso", description="Cria um novo curso")
async def create_course(course: CourseSchema, db: AsyncSession = Depends(get_session)) -> CourseSchema:
    new_course = CourseModel(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)

    return new_course


@router.put("/{course_id}", summary="Atualizar curso", description="Atualiza um curso existente")
async def update_course(course_id: int, course: CourseSchema, db: AsyncSession = Depends(get_session)) -> CourseSchema:
    async with db as session:
        query = select(CourseModel).where(CourseModel.id == course_id)
        result = await session.execute(query)
        current_course = result.scalar_one_or_none()

        if not current_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Curso não encontrado"
            )

        for field, value in course.model_dump().items():
            if field != "id":
                setattr(current_course, field, value)

        await db.commit()

        return current_course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir curso", description="Exclui um curso existente")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).where(CourseModel.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Curso não encontrado"
            )

        await db.delete(course)
        await db.commit()

        return
