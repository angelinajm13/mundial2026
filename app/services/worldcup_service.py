"""
Servicio principal — consume el feed de openfootball y calcula standings.
httpx es como 'requests' pero soporta async/await nativamente (ideal para FastAPI).
"""
import httpx
from app.models.schemas import Partido, Gol, EquipoStanding, Grupo

BASE_URL = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026"

# Cache simple en memoria — evita llamar a GitHub en cada request del usuario.
# Para un proyecto de práctica es suficiente.
_cache: dict = {"partidos": None, "grupos_raw": None}


async def _fetch_json(url: str) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def obtener_partidos_raw(forzar_refresh: bool = False) -> list[dict]:
    if _cache["partidos"] is None or forzar_refresh:
        data = await _fetch_json(f"{BASE_URL}/worldcup.json")
        _cache["partidos"] = data["matches"]
    return _cache["partidos"]


async def obtener_grupos_raw(forzar_refresh: bool = False) -> list[dict]:
    if _cache["grupos_raw"] is None or forzar_refresh:
        data = await _fetch_json(f"{BASE_URL}/worldcup.groups.json")
        _cache["grupos_raw"] = data["groups"]
    return _cache["grupos_raw"]


def _convertir_partido(raw: dict) -> Partido:
    score = raw.get("score")
    jugado = score is not None

    return Partido(
        round=raw["round"],
        date=raw["date"],
        time=raw["time"],
        team1=raw["team1"],
        team2=raw["team2"],
        group=raw.get("group"),
        ground=raw.get("ground"),
        goles_local=score["ft"][0] if jugado else None,
        goles_visitante=score["ft"][1] if jugado else None,
        goleadores_local=[Gol(**g) for g in raw.get("goals1", [])],
        goleadores_visitante=[Gol(**g) for g in raw.get("goals2", [])],
        jugado=jugado,
    )


async def listar_partidos(round_filtro: str | None = None) -> list[Partido]:
    raw = await obtener_partidos_raw()
    partidos = [_convertir_partido(p) for p in raw]
    if round_filtro:
        partidos = [p for p in partidos if round_filtro.lower() in p.round.lower()]
    return partidos


def _calcular_standing(nombre_grupo: str, equipos: list[str], partidos: list[Partido]) -> Grupo:
    tabla = {nombre: EquipoStanding(nombre=nombre) for nombre in equipos}
    partidos_del_grupo = [p for p in partidos if p.group == nombre_grupo and p.jugado]

    for p in partidos_del_grupo:
        local, visit = p.team1, p.team2
        gl, gv = p.goles_local, p.goles_visitante

        if local not in tabla or visit not in tabla:
            continue

        tabla[local].jugados += 1
        tabla[visit].jugados += 1
        tabla[local].goles_favor += gl
        tabla[local].goles_contra += gv
        tabla[visit].goles_favor += gv
        tabla[visit].goles_contra += gl

        if gl > gv:
            tabla[local].ganados += 1
            tabla[local].puntos += 3
            tabla[visit].perdidos += 1
        elif gl < gv:
            tabla[visit].ganados += 1
            tabla[visit].puntos += 3
            tabla[local].perdidos += 1
        else:
            tabla[local].empatados += 1
            tabla[visit].empatados += 1
            tabla[local].puntos += 1
            tabla[visit].puntos += 1

    for e in tabla.values():
        e.diferencia = e.goles_favor - e.goles_contra

    ordenados = sorted(
        tabla.values(),
        key=lambda e: (e.puntos, e.diferencia, e.goles_favor),
        reverse=True,
    )
    return Grupo(nombre=nombre_grupo, equipos=ordenados, partidos=partidos_del_grupo)


async def listar_grupos_con_standings() -> list[Grupo]:
    grupos_raw = await obtener_grupos_raw()
    todos = await listar_partidos()
    return [_calcular_standing(g["name"], g["teams"], todos) for g in grupos_raw]


async def obtener_grupo(nombre_grupo: str) -> Grupo | None:
    grupos = await listar_grupos_con_standings()
    for g in grupos:
        if g.nombre.lower() == nombre_grupo.lower():
            return g
    return None
