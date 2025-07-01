from app.db.mongo import db
from app.utils.auth_utils import hash_password, verify_password, create_jwt_token
from app.schemas.user_schema import UserCreate, UserLogin
from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import uuid

router = APIRouter()

@router.post("/client/signup")
async def client_signup(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)
    verification_token = str(uuid.uuid4())
    
    await db.users.insert_one({
        "email": user.email, 
        "password": hashed_pw, 
        "role": "client",
        "verified": False,
        "verification_token": verification_token
    })

    encrypted_url = f"http://127.0.0.1:8009/auth/verify-email/{verification_token}"

    return {
        "message": "Verification email sent", 
        "encrypted_url": encrypted_url,
        "note": "Please check your email for verification (Mock implementation)"
    }

@router.get("/verify-email/{token}")
async def verify_email(token: str):
    user = await db.users.find_one({"verification_token": token})
    if not user:
        raise HTTPException(status_code=404, detail="Invalid verification token")
    
    await db.users.update_one(
        {"verification_token": token},
        {"$set": {"verified": True}, "$unset": {"verification_token": ""}}
    )
    
    return {"message": "Email verified successfully"}

@router.post("/client/login")
async def client_login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not db_user.get("verified", False):
        raise HTTPException(status_code=401, detail="Email not verified")

    token = create_jwt_token(user.email, "client")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/ops/login")
async def ops_login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if db_user.get("role") != "ops":
        raise HTTPException(status_code=403, detail="Access denied. Ops users only.")

    token = create_jwt_token(user.email, "ops")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await db.users.find_one({"email": form_data.username})
    if not db_user or not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    role = db_user.get("role", "client")
    if role == "client" and not db_user.get("verified", False):
        raise HTTPException(status_code=401, detail="Email not verified")
    
    token = create_jwt_token(form_data.username, role)
    return {"access_token": token, "token_type": "bearer"}
