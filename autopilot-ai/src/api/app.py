"""FastAPI Application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.api.websocket import ws_router

def create_app(model: str = "gpt-4o") -> FastAPI:
    app = FastAPI(title="AutoPilot AI", version="1.0.0")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.state.model = model
    app.include_router(router, prefix="/api/v1")
    app.include_router(ws_router)
    return app
