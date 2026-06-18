from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import grupos, partidos, bracket

app = FastAPI(
    title="Mundial 2026 API",
    description="Tracker del Mundial FIFA 2026",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grupos.router)
app.include_router(partidos.router)
app.include_router(bracket.router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
