"""Bitácora del agente.

Escribe a consola y a `datos/aura.log`. El comando `/logs` de Telegram lee las
últimas líneas de ese archivo, así que el formato debe ser legible en un chat.
"""

from __future__ import annotations

import logging
from pathlib import Path

RUTA_LOG = Path(__file__).resolve().parents[2] / "datos" / "aura.log"
FORMATO = "%(asctime)s %(levelname)-7s [%(name)s] %(message)s"


def configurar(nivel: int = logging.INFO) -> None:
    """Arranca el logging del proceso. Se llama una sola vez, desde main."""
    raise NotImplementedError("Fase 1 — P1")


def obtener(nombre: str) -> logging.Logger:
    """Logger para un módulo. Usar `obtener(__name__)`."""
    return logging.getLogger(nombre)


def ultimas_lineas(cantidad: int = 20) -> list[str]:
    """Últimas entradas de la bitácora, para el comando `/logs`."""
    raise NotImplementedError("Fase 3 — P4")
