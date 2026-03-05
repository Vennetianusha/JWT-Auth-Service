from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.user_schema import UserRegister, UserLogin
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# REGISTER USER
@router.post("/register", status_code=201)
def register_user(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "message": "User registered successfully"
    }


# LOGIN USER
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(db_user.username)

    refresh_token = create_refresh_token()

    expires = datetime.utcnow() + timedelta(days=7)

    db_token = RefreshToken(
        user_id=db_user.id,
        token=refresh_token,
        expires_at=expires
    )

    db.add(db_token)
    db.commit()

    return {
        "token_type": "Bearer",
        "access_token": access_token,
        "expires_in": 900,
        "refresh_token": refresh_token
    }


# REFRESH TOKEN
@router.post("/refresh")
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):

    token_record = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user = db.query(User).filter(User.id == token_record.user_id).first()

    new_access_token = create_access_token(user.username)

    return {
        "token_type": "Bearer",
        "access_token": new_access_token,
        "expires_in": 900
    }


# LOGOUT
@router.post("/logout", status_code=204)
def logout_user(refresh_token: str, db: Session = Depends(get_db)):

    token_record = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if token_record:
        db.delete(token_record)
        db.commit()