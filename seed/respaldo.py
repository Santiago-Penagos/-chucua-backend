import json
from pathlib import Path

from chucua_backend.dominio.catastro import InformacionCatastral
from chucua_backend.dominio.educativo import CentroEducativo
from chucua_backend.dominio.escenario import EscenarioDeportivo
from chucua_backend.dominio.geometria_parser import desde_geojson
from chucua_backend.dominio.via import EstadoVia

RUTA_DATOS = Path(__file__).resolve().parent / "datos"


def _entidad(dominio: str, feature: dict):
    props = feature.get("properties") or {}
    base = {
        "nombre": props["nombre"],
        "sector": props["sector"],
        "geometria": desde_geojson(feature["geometry"]),
        "osm_id": props.get("osm_id"),
    }
    if dominio == "escenarios":
        return EscenarioDeportivo(**base, tipo_escenario=props["tipo_escenario"])
    if dominio == "educativos":
        return CentroEducativo(
            **base,
            nivel_educativo=props["nivel_educativo"],
            naturaleza=props["naturaleza"],
        )
    if dominio == "vias":
        return EstadoVia(**base, tipo_via=props["tipo_via"], estado=props["estado"])
    return InformacionCatastral(
        **base, uso_suelo=props["uso_suelo"], area_m2=props["area_m2"]
    )


def cargar_dominio(dominio: str) -> list:
    ruta = RUTA_DATOS / f"{dominio}.geojson"
    with ruta.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return [_entidad(dominio, feature) for feature in datos["features"]]


def cargar_todo() -> dict[str, list]:
    return {
        dominio: cargar_dominio(dominio)
        for dominio in ("escenarios", "educativos", "vias", "catastro")
    }
