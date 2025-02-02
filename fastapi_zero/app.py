from fastapi import FastAPI

from fastapi_zero.routers import auth, root, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(root.router)
