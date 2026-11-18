from ..dominio.transporte import ParaderoSitp
from .generico import RepositorioGenerico


class RepositorioTransporte(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="transporte",
            columnas=(
                "codigo_paradero",
                "rutas_alimentadoras",
                "direccion",
                "estado_senalizacion",
            ),
            entidad=ParaderoSitp,
        )
