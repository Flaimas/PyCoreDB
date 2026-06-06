from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)

async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        if "subscriptions" in self.__dict__:
            loaded_subs = self.__dict__["subscriptions"]
            if loaded_subs:
                subs_repr = f"Subscriptions {[sub.plan_name for sub in loaded_subs]}"
            else:
                subs_repr = f"Subscriptions []"
            cols.append(subs_repr)

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
