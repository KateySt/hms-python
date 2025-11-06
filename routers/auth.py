import uuid

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext

from models import User
from repo import get_user_repository
from repo.userRepo import UserRepository
from schemas import UserSchema, UserSchemaIn
from templates import templates

router = APIRouter(prefix="/auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/signup")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/signup")
def register(
        request: Request,
        form_data: UserSchemaIn = Depends(UserSchemaIn.as_form),
        repo: UserRepository = Depends(get_user_repository),
):
    if repo.find_by_name(form_data.name):
        return RedirectResponse(url="/auth/login", status_code=302)

    hashed_pwd = pwd_context.hash(form_data.password)
    user = User(name=form_data.name, password=hashed_pwd)
    repo.save(user)

    return RedirectResponse(url="/auth/login", status_code=302)


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
        request: Request,
        form_data: UserSchema = Depends(UserSchema.as_form),
        repo: UserRepository = Depends(get_user_repository),
):
    user = repo.find_by_name(form_data.name)
    if user and pwd_context.verify(form_data.password, user.password):
        response = RedirectResponse(url="/auth/me", status_code=303)
        response.set_cookie("user_id", str(user.id))
        return response
    return RedirectResponse(url="/auth/login", status_code=303)


@router.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/auth/login")
    response.delete_cookie("user_id")
    return response


@router.get("/me")
def get_user_me(request: Request, repo: UserRepository = Depends(get_user_repository)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/auth/login", status_code=303)

    user = repo.find_by_id(uuid.UUID(user_id))
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)

    return templates.TemplateResponse(
        "me.html",
        {"request": request, "user": user}
    )


@router.get('/forgot-password')
def forgot_password_form(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})


@router.post('/forgot-password')
def forgot_password(
        request: Request,
        name: str = Form(...),
        repo: UserRepository = Depends(get_user_repository)
):
    if user := repo.find_by_name(name):
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "user_id": user.id}
        )
    return templates.TemplateResponse("register.html", {"request": request})


@router.get('/reset-password')
def reset_password_form(request: Request, user_id: str = None):
    return templates.TemplateResponse("reset_password.html", {"request": request, "user_id": user_id})


@router.post('/reset-password')
def reset_password(
        request: Request,
        user_id: str = Form(...),
        password: str = Form(...),
        repo: UserRepository = Depends(get_user_repository)
):
    user = repo.find_by_id(uuid.UUID(user_id))
    if not user:
        return templates.TemplateResponse("register.html", {"request": request})

    hashed_pwd = pwd_context.hash(password)
    user.password = hashed_pwd
    repo.update(user)

    return templates.TemplateResponse("login.html", {"request": request})
