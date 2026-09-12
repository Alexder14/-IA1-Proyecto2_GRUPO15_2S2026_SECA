"""Acciones que el agente puede ejecutar y su vínculo con los gestos.

Un gesto no sabe qué hace; solo sabe que está vinculado a una acción. Esa
indirección es la que permite que `/linkAction` reasigne qué hace cada gesto
sin tocar código, y que `/addAction` agregue acciones nuevas en caliente.

Tipos de acción: un proceso RPA, un mensaje de Telegram fijo (`/sendMessage`),
o una respuesta visual del robot.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

RUTA = Path(__file__).resolve().parents[2] / "datos" / "acciones.json"


@dataclass
class Accion:
    nombre: str
    tipo: str  # "rpa" | "mensaje" | "visual"
    parametros: dict


def listar() -> list[Accion]:
    """Alimenta `/actions`."""
    raise NotImplementedError("Fase 3 — P4")


def agregar(accion: Accion) -> None:
    """Alimenta `/addAction`."""
    raise NotImplementedError("Fase 3 — P4")


def vincular(gesto: str, accion: str) -> None:
    """Alimenta `/linkAction`."""
    raise NotImplementedError("Fase 3 — P4")


def accion_de(gesto: str) -> Accion | None:
    """Qué acción corresponde a un gesto, o None si no tiene vínculo."""
    raise NotImplementedError("Fase 3 — P4")
