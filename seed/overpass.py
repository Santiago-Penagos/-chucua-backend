import json
import time
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

URL = "https://overpass-api.de/api/interpreter"
BBOX = (4.6238, -74.1695, 4.6318, -74.1615)

CONSULTAS = {
    "escenarios": (
        "[out:json][timeout:{timeout}];"
        "(nwr[\"leisure\"=\"pitch\"]({bbox});"
        "nwr[\"leisure\"=\"sports_centre\"]({bbox});"
        "nwr[\"sport\"]({bbox}););out body geom;"
    ),
    "educativos": (
        "[out:json][timeout:{timeout}];"
        "(nwr[\"amenity\"=\"school\"]({bbox});"
        "nwr[\"amenity\"=\"kindergarten\"]({bbox});"
        "nwr[\"amenity\"=\"college\"]({bbox});"
        "nwr[\"amenity\"=\"university\"]({bbox}););out body geom;"
    ),
    "vias": (
        "[out:json][timeout:{timeout}];"
        "way[\"highway\"~\"^(motorway|trunk|primary|secondary|tertiary|"
        "residential|unclassified|living_street|pedestrian|footway|cycleway)$\"]"
        "({bbox});out body geom 300;"
    ),
    "catastro": (
        "[out:json][timeout:{timeout}];"
        "way[\"building\"]({bbox});out body geom 200;"
    ),
}


def caja(bbox: tuple[float, float, float, float] = BBOX) -> str:
    return ",".join(str(valor) for valor in bbox)


def construir_consulta(
    dominio: str, bbox: tuple[float, float, float, float] = BBOX, timeout: int = 60
) -> str:
    return CONSULTAS[dominio].format(bbox=caja(bbox), timeout=timeout)


def _pedir(consulta: str, timeout: int) -> dict:
    datos = urlencode({"data": consulta}).encode("utf-8")
    peticion = Request(
        URL,
        data=datos,
        headers={"User-Agent": "ChucuaDeLaVaca/1.0 (proyecto academico)"},
    )
    with urlopen(peticion, timeout=timeout) as respuesta:
        return json.loads(respuesta.read().decode("utf-8"))


def consultar(
    dominio: str,
    *,
    timeout: int = 60,
    reintentos: int = 2,
    obtener=None,
    dormir=time.sleep,
) -> list[dict]:
    obtener = obtener or _pedir
    consulta = construir_consulta(dominio, timeout=timeout)
    for intento in range(reintentos + 1):
        try:
            return obtener(consulta, timeout).get("elements", [])
        except (URLError, TimeoutError, OSError, ValueError):
            if intento == reintentos:
                return []
            dormir(2 ** intento)
    return []


def consultar_todo(**opciones) -> dict[str, list[dict]]:
    return {dominio: consultar(dominio, **opciones) for dominio in CONSULTAS}
