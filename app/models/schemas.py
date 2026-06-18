from pydantic import BaseModel
from typing import Optional, List


class Gol(BaseModel):
    name: str
    minute: str
    penalty: bool = False
    owngoal: bool = False


class Partido(BaseModel):
    round: str
    date: str
    time: str
    team1: str
    team2: str
    group: Optional[str] = None
    ground: Optional[str] = None
    goles_local: Optional[int] = None
    goles_visitante: Optional[int] = None
    goleadores_local: List[Gol] = []
    goleadores_visitante: List[Gol] = []
    jugado: bool = False


class EquipoStanding(BaseModel):
    nombre: str
    jugados: int = 0
    ganados: int = 0
    empatados: int = 0
    perdidos: int = 0
    goles_favor: int = 0
    goles_contra: int = 0
    puntos: int = 0
    diferencia: int = 0


class Grupo(BaseModel):
    nombre: str
    equipos: List[EquipoStanding]
    partidos: List[Partido] = []


class Equipo(BaseModel):
    nombre: str
    grupo: str
    avanza: Optional[bool] = None