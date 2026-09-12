"""Métricas de la Raspberry Pi para el comando `/status`.

La rúbrica castiga que `/status` devuelva valores simulados: estos números
tienen que salir del dispositivo real.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Recursos:
    cpu_porcentaje: float
    ram_usada_mb: float
    ram_total_mb: float
    temperatura_c: float | None
    uptime_segundos: float


def medir() -> Recursos:
    """Lee CPU, RAM, temperatura y uptime con psutil."""
    raise NotImplementedError("Fase 1 — P4")
