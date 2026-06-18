"""
Aquí guardamos TU bracket (qué equipos marcaste como avanzados).
Para mantener el proyecto simple al inicio, lo guardamos en un archivo JSON local
en vez de meter una base de datos todavía. Cuando quieras, esto se reemplaza
fácilmente por SQLAlchemy + SQLite sin tocar el resto del proyecto
(el router solo llama a estas funciones, no le importa cómo se guarda el dato).
"""
import json
from pathlib import Path

ARCHIVO_BRACKET = Path(__file__).parent.parent / "data" / "bracket.json"


def _asegurar_archivo():
    ARCHIVO_BRACKET.parent.mkdir(exist_ok=True)
    if not ARCHIVO_BRACKET.exists():
        ARCHIVO_BRACKET.write_text(json.dumps({"avanzan": {}}, indent=2))


def obtener_bracket() -> dict:
    _asegurar_archivo()
    return json.loads(ARCHIVO_BRACKET.read_text())


def marcar_equipo_avanza(grupo: str, equipo: str, avanza: bool) -> dict:
    """
    Marca si un equipo avanza o no de su grupo, según tu propia predicción
    (no la calcula la API, la decides tú viendo la tabla).
    """
    data = obtener_bracket()
    data["avanzan"].setdefault(grupo, {})
    data["avanzan"][grupo][equipo] = avanza
    ARCHIVO_BRACKET.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return data
