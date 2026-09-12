"""Historial de gestos detectados, con su confianza y la acción ejecutada.

Es lo que devuelve `/history`. Se persiste en disco para que sobreviva a un
reinicio del servicio, porque el bot puede consultarlo después de un `/apagar`.
"""

from __future__ import annotations

from pathlib import Path

from aura.contratos import RegistroHistorial

RUTA = Path(__file__).resolve().parents[2] / "datos" / "historial.json"


def registrar(entrada: RegistroHistorial) -> None:
    raise NotImplementedError("Fase 2 — P4")


def consultar(limite: int = 20) -> list[RegistroHistorial]:
    """Últimas entradas, de la más reciente a la más vieja."""
    raise NotImplementedError("Fase 2 — P4")
