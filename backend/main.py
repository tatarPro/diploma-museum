"""
main.py — Главный файл FastAPI-приложения.
Запуск: uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

import os
import uuid
import shutil
from pathlib import Path
from typing import List, Optional

from fastapi import (
    FastAPI, Depends, HTTPException, status,
    UploadFile, File, Form,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import models
import schemas
from auth import (
    hash_password, verify_password,
    create_access_token,
    get_current_user, require_admin,
)
from database import Base, engine, get_db

# ─── Инициализация ────────────────────────────────────────────────────────────

# Создаём таблицы при старте (если не существуют)
Base.metadata.create_all(bind=engine)

# Папки для статических файлов
STATIC_DIR = Path("static")
for folder in ["images", "models"]:
    (STATIC_DIR / folder).mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Museum API",
    description="Информационная система музея студенческого поискового отряда",
    version="1.0.0",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # В продакшне заменить на конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Статика ──────────────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")


# ─── Вспомогательные функции ─────────────────────────────────────────────────

def save_upload(upload: UploadFile, subfolder: str) -> str:
    """
    Сохраняет загруженный файл в /static/<subfolder>/ с уникальным именем.
    Возвращает относительный URL вида /static/images/uuid_filename.ext
    """
    ext = Path(upload.filename).suffix
    filename = f"{uuid.uuid4().hex}{ext}"
    dest = STATIC_DIR / subfolder / filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)
    return f"/static/{subfolder}/{filename}"


def delete_file(url: Optional[str]) -> None:
    """Удаляет физический файл по его относительному URL, если он существует."""
    if url:
        path = Path(url.lstrip("/"))
        if path.exists():
            path.unlink()


# ─── Init-admin ───────────────────────────────────────────────────────────────

@app.post("/init-admin", tags=["System"])
def init_admin(db: Session = Depends(get_db)):

    existing = db.query(models.User).filter(models.User.login == "admin").first()
    if existing:
        raise HTTPException(status_code=400, detail="Администратор уже существует")
    admin = models.User(
        login=         "admin",
        password_hash= hash_password("123"),
        role=          models.UserRole.admin,
    )
    db.add(admin)
    db.commit()
    return {"detail": "Администратор создан. Login: admin, Password: 123"}


# ─── Auth ─────────────────────────────────────────────────────────────────────

@app.post("/auth/login", response_model=schemas.TokenResponse, tags=["Auth"])
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Аутентификация пользователя. Возвращает JWT-токен и роль."""
    user = db.query(models.User).filter(models.User.login == payload.login).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return schemas.TokenResponse(access_token=token, role=user.role)


# ─── Users (только admin) ────────────────────────────────────────────────────

@app.get("/users", response_model=List[schemas.UserOut], tags=["Users"])
def get_users(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    """Получить список всех пользователей (только admin)."""
    return db.query(models.User).all()


@app.post("/users", response_model=schemas.UserOut, status_code=201, tags=["Users"])
def create_user(
    payload: schemas.UserCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    """Создать нового пользователя (только admin)."""
    if db.query(models.User).filter(models.User.login == payload.login).first():
        raise HTTPException(status_code=400, detail="Логин уже занят")
    user = models.User(
        login=         payload.login,
        password_hash= hash_password(payload.password),
        role=          payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current: models.User = Depends(require_admin),
):
    """Удалить пользователя (только admin, нельзя удалить себя)."""
    if user_id == current.id:
        raise HTTPException(status_code=400, detail="Нельзя удалить себя")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"detail": "Пользователь удалён"}


# ─── Exhibits (Экспонаты) ─────────────────────────────────────────────────────

@app.get("/exhibits", response_model=List[schemas.ExhibitOut], tags=["Exhibits"])
def get_exhibits(db: Session = Depends(get_db)):
    """Получить список всех экспонатов (публичный)."""
    return db.query(models.Exhibit).order_by(models.Exhibit.created_at.desc()).all()


@app.get("/exhibits/{exhibit_id}", response_model=schemas.ExhibitOut, tags=["Exhibits"])
def get_exhibit(exhibit_id: int, db: Session = Depends(get_db)):
    """Получить один экспонат по ID (публичный)."""
    exhibit = db.query(models.Exhibit).filter(models.Exhibit.id == exhibit_id).first()
    if not exhibit:
        raise HTTPException(status_code=404, detail="Экспонат не найден")
    return exhibit


@app.post("/exhibits", response_model=schemas.ExhibitOut, status_code=201, tags=["Exhibits"])
def create_exhibit(
    title:       str             = Form(...),
    description: str             = Form(...),
    photo:       Optional[UploadFile] = File(None),
    model:       Optional[UploadFile] = File(None),
    gallery:     List[UploadFile]     = File(default=[]),
    db:          Session          = Depends(get_db),
    current:     models.User      = Depends(get_current_user),
):
    photo_url = save_upload(photo, "images") if photo and photo.filename else None
    exhibit_url = save_upload(model, "models") if model and model.filename else None

    exhibit = models.Exhibit(
        title=       title,
        description= description,
        photo_url=   photo_url,
        exhibit_url=   exhibit_url,
        author_id=   current.id,
    )
    db.add(exhibit)
    db.flush()

    for img in gallery:
        if img.filename:
            url = save_upload(img, "images")
            db.add(models.ExhibitImage(url=url, exhibit_id=exhibit.id))

    db.commit()
    db.refresh(exhibit)
    return exhibit


@app.put("/exhibits/{exhibit_id}", response_model=schemas.ExhibitOut, tags=["Exhibits"])
def update_exhibit(
    exhibit_id:  int,
    title:       str             = Form(...),
    description: str             = Form(...),
    photo:       Optional[UploadFile] = File(None),
    model:       Optional[UploadFile] = File(None),
    gallery:     List[UploadFile]     = File(default=[]),
    db:          Session          = Depends(get_db),
    _:           models.User      = Depends(get_current_user),
):
    """Обновить экспонат (защищённый)."""
    exhibit = db.query(models.Exhibit).filter(models.Exhibit.id == exhibit_id).first()
    if not exhibit:
        raise HTTPException(status_code=404, detail="Экспонат не найден")

    exhibit.title       = title
    exhibit.description = description

    if photo and photo.filename:
        delete_file(exhibit.photo_url)
        exhibit.photo_url = save_upload(photo, "images")

    if model and model.filename:
        delete_file(exhibit.exhibit_url)
        exhibit.exhibit_url = save_upload(model, "models")

    for img in gallery:
        if img.filename:
            url = save_upload(img, "images")
            db.add(models.ExhibitImage(url=url, exhibit_id=exhibit.id))

    db.commit()
    db.refresh(exhibit)
    return exhibit


@app.delete("/exhibits/{exhibit_id}", tags=["Exhibits"])
def delete_exhibit(
    exhibit_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    """Удалить экспонат и все его файлы (защищённый)."""
    exhibit = db.query(models.Exhibit).filter(models.Exhibit.id == exhibit_id).first()
    if not exhibit:
        raise HTTPException(status_code=404, detail="Экспонат не найден")

    delete_file(exhibit.photo_url)
    delete_file(exhibit.exhibit_url)
    for img in exhibit.images:
        delete_file(img.url)

    db.delete(exhibit)
    db.commit()
    return {"detail": "Экспонат удалён"}


@app.delete("/exhibits/{exhibit_id}/images/{image_id}", tags=["Exhibits"])
def delete_exhibit_image(
    exhibit_id: int,
    image_id:   int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    """Удалить одно изображение из галереи экспоната."""
    img = db.query(models.ExhibitImage).filter(
        models.ExhibitImage.id == image_id,
        models.ExhibitImage.exhibit_id == exhibit_id,
    ).first()
    if not img:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    delete_file(img.url)
    db.delete(img)
    db.commit()
    return {"detail": "Изображение удалено"}


# ─── Articles (Статьи / Истории экспедиций) ──────────────────────────────────

@app.get("/articles", response_model=List[schemas.ArticleOut], tags=["Articles"])
def get_articles(db: Session = Depends(get_db)):
    """Получить список всех статей (публичный)."""
    return db.query(models.Article).order_by(models.Article.created_at.desc()).all()


@app.get("/articles/{article_id}", response_model=schemas.ArticleOut, tags=["Articles"])
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Получить одну статью по ID (публичный)."""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return article


@app.post("/articles", response_model=schemas.ArticleOut, status_code=201, tags=["Articles"])
def create_article(
    title:         str                  = Form(...),
    content:       str                  = Form(...),
    preview_image: Optional[UploadFile] = File(None),
    main_image:    Optional[UploadFile] = File(None),
    gallery:       List[UploadFile]     = File(default=[]),
    db:            Session              = Depends(get_db),
    current:       models.User          = Depends(get_current_user),
):
    """Создать статью с файлами (защищённый)."""
    preview_url = save_upload(preview_image, "images") if preview_image and preview_image.filename else None
    main_url    = save_upload(main_image, "images")    if main_image    and main_image.filename    else None

    article = models.Article(
        title=             title,
        content=           content,
        preview_image_url= preview_url,
        main_image_url=    main_url,
        author_id=         current.id,
    )
    db.add(article)
    db.flush()

    for img in gallery:
        if img.filename:
            url = save_upload(img, "images")
            db.add(models.ArticleImage(url=url, article_id=article.id))

    db.commit()
    db.refresh(article)
    return article


@app.put("/articles/{article_id}", response_model=schemas.ArticleOut, tags=["Articles"])
def update_article(
    article_id:    int,
    title:         str                  = Form(...),
    content:       str                  = Form(...),
    preview_image: Optional[UploadFile] = File(None),
    main_image:    Optional[UploadFile] = File(None),
    gallery:       List[UploadFile]     = File(default=[]),
    db:            Session              = Depends(get_db),
    _:             models.User          = Depends(get_current_user),
):
    """Обновить статью (защищённый)."""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    article.title   = title
    article.content = content

    if preview_image and preview_image.filename:
        delete_file(article.preview_image_url)
        article.preview_image_url = save_upload(preview_image, "images")

    if main_image and main_image.filename:
        delete_file(article.main_image_url)
        article.main_image_url = save_upload(main_image, "images")

    for img in gallery:
        if img.filename:
            url = save_upload(img, "images")
            db.add(models.ArticleImage(url=url, article_id=article.id))

    db.commit()
    db.refresh(article)
    return article


@app.delete("/articles/{article_id}", tags=["Articles"])
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    """Удалить статью и все её файлы (защищённый)."""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    delete_file(article.preview_image_url)
    delete_file(article.main_image_url)
    for img in article.images:
        delete_file(img.url)

    db.delete(article)
    db.commit()
    return {"detail": "Статья удалена"}


@app.delete("/articles/{article_id}/images/{image_id}", tags=["Articles"])
def delete_article_image(
    article_id: int,
    image_id:   int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    """Удалить одно изображение из галереи статьи."""
    img = db.query(models.ArticleImage).filter(
        models.ArticleImage.id == image_id,
        models.ArticleImage.article_id == article_id,
    ).first()
    if not img:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    delete_file(img.url)
    db.delete(img)
    db.commit()
    return {"detail": "Изображение удалено"}
