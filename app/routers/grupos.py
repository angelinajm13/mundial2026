"""
Router de grupos — equivalente a urls.py + views.py en Django, pero todo junto.
Cada función con @router.get es un endpoint de tu API.
"""
from fastapi import APIRouter, HTTPException, Query
from app.services import worldcup_service

router = APIRouter(prefix="/api/grupos", tags=["Grupos"])


@router.get("/")
async def listar_grupos():
    """Los 12 grupos con tabla de posiciones calculada en tiempo real."""
    return await worldcup_service.listar_grupos_con_standings()


@router.get("/refresh")
async def refrescar_datos():
    """Fuerza la recarga del cache desde GitHub (útil después de que se actualice el JSON)."""
    await worldcup_service.obtener_partidos_raw(forzar_refresh=True)
    await worldcup_service.obtener_grupos_raw(forzar_refresh=True)
    return {"mensaje": "Cache actualizado correctamente"}


@router.get("/{nombre_grupo}")
async def detalle_grupo(nombre_grupo: str):
    """
    Detalle de un grupo específico con su tabla y partidos.
    Ejemplo: /api/grupos/Group A
    """
    grupo = await worldcup_service.obtener_grupo(nombre_grupo)
    if grupo is None:
        raise HTTPException(status_code=404, detail=f"Grupo '{nombre_grupo}' no encontrado")
    return grupo
