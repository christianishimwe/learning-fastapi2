
from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.seller import SellerCreate
from app.database.models import Seller
from pwdlib import PasswordHash
from sqlalchemy import select
import jwt
from app.config import jwt_settings
from app.utils import generate_access_token

password_hasher = PasswordHash.recommended()
# to prevent timing attacks
DUMMY_HASH = password_hasher.hash("dummy_password")


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID):
        return await self.session.get(Seller, id)

    async def add(self, credentials: SellerCreate) -> Seller:
        seller = Seller(
            **credentials.model_dump(exclude={"password"}),
            password_hash=password_hasher.hash(credentials.password)
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller

    async def token(self, email, password) -> str | None:
        # validate the credentials
        result = await self.session.execute(
            select(Seller).where(Seller.email == email))

        seller = result.scalar()

        if seller is None:
            # prevent a timing attack by hashing the password even if the user doesn't exist
            password_hasher.verify(password, DUMMY_HASH)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

        # now verify the password
        if not password_hasher.verify(password, seller.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

        # generate a jwt token
        token = generate_access_token(data={
            "user": {
                "name": seller.name,
                "id": str(seller.id)
            }
        })
        return token


print(password_hasher.hash("password123"))
