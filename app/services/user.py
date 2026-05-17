import re
from uuid import UUID
from fastapi import BackgroundTasks, HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy import select
from app.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.notification import NotificationService
from app.utils import decode_url_safe_token, generate_access_token, generate_url_safe_token

from .base import BaseService
from app.config import app_settings

password_hasher = PasswordHash.recommended()
# to prevent timing attacks
DUMMY_HASH = password_hasher.hash("dummy_password")


class UserService(BaseService):
    def __init__(self, model: type[User], session: AsyncSession, tasks: BackgroundTasks):
        self.model = model
        self.session = session
        self.notification_service = NotificationService(tasks)

    async def _add_user(self, data: dict, router_prefix: str):
        user = self.model(
            **data,
            password_hash=password_hasher.hash(data["password"])
        )
        # add user first so we can get the id
        user = await self._add(user)
        token = generate_url_safe_token({
            "email": user.email,
            "id": str(user.id)
        })
        # send an email on user registration
        await self.notification_service.send_mail_with_template(
            recipients=[user.email],
            subject="Verify your email",
            context={
                "username": user.name,
                "verification_url": f"{app_settings.APP_BASE_URL}/{router_prefix}/verify?token={token}"
            },
            template_name="mail_email_verify.html"
        )
        return user

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
        # check if the user's email has been verified
        if not user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email not verified"
            )
        # generate a jwt token
        return generate_access_token(data={
            "user": {
                "name": user.name,
                "id": str(user.id)
            }
        })

    async def verify_email(self, token: str):
        token_data = decode_url_safe_token(token)
        # if token data is not valid
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Token"
            )

        user = await self._get(UUID(token_data["id"]))
        user.email_verified = True
        await self._update(user)

    async def check_user_verified(self, email) -> bool:
        user = await self._get_by_email(email)
        if not user or not user.email_verified:
            return False
        return True
