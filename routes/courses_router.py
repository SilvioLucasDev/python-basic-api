# from fastapi import APIRouter

# router = APIRouter()


# @app.get("/api/v1/courses", summary="Listar cursos", description="Retorna todos os cursos cadastrados")
# async def get_courses(title: str = Query(None, title="Título do curso", description="Filtro por título", min_length=3), db=Depends(fake_db)) -> Union[list[Course], dict[int, Course]]:
#     if title:
#         for course_id, course in courses.items():
#             if course["title"] == title:
#                 return {course_id: course}
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Curso não encontrado"
#         )
#     return courses
