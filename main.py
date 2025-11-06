from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.auth import router as auth_router
import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
