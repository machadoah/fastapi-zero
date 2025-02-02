from fastapi import FastAPI, status

from fastapi_zero.routers import auth, html, users
from fastapi_zero.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(html.router)


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}
