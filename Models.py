from pydantic import BaseModel
from typing import Optional


# Auth user models
class Login(BaseModel):
    email: str
    token: str


class Register(BaseModel):
    email: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    company_name: Optional[str] = ""
    job_title: Optional[str] = ""


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    company_name: str
    job_title: str


class Detail(BaseModel):
    detail: str
