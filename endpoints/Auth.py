from fastapi import APIRouter
from pydantic import BaseModel
from MagicalAuth import MagicalAuth


router = APIRouter()


class Register(BaseModel):
    email: str
    first_name: str
    last_name: str
    company_name: str
    job_title: str


class Login(BaseModel):
    email: str
    token: str


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    company_name: str
    job_title: str


@router.post("/register")
def register(
    register: Register,
):
    auth = MagicalAuth(email=register.email)
    mfa_token = auth.register(
        first_name=register.first_name,
        last_name=register.last_name,
        company_name=register.company_name,
        job_title=register.job_title,
    )
    return {"mfa_token": mfa_token}


@router.post("/login")
def login(login: Login):
    auth = MagicalAuth(email=login.email, token=login.token)
    user = auth.login()
    return {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "company_name": user.company_name,
        "job_title": user.job_title,
    }


@router.post("/send_magic_link")
def send_magic_link(login: Login):
    auth = MagicalAuth(email=login.email)
    magic_link = auth.send_magic_link(otp=login.token)
    return {"message": magic_link}


@router.put("/update_user")
def update_user(update: UserInfo, login: Login):
    auth = MagicalAuth(email=login.email, token=login.token)
    user = auth.login()
    user.first_name = update.first_name
    user.last_name = update.last_name
    user.company_name = update.company_name
    user.job_title = update.job_title
    return {"message": "User updated successfully."}


@router.get("/status")
def ready():
    return {"message": "Ready."}
