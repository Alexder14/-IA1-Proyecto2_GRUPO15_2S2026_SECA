"""Medición de FPS y latencia del pipeline.

"Sin lag evidente" es un criterio de la rúbrica que vale 50 puntos, así que se
mide en vez de estimarse a ojo. El número se dibuja en el overlay durante el
desarrollo.
"""

from __future__ import annotations

import time
from collections import deque


class ContadorFPS:
    """Promedio móvil de cuadros por segundo.

    Promedio móvil y no total acumulado: lo que interesa es cómo va ahora, no
    cómo iba hace diez minutos. Una caída de FPS cuando arranca un proceso RPA
    se ve en la ventana y desaparece del promedio total.
    """

    def __init__(self, ventana: int = 30) -> None:
        self.ventana = ventana
        self._marcas: deque[float] = deque(maxlen=ventana)

    def marcar(self) -> None:
        """Registra que se terminó de procesar un cuadro."""
        self._marcas.append(time.perf_counter())

    @property
    def fps(self) -> float:
        if len(self._marcas) < 2:
            return 0.0
        transcurrido = self._marcas[-1] - self._marcas[0]
        if transcurrido <= 0:
            return 0.0
        return (len(self._marcas) - 1) / transcurrido

    def reiniciar(self) -> None:
        self._marcas.clear()
