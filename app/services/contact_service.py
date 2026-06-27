from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contact_message import ContactMessage
from app.models.phone_request import PhoneRequest
from app.models.user import User
from app.schemas.contact import ContactMessageCreate, PhoneRequestCreate


class ContactService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_contact_message(
        self,
        data: ContactMessageCreate,
        current_user: User,
    ) -> ContactMessage:
        contact_message = ContactMessage(
            user_id=current_user.id,
            email=current_user.email,
            message=data.message.strip(),
        )
        self.db.add(contact_message)
        await self.db.commit()
        await self.db.refresh(contact_message)
        return contact_message

    async def create_phone_request(
        self,
        data: PhoneRequestCreate,
        current_user: User,
    ) -> PhoneRequest:
        phone_request = PhoneRequest(
            user_id=current_user.id,
            email=current_user.email,
            phone_number=data.phone_number.strip(),
        )
        self.db.add(phone_request)
        await self.db.commit()
        await self.db.refresh(phone_request)
        return phone_request

    async def get_all_contact_messages_admin(
        self,
    ) -> list[ContactMessage]:
        result = await self.db.scalars(
            select(ContactMessage)
            .order_by(
                ContactMessage.created_at.desc(),
            )
        )
        return list(result.all())

    async def get_all_phone_requests_admin(
        self,
    ) -> list[PhoneRequest]:
        result = await self.db.scalars(
            select(PhoneRequest)
            .order_by(
                PhoneRequest.created_at.desc(),
            )
        )
        return list(result.all())