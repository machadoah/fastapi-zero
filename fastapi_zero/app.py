from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import Message

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
