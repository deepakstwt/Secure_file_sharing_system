from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Secret and algorithm
SECRET_KEY = "secret"  # ⚠️ Move to .env in real apps
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 2

# Token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ Create JWT token with expiry
def create_jwt_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": email,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ✅ Hash the password securely
def hash_password(password: str):
    return pwd_context.hash(password)


# ✅ Verify provided password with hashed one
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ✅ Decode JWT and return user type
def verify_user_type(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # 👉 Temp logic: determine role based on email
        if "ops" in email:
            return "ops"
        else:
            return "client"

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
