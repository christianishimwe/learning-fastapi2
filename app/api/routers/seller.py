
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.api.dependencies import SellerDep
from app.utils import decode_access_token
from ..schemas.seller import SellerCreate, SellerRead


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/login")
router = APIRouter(prefix="/seller", tags=["seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerDep):
    seller_out = await service.add(seller)


@router.post("/login")
async def login_seller(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: SellerDep):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }


@router.get("/dashboard")
async def get_dashboard(token: Annotated[str, Depends(oauth2_scheme)],):
    data = decode_access_token(token)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access Token")

    return {
        "detail": "Successfully Authenticated"
    }
