from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import Message, UserList, UserPublic, UserSchema
from fastapi_zero.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=UserPublic
)
def crete_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists.',
            )

        if db_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists.',
            )

    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(
    limit: int = 10,
    skip: int = 0,
    session: Session = Depends(get_session),
):
    users = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user_by_id(user_id: int, session: Session = Depends(get_session)):
    if user_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='ID must be a positive integer',
        )

    user = session.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {user_id} not found!',
        )

    return user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No enough permissions',
        )

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No enough permissions',
        )

    session.delete(current_user)
    session.commit()

    return {'message': f'User with id {user_id} deleted!'}
