"""Extracción de landmarks con MediaPipe.

Se usan dos soluciones a la vez: Hands para los gestos de mano y Pose para los
de cuerpo (brazos cruzados, persona presente, proximidad). Ambas son caras en
la Pi, así que la resolución de entrada y la frecuencia con la que se corren
son parámetros de `config.json`, no constantes.
"""

from __future__ import annotations

from datetime import datetime

import numpy as np

from aura.contratos import Frame


class Extractor:
    """Envuelve MediaPipe Hands y Pose detrás de una sola llamada."""

    def __init__(
        self,
        confianza_deteccion: float = 0.6,
        confianza_seguimiento: float = 0.5,
        max_manos: int = 2,
    ) -> None:
        self.confianza_deteccion = confianza_deteccion
        self.confianza_seguimiento = confianza_seguimiento
        self.max_manos = max_manos

    def abrir(self) -> None:
        """Carga los modelos. Tarda varios segundos en la Pi: hacerlo una vez."""
        raise NotImplementedError("Fase 2 — P1")

    def procesar(self, imagen: np.ndarray, timestamp: datetime | None = None) -> Frame:
        """Corre ambos modelos sobre la imagen y arma el Frame."""
        raise NotImplementedError("Fase 2 — P1")

    def cerrar(self) -> None:
        raise NotImplementedError("Fase 2 — P1")
