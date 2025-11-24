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
# Замените данные ниже на свои настройки MySQL
DATABASE_URL = "mysql+mysqlconnector://root:password@localhost/museum_db"

SECRET_KEY = "YOUR_SUPER_SECRET_KEY_FOR_JWT"  # Поменяй на длинную случайную строку
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Настройка путей для сохранения файлов
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
    USER = "user"  # Обычный пользователь (для расширения)


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
    image_url = Column(String(255))
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class Exhibit(Base):
    __tablename__ = "exhibits"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    photo_url = Column(String(255))
    model_url = Column(String(255))
    author_id = Column(Integer, ForeignKey("users.id"))
    # Если экспедиция не выбрана, поле может быть пустым
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)

# --- SECURITY & AUTH HELPERS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.login == login).first()
    if user is None:
        raise credentials_exception
    return user


# --- PYDANTIC SCHEMAS ---
class UserCreate(BaseModel):
    login: str
    password: str
    role: UserRole


class UserOut(BaseModel):
    id: int
    login: str
    role: UserRole

    class Config:
        orm_mode = True


class ExhibitOut(BaseModel):
    id: int
    title: str
    description: str
    photo_url: str
    model_url: str
    created_at: datetime

    class Config:
        orm_mode = True


# --- APP INIT ---
app = FastAPI(title="Museum API")

# CORS (Разрешаем запросы с фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки можно *, в проде лучше конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статики (доступ к картинкам и моделям по URL)
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- ENDPOINTS ---

# 1. Auth
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect login or password")

    access_token = create_access_token(data={"sub": user.login, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role.value}


# 2. Создание пользователей (Только Админ)
@app.post("/users/", response_model=UserOut)
def create_moderator(user: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only Admins can add users")

    # Проверка, существует ли такой логин
    if db.query(User).filter(User.login == user.login).first():
        raise HTTPException(status_code=400, detail="Login already registered")

    new_user = User(
        login=user.login,
        password_hash=get_password_hash(user.password),
        role=user.role  # Админ может создать и админа, и модератора
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Инициализация первого Админа (ручка-хелпер, чтобы создать первого юзера)
@app.get("/init-admin")
def init_admin(db: Session = Depends(get_db)):
    if db.query(User).filter(User.role == UserRole.ADMIN).first():
        return {"message": "Admin already exists"}

    admin = User(
        login="admin",
        password_hash=get_password_hash("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    return {"message": "Admin user created: login=admin, pass=admin123"}


# 3. Экспонаты (Общедоступно - чтение)
@app.get("/exhibits", response_model=List[ExhibitOut])
def get_exhibits(db: Session = Depends(get_db)):
    return db.query(Exhibit).all()


@app.get("/exhibits/{exhibit_id}", response_model=ExhibitOut)
def get_exhibit(exhibit_id: int, db: Session = Depends(get_db)):
    exhibit = db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()
    if not exhibit:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return exhibit


# 4. Добавление Экспоната (Админ и Модератор)
@app.post("/exhibits/")
async def create_exhibit(
        title: str = Form(...),
        description: str = Form(...),
        photo: UploadFile = File(...),
        model: UploadFile = File(...),
        article_id: Optional[int] = Form(None),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Сохраняем фото
    photo_filename = f"{datetime.now().timestamp()}_{photo.filename}"
    photo_path = os.path.join(IMG_DIR, photo_filename)
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # Сохраняем модель
    model_filename = f"{datetime.now().timestamp()}_{model.filename}"
    model_path = os.path.join(MODEL_DIR, model_filename)
    with open(model_path, "wb") as buffer:
        shutil.copyfileobj(model.file, buffer)

    # URL для фронтенда (относительный путь)
    photo_url_db = f"/static/images/{photo_filename}"
    model_url_db = f"/static/models/{model_filename}"

    new_exhibit = Exhibit(
        title=title,
        description=description,
        photo_url=photo_url_db,
        model_url=model_url_db,
        author_id=current_user.id,
        article_id=article_id
    )
    db.add(new_exhibit)
    db.commit()
    db.refresh(new_exhibit)
    return new_exhibit