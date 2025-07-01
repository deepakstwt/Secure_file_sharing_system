from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.routes import auth_routes, file_routes
import os

app = FastAPI(title="Secure File Sharing System")


os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/web", response_class=HTMLResponse)
async def web_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/")
def api_root():
    return {"message": "Welcome to the Secure File Sharing API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(file_routes.router, prefix="/file")
