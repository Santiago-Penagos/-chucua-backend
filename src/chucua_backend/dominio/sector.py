from typing import Literal

from ..errores import ErrorValidacion

Sector = Literal["I", "II", "III"]
SECTORES: tuple[str, ...] = ("I", "II", "III")


def validar_sector(valor: str | None) -> Sector:
    """Devuelve el sector normalizado o falla si no es I, II o III."""
    if valor not in SECTORES:
        permitidos = ", ".join(SECTORES)
        raise ErrorValidacion(
            f"Sector inválido: {valor!r}. Valores permitidos: {permitidos}"
        )
    return valor  # type: ignore[return-value]
