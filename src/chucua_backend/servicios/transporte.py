from ..dominio.transporte import ParaderoSitp
from .servicio_base import ServicioBase


class ServicioTransporte(ServicioBase[ParaderoSitp]):
    """Servicio de aplicación para paraderos SITP."""
