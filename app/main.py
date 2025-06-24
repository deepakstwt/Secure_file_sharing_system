from fastapi import FastAPI
from app.routes import auth_routes, file_routes

app = FastAPI(title="Secure File Sharing System")

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(file_routes.router, prefix="/file")

@app.get("/")
def root():
    return {"message": "Welcome to the Secure File Sharing API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
