import argparse
import json

from chucua_backend.db.conexion import conectar
from chucua_backend.errores import ErrorValidacion

from . import overpass, respaldo
from .constructores import DOMINIOS
from .fuentes import DOMINIOS_OVERPASS, crear_repositorios
from .mapeo import mapear

SECTORES = ("I", "II", "III")


def _mapear_elementos(dominio: str, elementos: list[dict]) -> list:
    entidades = []
    for elemento in elementos:
        try:
            entidades.append(mapear(dominio, elemento))
        except (ErrorValidacion, KeyError, TypeError, ValueError):
            continue
    return entidades


def sembrar(
    fuente: str = "auto", conexion=None, usar_red: bool = True, opciones_overpass=None
) -> dict:
    conexion = conexion or conectar()
    repositorios = crear_repositorios(conexion)
    opciones_overpass = opciones_overpass or {}
    detalle_fuente: dict[str, str] = {}
    for dominio in DOMINIOS:
        entidades: list = []
        consulta_red = dominio in DOMINIOS_OVERPASS
        if fuente in ("auto", "overpass") and usar_red and consulta_red:
            elementos = overpass.consultar(dominio, **opciones_overpass)
            entidades = _mapear_elementos(dominio, elementos)
            detalle_fuente[dominio] = "overpass" if entidades else "respaldo"
        if not entidades:
            entidades = respaldo.cargar_dominio(dominio)
            detalle_fuente[dominio] = "respaldo"
        conexion.execute(f"DELETE FROM {repositorios[dominio].tabla} WHERE osm_id IS NOT NULL")
        for entidad in entidades:
            repositorios[dominio].upsert_por_osm_id(entidad)
    return _reporte(fuente, detalle_fuente, repositorios)


def _reporte(fuente: str, detalle: dict[str, str], repositorios: dict) -> dict:
    por_dominio = {dominio: len(repositorios[dominio].listar()) for dominio in DOMINIOS}
    por_sector = {sector: 0 for sector in SECTORES}
    for dominio in DOMINIOS:
        for entidad in repositorios[dominio].listar():
            por_sector[entidad.sector] += 1
    total = sum(por_dominio.values())
    todo_overpass = detalle and all(v == "overpass" for v in detalle.values())
    usada = "overpass" if todo_overpass else "respaldo"
    return {
        "fuente": usada if fuente != "respaldo" else "respaldo",
        "detalle_fuente": detalle,
        "total": total,
        "dominios": por_dominio,
        "sectores": por_sector,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Carga datos del barrio en SQLite")
    parser.add_argument("--fuente", choices=("auto", "overpass", "respaldo"), default="auto")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    argumentos = parser.parse_args(argv)
    reporte = sembrar(fuente=argumentos.fuente)
    if argumentos.json:
        print(json.dumps(reporte, ensure_ascii=False, indent=2))
    else:
        print(f"Fuente: {reporte['fuente']}")
        print(f"Total: {reporte['total']}")
        print(f"Por dominio: {reporte['dominios']}")
        print(f"Por sector: {reporte['sectores']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

