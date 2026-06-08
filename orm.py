from datetime import datetime, timedelta, UTC
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, create_session
from database import async_engine, Base, async_session_factory
from models import User, Subscription


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            pass

    @staticmethod
    async def add_user_with_sub(username: str = "Slava", plan_name: str = "Standard", days: int = 30):
        async with async_session_factory() as session:
            async with session.begin():
                user = User(username=username)
                session.add(user)
                await session.flush()
                user_subscription = Subscription(user_id=user.id, plan_name=plan_name, expires_at=(
                            datetime.now(UTC).replace(tzinfo=None) + timedelta(days=days)))
                session.add(user_subscription)

    @staticmethod
    async def get_all_users_with_their_subs():
        async with async_session_factory() as session:
            query = (
                select(User)
                .options(joinedload(User.subscriptions))
            )
            res = await session.execute(query)
            result = res.scalars().unique().all()
            print(f"{result=}")

