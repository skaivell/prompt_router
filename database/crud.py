from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ChatRequests

async def get_user_requests(
    ip_address: str, 
    session: AsyncSession
    )-> list[ChatRequests]:
    query = select(ChatRequests).filter_by(ip_address=ip_address)
    result = await session.execute(query)
    return result.scalars().all()

async def add_request_data(
    ip_address: str, 
    prompt: str,
    response: str,
    session: AsyncSession
    )-> None:
    new_request = ChatRequests(
        ip_address=ip_address,
        prompt=prompt,
        response=response
    )
    
    session.add(new_request)
    await session.commit()