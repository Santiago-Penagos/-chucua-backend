from ..dominio.seguridad import PuntoSeguridad
from .generico import RepositorioGenerico


class RepositorioSeguridad(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="seguridad",
            columnas=("tipo_punto", "cuadrante", "telefono_contacto"),
            entidad=PuntoSeguridad,
        )
