"""
schemas.py — Pydantic-схемы для валидации запросов и сериализации ответов.
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from models import UserRole


# ─── Auth ─────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    login:    str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    role:         UserRole


# ─── Users ────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    login:    str
    password: str
    role:     UserRole = UserRole.moderator


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:         int
    login:      str
    role:       UserRole
    created_at: datetime


# ─── Article Images ───────────────────────────────────────────────────────────

class ArticleImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:  int
    url: str


# ─── Articles ─────────────────────────────────────────────────────────────────

class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:                int
    title:             str
    content:           str
    preview_image_url: Optional[str]
    main_image_url:    Optional[str]
    author_id:         Optional[int]
    created_at:        datetime
    images:            List[ArticleImageOut] = []


# ─── Exhibit Images ───────────────────────────────────────────────────────────

class ExhibitImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:  int
    url: str


# ─── Exhibits ─────────────────────────────────────────────────────────────────

class ExhibitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:          int
    title:       str
    description: str
    photo_url:   Optional[str]
    exhibit_url:   Optional[str]
    author_id:   Optional[int]
    created_at:  datetime
    images:      List[ExhibitImageOut] = []
