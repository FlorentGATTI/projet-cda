from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from bson import ObjectId
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration MongoDB
async def connect_to_mongodb():
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client['cda']
        
        return db
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {str(e)}")
        raise

# Configurer le contexte pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clé secrète pour les JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer pour extraire le token des requêtes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Modèle de données pour l'utilisateur
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str
    is_admin: bool = False

class UserInDB(User):
    id: Optional[str] = Field(alias="_id")

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Fonction pour hacher le mot de passe
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Fonction pour vérifier le mot de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Fonction pour créer un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await connect_to_mongodb()
    
    logger.info("Checking for default admin user...")
    admin = await db.users.find_one({"username": "admin"})
    
    if not admin:
        try:
            logger.info("Admin user not found. Creating default admin user...")
            hashed_password = hash_password("adminpassword")
            result = await db.users.insert_one({
                "username": "admin",
                "email": "admin@example.com",
                "hashed_password": hashed_password,
                "is_admin": True
            })
            if result.inserted_id:
                logger.info(f"Admin user created with ID: {result.inserted_id}")
            else:
                logger.error("Failed to create admin user.")
        except Exception as e:
            logger.error(f"Error creating admin user: {str(e)}")
    else:
        logger.info("Admin user already exists.")
    
    yield  # Continue with the lifespan context

app = FastAPI(lifespan=lifespan)

# Fonction pour obtenir un utilisateur par nom d'utilisateur
async def get_user(username: str):
    user = await db.users.find_one({"username": username})
    if user:
        return UserInDB(**user)

# Authentification et récupération de l'utilisateur actuel
async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Récupération de l'utilisateur courant à partir du token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Route pour s'inscrire
@app.post("/register")
async def register(user: UserCreate):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    hashed_password = hash_password(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    user_dict.pop("password")
    user_dict.pop("confirm_password")
    user_dict["is_admin"] = False

    await db.users.insert_one(user_dict)
    return {"msg": "User created successfully"}

# Route pour se connecter
@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Route protégée (exemple)
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Pour protéger les routes
def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/test-insert")
async def test_insert_user():
    db = await connect_to_mongodb()
    user = {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": hash_password("testpassword"),
        "is_admin": False
    }
    result = await db.users.insert_one(user)
    return {"inserted_id": str(result.inserted_id)}
