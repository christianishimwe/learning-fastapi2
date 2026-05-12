
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.api.dependencies import DeliveryPartnerDep, SellerServiceDep, get_seller_access_token
from app.api.schemas.delivery_partner import DeliveryPartnerUpdate
from app.database.models import Seller
from app.database.redis import add_jti_to_blacklist
from ..schemas.seller import SellerCreate, SellerRead

router = APIRouter(prefix="/seller", tags=["seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    seller_out = await service.add(seller)
    return seller_out


@router.post("/login")
async def login_seller(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: SellerServiceDep):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }


@router.get("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_seller_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {
        "detail": "successfully logged out"
    }


@router.get("/", response_model=SellerRead)
async def get_seller(id: UUID, service: SellerServiceDep):
    return await service.get(id)

# update the delivery partner


@router.post("/")
async def update_delivery_partner(partner_update: DeliveryPartnerUpdate, partner: DeliveryPartnerDep, service):
    pass
