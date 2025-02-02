from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse

router = APIRouter(prefix='/html', tags=['html'])


@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
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
