from datetime import datetime, timedelta
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import TokenData
from fastapi_zero.settings import Settings

pwd_context = PasswordHash.recommended()

# oauth2_scheme é um objeto que pode ser usado para autenticar usuários,
# ele é um objeto que pode ser usado como dependência em qualquer rota
# que precise de autenticação
# tokenUrl é o endpoint que o usuário deve acessar para obter um token
# de acesso
# Obs: no swagger ele aparece como 'Authorize' e um cadeado
#      mostrando que é necessário autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
settings = Settings()

T_Session = Annotated[Session, Depends(get_session)]


def get_password_hash(password: str):
    return pwd_context.hash(password=password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(password=plain_password, hash=hashed_password)


# função responsavel por criar token jwt
def create_access_token(data: dict):
    # copia das informações internas no payload
    to_encode = data.copy()

    # data do utc
    date_now = datetime.now(tz=ZoneInfo('UTC'))

    # tempo que o teken valera
    minutes = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # adiciona um tempo em minutos que tera expiração
    expire = date_now + minutes

    # adiciona uma expiração além do 'sub' recebido no data
    to_encode.update({'exp': expire})

    # encoda, o payload (data - sub - mais o exp), chave e algoritmo
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    # retorna o encode jwt
    return encoded_jwt


# VERIFICA quem é o usuário que está fazendo operação
def get_current_user(
    session: T_Session,
    token: str = Depends(oauth2_scheme),
):
    # se não conseguir validar as credenciais
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        # decodifica o token recebido
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        # pega o sub do payload
        username: str = payload.get('sub')

        # se não tiver sub
        if not username:
            raise credentials_exception

        # cria um objeto TokenData com o username
        token_data = TokenData(username=username)

    # se não conseguir decodificar
    except DecodeError:
        raise credentials_exception

    # procura no banco de dados o usuário com o email do token
    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    # se não encontrar o usuário
    if not user:
        raise credentials_exception

    # retorna o usuário
    return user
