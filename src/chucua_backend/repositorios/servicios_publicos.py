from ..dominio.servicios_publicos import PuntoServicioPublico
from .generico import RepositorioGenerico


class RepositorioServiciosPublicos(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="servicios_publicos",
            columnas=("tipo_servicio", "estado_operativo", "ubicacion_referencia"),
            entidad=PuntoServicioPublico,
        )
