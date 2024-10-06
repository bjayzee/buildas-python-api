from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from .models import User
from dependencies import get_db
from .schema import CreateUser, UserLogin, Token
from ..middleware.authentication import isAuthenticated  

user_router = APIRouter()

@user_router.post('/register')
def register(user_data: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = User(name=user_data.name, username=user_data.username, email=user_data.email)
    user.encode_password(user_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration is successful",
        "success": True,
        "data": {
            "id": str(user.id),
            "username": user.username,
            "name": user.name,
            "email": user.email
        }
    }

@user_router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    if user is None or not user.verify_password(user_data.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')

    token = user.generate_token()

    return Token(access_token=token, token_type="bearer", expires_in=86400)

@user_router.put("/users/{user_id}", dependencies=[Depends(isAuthenticated)])
def update_user(user_id: str, user_data: CreateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    user.username = user_data.username
    user.name = user_data.name
    user.email = user_data.email
    if user_data.password:  
        user.encode_password(user_data.password)

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "success": True,
        "data": {
            "id": str(user.id),
            "username": user.username,
            "name": user.name,
            "email": user.email
        }
    }

@user_router.get('/users/{user_id}', dependencies=[Depends(isAuthenticated)])
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User fetched successfully", "data": {
        "id": str(user.id),
        "username": user.username,
        "name": user.name,
        "email": user.email
    }, "success": True}

@user_router.delete('/users/{user_id}', dependencies=[Depends(isAuthenticated)])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully", "success": True}
