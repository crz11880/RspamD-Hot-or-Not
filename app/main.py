from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text

from app.config import settings
from app.db import init_db, get_db, SessionLocal, engine
from app.routes import auth, messages, dashboard, settings as settings_routes, admin
from app.services.auth_service import AuthService
from app.models.user import User as UserModel

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title=settings.APP_TITLE, debug=settings.DEBUG)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


def ensure_user_schema():
    with engine.begin() as conn:
        inspector = inspect(conn)
        if not inspector.has_table("users"):
            return

        columns = [column["name"] for column in inspector.get_columns("users")]
        if "must_change_credentials" not in columns:
            conn.execute(
                text("ALTER TABLE users ADD COLUMN must_change_credentials BOOLEAN NOT NULL DEFAULT 1")
            )

@app.on_event("startup")
def startup_event():
    init_db()
    ensure_user_schema()
    db = SessionLocal()
    
    admin_user = db.query(UserModel).filter(
        UserModel.username == settings.ADMIN_USERNAME
    ).first()
    
    if not admin_user:
        AuthService.create_user(
            db=db,
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD
        )
        print(f"Created admin user: {settings.ADMIN_USERNAME}")
    
    db.close()

app.include_router(auth.router)
app.include_router(messages.router)
app.include_router(dashboard.router)
app.include_router(settings_routes.router)
app.include_router(admin.router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/first-login", response_class=HTMLResponse)
async def first_login_page(request: Request):
    return templates.TemplateResponse("first_login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/review", response_class=HTMLResponse)
async def review_page(request: Request):
    return templates.TemplateResponse("review.html", {"request": request})

@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
