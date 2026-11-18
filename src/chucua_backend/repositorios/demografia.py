from ..dominio.demografia import DemografiaSector
from .generico import RepositorioGenerico


class RepositorioDemografia(RepositorioGenerico):
    def __init__(self, conexion):
        super().__init__(
            conexion,
            tabla="demografia",
            columnas=(
                "poblacion_estimada",
                "hogares_aprox",
                "grupo_etario_predominante",
                "anio_censo",
            ),
            entidad=DemografiaSector,
        )
