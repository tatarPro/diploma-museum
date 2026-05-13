"""
models.py — ORM-модели SQLAlchemy, соответствующие таблицам базы данных.
"""

import enum
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, Enum, DateTime,
    ForeignKey, func,
)
from sqlalchemy.orm import relationship

from database import Base


# ─── Перечисление ролей пользователя ─────────────────────────────────────────

class UserRole(str, enum.Enum):
    admin     = "admin"
    moderator = "moderator"


# ─── Таблица users ────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    login         = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role          = Column(Enum(UserRole), nullable=False, default=UserRole.moderator)
    created_at    = Column(DateTime, server_default=func.now())

    # Обратные связи
    articles = relationship("Article", back_populates="author")
    exhibits = relationship("Exhibit",  back_populates="author")


# ─── Таблица articles ─────────────────────────────────────────────────────────

class Article(Base):
    __tablename__ = "articles"

    id                = Column(Integer, primary_key=True, index=True)
    title             = Column(String(255), nullable=False)
    content           = Column(Text, nullable=False)
    preview_image_url = Column(String(512), nullable=True)
    main_image_url    = Column(String(512), nullable=True)
    author_id         = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at        = Column(DateTime, server_default=func.now())

    author = relationship("User", back_populates="articles")
    images = relationship(
        "ArticleImage",
        back_populates="article",
        cascade="all, delete-orphan",  # удалять изображения при удалении статьи
    )


class ArticleImage(Base):
    __tablename__ = "article_images"

    id         = Column(Integer, primary_key=True, index=True)
    url        = Column(String(512), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)

    article = relationship("Article", back_populates="images")


# ─── Таблица exhibits ─────────────────────────────────────────────────────────

class Exhibit(Base):
    __tablename__ = "exhibits"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    photo_url   = Column(String(512), nullable=True)
    exhibit_url   = Column(String(512), nullable=True)  # путь к .glb файлу
    author_id   = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at  = Column(DateTime, server_default=func.now())

    author = relationship("User", back_populates="exhibits")
    images = relationship(
        "ExhibitImage",
        back_populates="exhibit",
        cascade="all, delete-orphan",
    )


class ExhibitImage(Base):
    __tablename__ = "exhibit_images"

    id         = Column(Integer, primary_key=True, index=True)
    url        = Column(String(512), nullable=False)
    exhibit_id = Column(Integer, ForeignKey("exhibits.id", ondelete="CASCADE"), nullable=False)

    exhibit = relationship("Exhibit", back_populates="images")
