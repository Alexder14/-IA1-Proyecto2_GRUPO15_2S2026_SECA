"""Bitácora del agente.

Escribe a consola y a `datos/aura.log`. El comando `/logs` de Telegram lee las
últimas líneas de ese archivo, así que el formato debe ser legible en un chat.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

RUTA_LOG = Path(__file__).resolve().parents[2] / "datos" / "aura.log"
FORMATO = "%(asctime)s %(levelname)-7s [%(name)s] %(message)s"
FECHA = "%Y-%m-%d %H:%M:%S"

# La Pi arranca con systemd y puede quedarse días corriendo. Sin rotación, el
# log se come la microSD.
TAMANO_MAX = 2 * 1024 * 1024
RESPALDOS = 3

_configurado = False


def configurar(nivel: int = logging.INFO) -> None:
    """Arranca el logging del proceso. Se llama una sola vez, desde main."""
    global _configurado
    if _configurado:
        return

    RUTA_LOG.parent.mkdir(parents=True, exist_ok=True)
    formato = logging.Formatter(FORMATO, datefmt=FECHA)

    consola = logging.StreamHandler()
    consola.setFormatter(formato)

    archivo = RotatingFileHandler(
        RUTA_LOG, maxBytes=TAMANO_MAX, backupCount=RESPALDOS, encoding="utf-8"
    )
    archivo.setFormatter(formato)

    raiz = logging.getLogger()
    raiz.setLevel(nivel)
    raiz.handlers.clear()
    raiz.addHandler(consola)
    raiz.addHandler(archivo)

    _configurado = True


def obtener(nombre: str) -> logging.Logger:
    """Logger para un módulo. Usar `obtener(__name__)`."""
    return logging.getLogger(nombre)


def ultimas_lineas(cantidad: int = 20) -> list[str]:
    """Últimas entradas de la bitácora, para el comando `/logs`."""
    raise NotImplementedError("Fase 3 — P4")
