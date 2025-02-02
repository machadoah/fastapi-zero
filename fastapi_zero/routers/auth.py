from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import Token
from fastapi_zero.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


# endpoint para criar token
@router.post('/token', response_model=Token)
def login_for_access_token(
    session: T_Session,  # session, conexão com banco de dados
    form_data: T_OAuth2Form,  # formulários oauth2
):
    # com base no username do formulário, vê se ele existe no banco
    user = session.scalar(select(User).where(User.email == form_data.username))

    # se o usuário não existir ou a senha não for válida
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password',
        )

    # cria o access token
    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
