from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy import select
from app.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import generate_access_token

from .base import BaseService

password_hasher = PasswordHash.recommended()
# to prevent timing attacks
DUMMY_HASH = password_hasher.hash("dummy_password")


class UserService(BaseService):
    def __init__(self, model: type[User], session: AsyncSession):
        self.model = model
        self.session = session

    async def _add_user(self, data: dict):
        user = self.model(
            **data,
            password_hash=password_hasher.hash(data["password"])
        )
        return await self._add(user)

    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password) -> str | None:
        # validate the credentials
        user = await self._get_by_email(email)

        if user is None:
            # prevent a timing attack by hashing the password even if the user doesn't exist
            password_hasher.verify(password, DUMMY_HASH)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

        # now verify the password
        if not password_hasher.verify(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

        # generate a jwt token
        return generate_access_token(data={
            "user": {
                "name": user.name,
                "id": str(user.id)
            }
        })
