from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .models import User
from .utils import verify_password, create_access_token, verify_access_token
from .schemas import UserCreate
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def login(db: Session, user: UserCreate):
    authenticated_user = authenticate_user(db=db, email=user.email, password=user.password)
    access_token = create_access_token(data={"sub": authenticated_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.email == payload["sub"]).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
