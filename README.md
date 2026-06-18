# 🏆 Mundial 2026 Tracker

Proyecto de práctica con **FastAPI** + **Tailwind CSS** para seguir el Mundial FIFA 2026 en vivo.

## Stack
- **Backend:** FastAPI + httpx + Pydantic
- **Frontend:** HTML + Tailwind CSS (CDN) + JS vanilla
- **Datos:** openfootball/worldcup.json (actualiza ~1 vez al día, gratis, sin API key)

## Estructura
```
mundial2026/
├── main.py                      # Punto de entrada (como wsgi.py en Django)
├── requirements.txt
├── app/
│   ├── models/
│   │   └── schemas.py           # Modelos Pydantic (como Serializers en DRF)
│   ├── services/
│   │   └── worldcup_service.py  # Lógica de negocio + consumo de API externa
│   └── routers/
│       ├── grupos.py            # Endpoints de grupos (como urls.py + views.py)
│       └── partidos.py          # Endpoints de partidos
└── frontend/
    └── index.html               # UI con Tailwind CSS
```

## Instalación y uso

```bash
# 1. Crear entorno virtual (buena práctica)
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Correr el servidor
uvicorn main:app --reload
```

Abre tu navegador en:
- **http://127.0.0.1:8000** → Frontend con los grupos
- **http://127.0.0.1:8000/docs** → Documentación automática (¡Swagger gratis!)
- **http://127.0.0.1:8000/redoc** → Documentación alternativa

## Endpoints disponibles
| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/grupos/` | Los 12 grupos con standings |
| GET | `/api/grupos/Group A` | Detalle de un grupo |
| GET | `/api/grupos/refresh` | Fuerza actualización del cache |
| GET | `/api/partidos/` | Todos los partidos |
| GET | `/api/partidos/?ronda=Matchday 1` | Partidos de una jornada |
| GET | `/api/partidos/?ronda=Round of 32` | Partidos de octavos |

## Próximos pasos sugeridos
- [ ] Agregar página de bracket para eliminatorias
- [ ] Guardar tus predicciones (SQLite + SQLAlchemy)
- [ ] Mostrar goleadores en cada partido
- [ ] Página de próximos partidos del día
