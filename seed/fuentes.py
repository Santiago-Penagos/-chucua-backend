from chucua_backend.repositorios import (
    RepositorioCatastro,
    RepositorioCentrosSalud,
    RepositorioComercio,
    RepositorioCultura,
    RepositorioDemografia,
    RepositorioEducativos,
    RepositorioEscenarios,
    RepositorioHumedalPuntos,
    RepositorioJac,
    RepositorioSeguridad,
    RepositorioServiciosPublicos,
    RepositorioTransporte,
    RepositorioVias,
    RepositorioZonasVerdes,
)

from .constructores import DOMINIOS

DOMINIOS_OVERPASS = ("escenarios", "educativos", "vias", "catastro")

CLASES = {
    "escenarios": RepositorioEscenarios,
    "educativos": RepositorioEducativos,
    "vias": RepositorioVias,
    "catastro": RepositorioCatastro,
    "jac": RepositorioJac,
    "centros_salud": RepositorioCentrosSalud,
    "seguridad": RepositorioSeguridad,
    "humedal_puntos": RepositorioHumedalPuntos,
    "transporte": RepositorioTransporte,
    "comercio": RepositorioComercio,
    "cultura": RepositorioCultura,
    "servicios_publicos": RepositorioServiciosPublicos,
    "zonas_verdes": RepositorioZonasVerdes,
    "demografia": RepositorioDemografia,
}


def crear_repositorios(conexion) -> dict:
    return {dominio: CLASES[dominio](conexion) for dominio in DOMINIOS}
