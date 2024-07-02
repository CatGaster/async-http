import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func, Integer, String
import datetime


POSTGRES_USER = os.getenv["POSTGRES_USER", "postgres"]
POSTGRES_PASSWORD = os.getenv["POSTGRES_PASSWORD", "postgres"]
POSTGRES_DB_NAME = os.getenv["POSTGRES_DB_NAME","flask_db"]
POSTGRES_HOST = os.getenv["POSTGRES_HOST", "127.0.0.1"]
POSTGRES_PORT = os.getenv["POSTGRES_PORT", "5431"]


engine = create_async_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
                       f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}')

Session = async_sessionmaker(bind = engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    text: Mapped[str] = mapped_column(String(120), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    