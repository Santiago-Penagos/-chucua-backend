class ErrorValidacion(ValueError):
    """Entrada que no cumple una invariante de dominio."""


class EntidadNoEncontrada(LookupError):
    """La entidad solicitada no existe en la persistencia."""
