
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.api.dependencies import SellerServiceDep, SessionDep, get_token_data
from app.database.models import Seller
from app.utils import decode_access_token
from ..schemas.seller import SellerCreate, SellerRead

router = APIRouter(prefix="/seller", tags=["seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    seller_out = await service.add(seller)


@router.post("/login")
async def login_seller(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: SellerServiceDep):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }


@router.get("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_token_data)]):
    token_data["jti"]
    pass
