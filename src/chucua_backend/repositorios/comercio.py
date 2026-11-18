from ..dominio.comercio import ComercioLocal
from .generico import RepositorioGenerico


class RepositorioComercio(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="comercio",
            columnas=(
                "categoria_comercial",
                "nombre_establecimiento",
                "direccion",
                "horario",
            ),
            entidad=ComercioLocal,
        )
