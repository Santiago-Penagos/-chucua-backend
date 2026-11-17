from chucua_backend.dominio.geometria import Coordenada, Linea, Poligono, Punto
from chucua_backend.errores import ErrorValidacion


def osm_id(elemento: dict) -> str:
    return f"{elemento.get('type', 'node')}/{elemento['id']}"


def etiquetas(elemento: dict) -> dict:
    return elemento.get("tags") or {}


def nombre(elemento: dict, defecto: str) -> str:
    valor = etiquetas(elemento).get("name")
    if isinstance(valor, str) and valor.strip():
        return valor.strip()
    return f"{defecto} {osm_id(elemento)}"


def punto(elemento: dict) -> Punto:
    if "lat" in elemento and "lon" in elemento:
        return Punto((float(elemento["lon"]), float(elemento["lat"])))
    centro = elemento.get("center") or {}
    if "lat" in centro and "lon" in centro:
        return Punto((float(centro["lon"]), float(centro["lat"])))
    geometria = elemento.get("geometry") or []
    if geometria:
        return Punto((float(geometria[0]["lon"]), float(geometria[0]["lat"])))
    raise ErrorValidacion(f"Elemento {osm_id(elemento)} sin coordenadas")


def linea(elemento: dict) -> Linea:
    puntos = [(float(p["lon"]), float(p["lat"])) for p in elemento.get("geometry") or []]
    return Linea(tuple(puntos))


def poligono(elemento: dict) -> Poligono:
    puntos = [(float(p["lon"]), float(p["lat"])) for p in elemento.get("geometry") or []]
    return Poligono(tuple(puntos))


def coordenadas_de(geometria) -> list[Coordenada]:
    return geometria.coordenadas
