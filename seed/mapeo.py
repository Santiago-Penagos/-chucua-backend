from chucua_backend.dominio.catastro import InformacionCatastral
from chucua_backend.dominio.educativo import CentroEducativo
from chucua_backend.dominio.escenario import EscenarioDeportivo
from chucua_backend.dominio.via import EstadoVia

from .normalizacion import etiquetas, linea, nombre, osm_id, poligono, punto
from .sectores import sector_de_coordenadas

NIVELES = {
    "kindergarten": "preescolar",
    "school": "basica",
    "college": "superior",
    "university": "superior",
}
NATURALEZAS = {"public": "publico", "private": "privado"}


def _sector(geometria) -> str:
    return sector_de_coordenadas(geometria.coordenadas)


def mapear_escenario(elemento: dict) -> EscenarioDeportivo:
    tags = etiquetas(elemento)
    geometria = punto(elemento)
    tipo = tags.get("sport") or tags.get("leisure") or "deportivo"
    return EscenarioDeportivo(
        nombre=nombre(elemento, "Escenario deportivo"),
        sector=_sector(geometria),
        geometria=geometria,
        tipo_escenario=str(tipo).replace("_", " "),
        osm_id=osm_id(elemento),
    )


def mapear_educativo(elemento: dict) -> CentroEducativo:
    tags = etiquetas(elemento)
    geometria = punto(elemento)
    nivel = tags.get("isced:level") or NIVELES.get(tags.get("amenity"), "no_especificado")
    naturaleza = NATURALEZAS.get(tags.get("operator:type"), "no_especificado")
    return CentroEducativo(
        nombre=nombre(elemento, "Centro educativo"),
        sector=_sector(geometria),
        geometria=geometria,
        nivel_educativo=str(nivel),
        naturaleza=naturaleza,
        osm_id=osm_id(elemento),
    )


def mapear_via(elemento: dict) -> EstadoVia:
    tags = etiquetas(elemento)
    geometria = linea(elemento)
    return EstadoVia(
        nombre=nombre(elemento, "Vía"),
        sector=_sector(geometria),
        geometria=geometria,
        tipo_via=tags.get("highway") or "via",
        estado=tags.get("estado") or "sin_evaluar",
        osm_id=osm_id(elemento),
    )


def mapear_catastro(elemento: dict) -> InformacionCatastral:
    tags = etiquetas(elemento)
    geometria = poligono(elemento)
    uso = tags.get("landuse") or ("residencial" if tags.get("building") else "residencial")
    return InformacionCatastral(
        nombre=nombre(elemento, "Predio"),
        sector=_sector(geometria),
        geometria=geometria,
        uso_suelo=str(uso).replace("_", " "),
        area_m2=round(geometria.area_m2(), 2),
        osm_id=osm_id(elemento),
    )


MAPEADORES = {
    "escenarios": mapear_escenario,
    "educativos": mapear_educativo,
    "vias": mapear_via,
    "catastro": mapear_catastro,
}


def mapear(dominio: str, elemento: dict):
    return MAPEADORES[dominio](elemento)
