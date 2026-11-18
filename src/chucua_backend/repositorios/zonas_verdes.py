from ..dominio.zonas_verdes import ZonaVerde
from .generico import RepositorioGenerico


class RepositorioZonasVerdes(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="zonas_verdes",
            columnas=(
                "area_aprox_m2",
                "tipo_vegetacion",
                "estado_mantenimiento",
                "direccion",
            ),
            entidad=ZonaVerde,
        )
