from ..dominio.salud import CentroSalud
from .generico import RepositorioGenerico


class RepositorioCentrosSalud(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="centros_salud",
            columnas=("tipo_centro", "nivel_atencion", "horario", "direccion"),
            entidad=CentroSalud,
        )
