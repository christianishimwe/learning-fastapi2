
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.api.dependencies import DeliveryPartnerDep, DeliveryPartnerServiceDep, get_partner_access_token
from app.database.models import DeliveryPartner
from app.database.redis import add_jti_to_blacklist
from ..schemas.delivery_partner import DeliveryPartnerCreate, DeliveryPartnerRead, DeliveryPartnerUpdate

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(delivery_partner: DeliveryPartnerCreate, service: DeliveryPartnerServiceDep):
    DeliveryPartner_out = await service.add(delivery_partner)
    return DeliveryPartner_out


@router.post("/login")
async def login_delivery_partner(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: DeliveryPartnerServiceDep,):
    # see if the email is verified
    # get the user
    if not await service.check_user_verified(request_form.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified")
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }


@router.post("/", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    return await service.update(
        partner.sqlmodel_update(partner_update)
    )


@router.get("/logout")
async def logout_delivery_partner(token_data: Annotated[dict, Depends(get_partner_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {
        "detail": "successfully logged out"
    }


@router.get("/verify")
async def verify_seller_email(token: str, service: DeliveryPartnerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account Verified"}
