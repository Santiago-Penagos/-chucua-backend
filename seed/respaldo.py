import json
from pathlib import Path

from chucua_backend.dominio.geometria_parser import desde_geojson

from .constructores import DOMINIOS, ESPECIFICACIONES

RUTA_DATOS = Path(__file__).resolve().parent / "datos"


def _entidad(dominio: str, feature: dict):
    clase, campos = ESPECIFICACIONES[dominio]
    props = feature.get("properties") or {}
    atributos = {campo: props[campo] for campo in campos}
    return clase(
        nombre=props["nombre"],
        sector=props["sector"],
        geometria=desde_geojson(feature["geometry"]),
        osm_id=props.get("osm_id"),
        **atributos,
    )


def cargar_dominio(dominio: str) -> list:
    ruta = RUTA_DATOS / f"{dominio}.geojson"
    with ruta.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return [_entidad(dominio, feature) for feature in datos["features"]]


def cargar_todo() -> dict[str, list]:
    return {dominio: cargar_dominio(dominio) for dominio in DOMINIOS}
