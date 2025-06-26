from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from app.utils.auth_utils import verify_user_type
from app.db.mongo import db
import os
import shutil
from jose import jwt
from datetime import datetime, timedelta
from bson import ObjectId

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"docx", "pptx", "xlsx"}

SECRET_KEY = "secret"
ALGORITHM = "HS256"

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_type: str = Depends(verify_user_type)
):
    if user_type != "ops":
        raise HTTPException(status_code=403, detail="Only Ops can upload files")
    
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = await db.files.insert_one({
        "filename": file.filename,
        "file_type": ext,
        "uploader": "ops",
        "uploaded_at": datetime.utcnow()
    })

    return {"message": "File uploaded successfully", "file_id": str(result.inserted_id)}

@router.get("/list")
async def list_all_files(user_type: str = Depends(verify_user_type)):
    if user_type != "client":
        raise HTTPException(status_code=403, detail="Only clients can list files")
    
    files = []
    async for file in db.files.find():
        files.append({
            "file_id": str(file["_id"]),
            "filename": file["filename"],
            "file_type": file["file_type"],
            "uploader": file["uploader"],
            "uploaded_at": file.get("uploaded_at", "")
        })
    
    return {"files": files, "total_files": len(files)}

@router.get("/download/{file_id}")
async def get_download_link(
    file_id: str,
    user_type: str = Depends(verify_user_type)
):
    if user_type != "client":
        raise HTTPException(status_code=403, detail="Only clients can download files")
    
    token_payload = {
        "file_id": file_id,
        "role": user_type,
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "download_link": f"http://127.0.0.1:8009/file/actual-download/{token}",
        "message": "success"
    }

@router.get("/actual-download/{token}")
async def actual_download(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        file_id = payload.get("file_id")
        role = payload.get("role")

        if role != "client":
            raise HTTPException(status_code=403, detail="Unauthorized")

        file_meta = await db.files.find_one({"_id": ObjectId(file_id)})
        if not file_meta:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = os.path.join(UPLOAD_DIR, file_meta["filename"])
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File missing from server")

        return FileResponse(file_path, filename=file_meta["filename"])

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Download link expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid download token")
