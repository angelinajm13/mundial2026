"""
Router de partidos — para consultar fixtures por ronda.
"""
from fastapi import APIRouter, Query
from app.services import worldcup_service

router = APIRouter(prefix="/api/partidos", tags=["Partidos"])


@router.get("/")
async def listar_partidos(ronda: str | None = Query(default=None, description="Filtra por ronda, ej: 'Matchday 1', 'Round of 32'")):
    """
    Lista todos los partidos. 
    Con ?ronda=Matchday+1 filtra por jornada específica.
    Con ?ronda=Round+of+32 muestra los de octavos, etc.
    """
    return await worldcup_service.listar_partidos(round_filtro=ronda)
