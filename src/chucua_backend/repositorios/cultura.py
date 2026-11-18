from ..dominio.cultura import EspacioCultural
from .generico import RepositorioGenerico


class RepositorioCultura(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="cultura",
            columnas=(
                "tipo_espacio",
                "actividad_principal",
                "direccion",
                "aforo_aproximado",
            ),
            entidad=EspacioCultural,
        )
