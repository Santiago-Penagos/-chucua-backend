from ..dominio.jac import JuntaAccionComunal
from .generico import RepositorioGenerico


class RepositorioJac(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="jac",
            columnas=("presidente_contacto", "direccion", "horario_atencion"),
            entidad=JuntaAccionComunal,
        )
