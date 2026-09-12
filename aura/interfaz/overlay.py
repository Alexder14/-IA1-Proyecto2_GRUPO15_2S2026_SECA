"""Realidad aumentada sobre el video en vivo.

Es el 50% del punteo. Lo que la rúbrica exige ver en pantalla:

- el feed de video fluido y sin lag evidente
- bounding boxes y landmarks sobre la persona
- el gesto detectado y su nivel de confianza
- la interpretación y la acción que el agente va a ejecutar

Si el video no muestra el texto y las cajas de razonamiento, son -30% aparte.
"""

from __future__ import annotations

import numpy as np

from aura.contratos import EstadoAura, Frame


class Overlay:
    """Dibuja el razonamiento de AURA encima del frame."""

    def __init__(self, mostrar_landmarks: bool = True, mostrar_caja: bool = True) -> None:
        self.mostrar_landmarks = mostrar_landmarks
        self.mostrar_caja = mostrar_caja

    def dibujar(self, frame: Frame, estado: EstadoAura) -> np.ndarray:
        """Devuelve una copia del frame con todas las capas encima."""
        raise NotImplementedError("Fase 2 — P3")

    def _dibujar_landmarks(self, imagen: np.ndarray, frame: Frame) -> None:
        raise NotImplementedError("Fase 2 — P3")

    def _dibujar_caja(self, imagen: np.ndarray, frame: Frame) -> None:
        raise NotImplementedError("Fase 2 — P3")

    def _dibujar_panel(self, imagen: np.ndarray, estado: EstadoAura) -> None:
        """Panel de razonamiento: percibe, interpreta, decide, ejecuta."""
        raise NotImplementedError("Fase 2 — P3")
