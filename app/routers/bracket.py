"""
Router del bracket eliminatorio.
"""
from fastapi import APIRouter
from app.services import worldcup_service

router = APIRouter(prefix="/api/bracket", tags=["Bracket"])

RONDAS_GRUPOS = {
    "Matchday 1", "Matchday 2", "Matchday 3", "Matchday 4",
    "Matchday 5", "Matchday 6", "Matchday 7", "Matchday 8",
    "Matchday 9", "Matchday 10", "Matchday 11", "Matchday 12",
    "Matchday 13", "Matchday 14", "Matchday 15", "Matchday 16",
    "Matchday 17",
}

ORDEN_RONDAS = [
    "Round of 32",
    "Round of 16",
    "Quarter-final",
    "Semi-final",
    "Match for third place",
    "Final",
]

@router.get("/")
async def obtener_bracket():
    """
    Regresa los partidos eliminatorios agrupados por ronda,
    en el orden correcto del bracket.
    """
    todos = await worldcup_service.listar_partidos()
    eliminatorios = [p for p in todos if p.round not in RONDAS_GRUPOS]

    bracket = {}
    for p in eliminatorios:
        bracket.setdefault(p.round, []).append(p)

    # Ordenar por el orden oficial del torneo
    resultado = []
    for ronda in ORDEN_RONDAS:
        if ronda in bracket:
            partidos = sorted(bracket[ronda], key=lambda p: p.date)
            resultado.append({"ronda": ronda, "partidos": partidos})

    return resultado
