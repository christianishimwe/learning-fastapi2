# create an instance of the fastmail
import asyncio
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from app.config import notification_settings

fastmail = FastMail(
    ConnectionConfig(
        **notification_settings.model_dump()
    )
)
asyncio.run(
    fastmail.send_message(
        MessageSchema(
            recipients=[
                NameEmail(name="", email="christianishimwe90@gmail.com")],
            subject="mail from testing",
            body="Hello!",
            subtype=MessageType.plain
        )
    )
)
