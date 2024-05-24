from fastapi import APIRouter, Request, Header, Depends
from Models import Detail, OTP, UserInfo, Register
from MagicalAuth import MagicalAuth, verify_api_key
from Globals import getenv
import pyotp

router = APIRouter()


@router.post("/v1/user")
def register(register: Register):
    mfa_token = MagicalAuth().register(
        email=register.email,
        first_name=register.first_name,
        last_name=register.last_name,
        company_name=register.company_name,
        job_title=register.job_title,
    )
    totp = pyotp.TOTP(mfa_token)
    otp_uri = totp.provisioning_uri(name=register.email, issuer_name=getenv("APP_NAME"))
    return {"otp_uri": otp_uri}


@router.get("/v1/user/exists", response_model=bool, summary="Check if user exists")
def get_user(email: str) -> bool:
    try:
        return MagicalAuth().user_exists(email=email)
    except:
        return False


@router.get(
    "/v1/user",
    dependencies=[Depends(verify_api_key)],
    summary="Get user details",
)
def login(
    request: Request,
    authorization: str = Header(None),
):
    user_data = MagicalAuth(token=authorization).login(ip_address=request.client.host)
    return {
        "email": user_data.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "company_name": user_data.company_name,
        "job_title": user_data.job_title,
    }


@router.post(
    "/v1/login",
    response_model=Detail,
    summary="Login with email and OTP token",
)
def send_magic_link(request: Request, otp: OTP):
    magic_link = MagicalAuth().send_magic_link(
        email=otp.email, otp=otp.token, ip_address=request.client.host
    )
    return Detail(detail=magic_link)


@router.put(
    "/v1/user",
    dependencies=[Depends(verify_api_key)],
    response_model=Detail,
    summary="Update user details",
)
def update_user(update: UserInfo, request: Request, authorization: str = Header(None)):
    user = MagicalAuth(token=authorization).update_user(
        ip_address=request.client.host, **update.model_dump()
    )
    return Detail(detail=user)


# Delete user
@router.delete(
    "/v1/user",
    dependencies=[Depends(verify_api_key)],
    response_model=Detail,
    summary="Delete user",
)
def delete_user(
    user=Depends(verify_api_key),
    authorization: str = Header(None),
):
    MagicalAuth(token=authorization).delete_user()
    return Detail(detail="User deleted successfully.")
