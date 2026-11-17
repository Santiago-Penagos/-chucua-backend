from chucua_backend.dominio.catastro import InformacionCatastral
from chucua_backend.dominio.educativo import CentroEducativo
from chucua_backend.dominio.escenario import EscenarioDeportivo
from chucua_backend.dominio.geometria import Linea, Poligono, Punto
from chucua_backend.dominio.via import EstadoVia


def escenario(nombre="Cancha Central", sector="I", tipo_escenario="cancha", osm_id=None):
    return EscenarioDeportivo(
        nombre=nombre,
        sector=sector,
        geometria=Punto((-74.1685, 4.6285)),
        tipo_escenario=tipo_escenario,
        osm_id=osm_id,
    )


def educativo(nombre="Colegio Central", sector="II", osm_id=None):
    return CentroEducativo(
        nombre=nombre,
        sector=sector,
        geometria=Punto((-74.1645, 4.629)),
        nivel_educativo="basica",
        naturaleza="publico",
        osm_id=osm_id,
    )


def via(nombre="Carrera 80", sector="III", osm_id=None):
    return EstadoVia(
        nombre=nombre,
        sector=sector,
        geometria=Linea(((-74.162, 4.627), (-74.161, 4.6275), (-74.160, 4.628))),
        tipo_via="residential",
        estado="regular",
        osm_id=osm_id,
    )


def catastro(nombre="Predio Central", sector="I", osm_id=None):
    return InformacionCatastral(
        nombre=nombre,
        sector=sector,
        geometria=Poligono(
            ((-74.169, 4.625), (-74.1684, 4.625), (-74.1684, 4.6256), (-74.169, 4.6256))
        ),
        uso_suelo="residencial",
        area_m2=1200,
        osm_id=osm_id,
    )


FABRICAS = {
    "escenarios": escenario,
    "educativos": educativo,
    "vias": via,
    "catastro": catastro,
}
