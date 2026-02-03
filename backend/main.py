"""
Inicialização do App e LTI Launch.
Ponto de entrada da aplicação FastAPI.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from backend.config import settings
from backend.database import init_db
from backend.routers import auth_lti, api_gamification, api_dashboard, chatbot
from backend.tasks import start_scheduler

app = FastAPI(title="AvaMJ", version="0.1.0")

# Frontend: templates e arquivos estáticos
BASE_DIR = Path(__file__).resolve().parent.parent
frontend_path = BASE_DIR / "frontend"
app.mount("/static", StaticFiles(directory=frontend_path / "static"), name="static")
templates = Jinja2Templates(directory=frontend_path / "templates")

# Rotas
app.include_router(auth_lti.router, prefix="/auth", tags=["LTI"])
app.include_router(api_gamification.router, prefix="/api/gamification", tags=["Gamificação"])
app.include_router(api_dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])


@app.on_event("startup")
async def startup():
    init_db()  # não derruba o app se o MySQL estiver fora (ex.: tunnel SSH fechado)
    start_scheduler()


@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard_aluno.html", {"request": request})


@app.get("/ranking", response_class=HTMLResponse)
async def ranking(request: Request):
    return templates.TemplateResponse("ranking.html", {"request": request})


@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    return templates.TemplateResponse("chatbot_widget.html", {"request": request})


@app.get("/error", response_class=HTMLResponse)
async def error_page(request: Request):
    return templates.TemplateResponse("error.html", {"request": request})
