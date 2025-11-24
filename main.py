import os
import shutil
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum

from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from passlib.context import CryptContext
from jose import JWTError, jwt

# --- КОНФИГУРАЦИЯ ---
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/museum_db"
SECRET_KEY = "HYPERBOREA_FOREVERT"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

UPLOAD_DIR = "static"
IMG_DIR = os.path.join(UPLOAD_DIR, "images")
MODEL_DIR = os.path.join(UPLOAD_DIR, "models")
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# --- DATABASE SETUP ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- MODELS (SQLAlchemy) ---
class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow)


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text)
    preview_image_url = Column(String(255))  # Фото на карточке
    main_image_url = Column(String(255))  # Фото в начале статьи
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User")
    images = relationship("ArticleImage", back_populates="article", cascade="all, delete-orphan")


class ArticleImage(Base):
    __tablename__ = "article_images"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    article_id = Column(Integer, ForeignKey("articles.id"))
    article = relationship("Article", back_populates="images")


class Exhibit(Base):
    __tablename__ = "exhibits"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    photo_url = Column(String(255))  # Главное фото (превью)
    model_url = Column(String(255))  # 3D модель
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User")
    images = relationship("ExhibitImage", back_populates="exhibit", cascade="all, delete-orphan")


class ExhibitImage(Base):
    __tablename__ = "exhibit_images"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    exhibit_id = Column(Integer, ForeignKey("exhibits.id"))
    exhibit = relationship("Exhibit", back_populates="images")


Base.metadata.create_all(bind=engine)

# --- SECURITY & UTILS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain, hashed): return pwd_context.verify(plain, hashed)


def get_password_hash(password): return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None: raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)
    user = db.query(User).filter(User.login == login).first()
    if user is None: raise HTTPException(status_code=401)
    return user


def save_file(file: UploadFile, folder: str) -> str:
    filename = f"{datetime.now().timestamp()}_{file.filename}"
    path = os.path.join(folder, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Возвращаем URL относительно корня сайта
    return f"/static/{os.path.basename(folder)}/{filename}"


# --- PYDANTIC SCHEMAS ---
class UserCreate(BaseModel):
    login: str
    password: str
    role: UserRole


class ImageOut(BaseModel):
    url: str

    class Config: from_attributes = True


class ExhibitOut(BaseModel):
    id: int
    title: str
    description: str
    photo_url: str
    model_url: str
    created_at: datetime
    images: List[ImageOut] = []

    class Config: from_attributes = True


class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    preview_image_url: str
    main_image_url: str
    created_at: datetime
    author_id: int
    images: List[ImageOut] = []

    class Config: from_attributes = True


# --- API ---
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")


# AUTH
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Error")
    return {"access_token": create_access_token({"sub": user.login, "role": user.role.value}), "token_type": "bearer",
            "role": user.role.value}


@app.get("/init-admin")
def init_admin(db: Session = Depends(get_db)):
    if not db.query(User).filter(User.role == UserRole.ADMIN).first():
        db.add(User(login="admin", password_hash=get_password_hash("admin123"), role=UserRole.ADMIN))
        db.commit()
        return {"message": "Admin created"}
    return {"message": "Admin exists"}


@app.post("/users/")
def create_user(user: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN: raise HTTPException(403)
    if db.query(User).filter(User.login == user.login).first(): raise HTTPException(400, "Exists")
    db.add(User(login=user.login, password_hash=get_password_hash(user.password), role=user.role))
    db.commit()
    return {"msg": "Created"}


# --- EXHIBITS CRUD ---
@app.get("/exhibits", response_model=List[ExhibitOut])
def get_exhibits(db: Session = Depends(get_db)):
    return db.query(Exhibit).all()


@app.get("/exhibits/{id}", response_model=ExhibitOut)
def get_exhibit(id: int, db: Session = Depends(get_db)):
    ex = db.query(Exhibit).filter(Exhibit.id == id).first()
    if not ex: raise HTTPException(404)
    return ex


@app.post("/exhibits/")
async def create_exhibit(
        title: str = Form(...), description: str = Form(...),
        photo: UploadFile = File(...), model: UploadFile = File(...),
        gallery: List[UploadFile] = File(default=[]),
        user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    new_ex = Exhibit(
        title=title, description=description,
        photo_url=save_file(photo, IMG_DIR),
        model_url=save_file(model, MODEL_DIR),
        author_id=user.id
    )
    db.add(new_ex)
    db.commit()
    db.refresh(new_ex)

    # Save gallery images
    for img in gallery:
        if img.filename:
            db.add(ExhibitImage(url=save_file(img, IMG_DIR), exhibit_id=new_ex.id))
    db.commit()
    return new_ex


@app.delete("/exhibits/{id}")
def delete_exhibit(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ex = db.query(Exhibit).filter(Exhibit.id == id).first()
    if not ex: raise HTTPException(404)
    db.delete(ex)
    db.commit()
    return {"msg": "Deleted"}


@app.put("/exhibits/{id}")
def update_exhibit(id: int, title: str = Form(...), description: str = Form(...),
                   user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ex = db.query(Exhibit).filter(Exhibit.id == id).first()
    if not ex: raise HTTPException(404)
    ex.title = title
    ex.description = description
    db.commit()
    return {"msg": "Updated"}


# --- ARTICLES CRUD ---
@app.get("/articles", response_model=List[ArticleOut])
def get_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()


@app.get("/articles/{id}", response_model=ArticleOut)
def get_article(id: int, db: Session = Depends(get_db)):
    art = db.query(Article).filter(Article.id == id).first()
    if not art: raise HTTPException(404)
    return art


@app.post("/articles/")
async def create_article(
        title: str = Form(...), content: str = Form(...),
        preview: UploadFile = File(...), main_img: UploadFile = File(...),
        gallery: List[UploadFile] = File(default=[]),
        user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    new_art = Article(
        title=title, content=content,
        preview_image_url=save_file(preview, IMG_DIR),
        main_image_url=save_file(main_img, IMG_DIR),
        author_id=user.id
    )
    db.add(new_art)
    db.commit()
    db.refresh(new_art)

    for img in gallery:
        if img.filename:
            db.add(ArticleImage(url=save_file(img, IMG_DIR), article_id=new_art.id))
    db.commit()
    return new_art


@app.delete("/articles/{id}")
def delete_article(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    art = db.query(Article).filter(Article.id == id).first()
    if not art: raise HTTPException(404)
    db.delete(art)
    db.commit()
    return {"msg": "Deleted"}


@app.put("/articles/{id}")
def update_article(id: int, title: str = Form(...), content: str = Form(...),
                   user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    art = db.query(Article).filter(Article.id == id).first()
    if not art: raise HTTPException(404)
    art.title = title
    art.content = content
    db.commit()
    return {"msg": "Updated"}