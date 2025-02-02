from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    Token,
)
from fastapi_zero.security import (
    create_access_token,
    verify_password,
)

app = FastAPI()


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}


@app.get('/html', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def read_html():
    return """
<html>
    <head>
        <title>Nosso olá mundo</title>
    </head>
    <body>
        <h1>Olá, Mundo!</h1>
    </body>
</html>
"""


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
