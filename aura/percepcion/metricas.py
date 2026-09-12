"""Medición de FPS y latencia del pipeline.

"Sin lag evidente" es un criterio de la rúbrica que vale 50 puntos, así que se
mide en vez de estimarse a ojo. El número se dibuja en el overlay durante el
desarrollo.
"""

from __future__ import annotations


class ContadorFPS:
    """Promedio móvil de cuadros por segundo."""

    def __init__(self, ventana: int = 30) -> None:
        self.ventana = ventana

    def marcar(self) -> None:
        """Registra que se terminó de procesar un cuadro."""
        raise NotImplementedError("Fase 2 — P1")

    @property
    def fps(self) -> float:
        raise NotImplementedError("Fase 2 — P1")
