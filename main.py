from models import Course
from models import courses

# from routes import courses_router

from typing import Union

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Path
from fastapi import Query
from fastapi import Depends


def fake_db():
    try:
        print("Conectando ao banco de dados")
    finally:
        print("Fechando conexão com o banco de dados")


app = FastAPI(
    title="API de Cursos (SLDS)",
    description="API para cadastro, consulta, atualização e exclusão de cursos",
    version="0.0.1",
)

# app.include_router(courses_router.router, tags=["Cursos"])


@app.get("/courses", summary="Listar cursos", description="Retorna todos os cursos cadastrados")
async def get_courses(title: str = Query(None, title="Título do curso", description="Filtro por título", min_length=3), db=Depends(fake_db)) -> Union[list[Course], dict[int, Course]]:
    if title:
        for course_id, course in courses.items():
            if course["title"] == title:
                return {course_id: course}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    return courses


@app.get("/courses/{course_id}", summary="Obter curso", description="Retorna um curso específico")
async def get_course(course_id: int = Path(..., title="ID do curso", description="Deve ser maior ou igual a 1", ge=1), db=Depends(fake_db)) -> Course:
    try:
        return courses[course_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )


@app.post("/courses", status_code=status.HTTP_201_CREATED, summary="Criar curso", description="Cria um novo curso")
async def create_course(course: Course, db=Depends(fake_db)) -> Course:
    next_id = len(courses) + 1
    course.id = next_id
    courses.append(course.model_dump())
    return course


@app.put("/courses/{course_id}", summary="Atualizar curso", description="Atualiza um curso existente")
async def update_course(course_id: int, course: Course, db=Depends(fake_db)) -> Course:
    if course_id not in courses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    courses[course_id] = course.model_dump()
    return course


@app.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir curso", description="Exclui um curso existente")
async def delete_course(course_id: int, db=Depends(fake_db)):
    if course_id not in courses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    del courses[course_id]
    return


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )
