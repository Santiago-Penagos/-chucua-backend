# chucua-backend

Dominio, persistencia SQLite y semilla de datos del barrio **Chucua de la Vaca**
(Localidad de Kennedy, Bogotá). Es la librería que consume `chucua-api`.

## Requisitos

- Python 3.11 o superior.
- Las carpetas `chucua-backend`, `chucua-api` y `chucua-frontend` deben ser
  hermanas dentro de una misma carpeta raíz.

## Instalación

Desde la carpeta raíz que contiene los tres repositorios:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .\chucua-backend
```

## Jerarquía del dominio

```text
EntidadGeografica (ABC)
├── EscenarioDeportivo      Point       + tipo_escenario
├── CentroEducativo         Point       + nivel_educativo, naturaleza
├── EstadoVia               LineString  + tipo_via, estado
└── InformacionCatastral    Polygon     + uso_suelo, area_m2

IRepositorioCRUD[T] (Protocol)
└── RepositorioSQLiteBase[T]
    ├── RepositorioEscenarios
    ├── RepositorioEducativos
    ├── RepositorioVias
    └── RepositorioCatastro

ServicioBase[T] (recibe IRepositorioCRUD[T] por constructor)
├── ServicioEscenarios
├── ServicioEducativos
├── ServicioVias
└── ServicioCatastro
```

Toda entidad tiene `nombre`, `sector` (`"I"`, `"II"` o `"III"`), geometría
GeoJSON con orden **longitud, latitud** y un `osm_id` opcional único.

## Base de datos

La ruta del archivo SQLite se define con la variable de entorno
`CHUCUA_DB_PATH`. Si no se define, se usa `chucua-backend/chucua.db`:

```powershell
$env:CHUCUA_DB_PATH = "C:\datos\chucua.db"
```

El esquema se crea automáticamente en cada conexión:

| Tabla        | Geometría  | Atributos propios                   |
| ------------ | ---------- | ----------------------------------- |
| `escenarios` | Point      | `tipo_escenario`                    |
| `educativos` | Point      | `nivel_educativo`, `naturaleza`     |
| `vias`       | LineString | `tipo_via`, `estado`                |
| `catastro`   | Polygon    | `uso_suelo`, `area_m2`              |

Cada tabla impone `CHECK` de sector, nombre no vacío, geometría no vacía y
área positiva. La geometría se guarda como texto GeoJSON; `mod_spatialite` se
intenta cargar de forma opcional, pero la aplicación funciona sin él.

## Semilla

```powershell
# Intenta Overpass y cae a los GeoJSON locales si no hay red.
.\.venv\Scripts\python.exe -m seed.ejecutar --fuente auto --json

# Fuerza los archivos locales de respaldo.
.\.venv\Scripts\python.exe -m seed.ejecutar --fuente respaldo
```

Se ejecuta desde `chucua-backend`. La siembra es idempotente: usa
`upsert_por_osm_id`, por lo que dos ejecuciones no duplican registros. El
reporte muestra totales por dominio y por sector.

Los datos de respaldo están en `seed/datos/*.geojson` (24 registros, 8 por
sector) y llevan la atribución correspondiente a OpenStreetMap.

### Ejecución registrada

Ejecución real del **16 de noviembre de 2026** con `--fuente auto`: Overpass
respondió para los cuatro dominios y se cargaron 384 registros.

| Dominio      | Registros |
| ------------ | --------- |
| `escenarios` | 27        |
| `educativos` | 1         |
| `vias`       | 300       |
| `catastro`   | 56        |

Distribución por sector: I = 147, II = 117, III = 120. Una segunda ejecución
mantuvo exactamente los mismos conteos (upsert idempotente).


## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest
```

`pyproject.toml` incluye `tests` y `../chucua-api/tests` en `testpaths`, así
que este comando ejecuta la suite completa (backend + API). La prueba
`tests/test_limite_lineas.py` falla si algún archivo `.py`, `.js`, `.html` o
`.css` de los tres repositorios supera las 100 líneas.

## Atribución

Los datos de origen OSM se distribuyen bajo la licencia **ODbL 1.0** de
OpenStreetMap. Atribución: *© OpenStreetMap contributors*.
Consulta: https://www.openstreetmap.org/copyright
