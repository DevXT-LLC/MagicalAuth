from pydantic import BaseModel


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


class Detail(BaseModel):
    detail: str
