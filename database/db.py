from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import get_db_url

engine = create_async_engine(
    url=get_db_url(),
    pool_size=20,
    max_overflow=30
)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)