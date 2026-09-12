"""Gestos registrados en caliente desde Telegram.

`/addGesture` captura la posición actual de los landmarks y la guarda como
plantilla; el clasificador luego compara contra ella por distancia. Es lo más
simple que cumple "registrar/entrenar una nueva seña" sin salirse de OpenCV y
MediaPipe.
"""

from __future__ import annotations

from pathlib import Path

RUTA = Path(__file__).resolve().parents[2] / "datos" / "gestos.json"


def listar() -> list[dict]:
    """Gestos personalizados registrados. Alimenta `/gestures`."""
    raise NotImplementedError("Fase 3 — P2")


def agregar(nombre: str, plantilla: list[list[float]], interpretacion: str) -> None:
    """Guarda una seña nueva. Alimenta `/addGesture`."""
    raise NotImplementedError("Fase 3 — P2")


def eliminar(nombre: str) -> bool:
    """Borra o deshabilita una seña. Alimenta `/deleteGesture`."""
    raise NotImplementedError("Fase 3 — P2")
