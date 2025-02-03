from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import Todo, TodoState, User
from fastapi_zero.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fastapi_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: T_CurrentUser, session: T_Session):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(  # noqa: PLR0917 PLR0913 (too many arguments)
    session: T_Session,
    user: T_CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: TodoState | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(session: T_Session, user: T_CurrentUser, todo_id: int):
    todo = session.scalar(select(Todo).where(Todo.id == todo_id))

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found'
        )

    session.delete(todo)
    session.commit()

    return {'message': 'Todo deleted'}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, session: T_Session, user: T_CurrentUser, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
