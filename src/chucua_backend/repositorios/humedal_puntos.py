from ..dominio.humedal_puntos import PuntoHumedal
from .generico import RepositorioGenerico


class RepositorioHumedalPuntos(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="humedal_puntos",
            columnas=("zona_humedal", "estado_conservacion", "especie_destacada"),
            entidad=PuntoHumedal,
        )
