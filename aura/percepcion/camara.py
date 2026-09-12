"""Captura de video.

En la Raspberry Pi el cuello de botella es la inferencia, no la captura: si la
lectura de frames y el procesamiento comparten hilo, la imagen se congela. Por
eso la cámara corre en su propio hilo y siempre entrega el frame más reciente,
descartando los atrasados.
"""

from __future__ import annotations

import numpy as np


class Camara:
    """Lector de cámara en segundo plano."""

    def __init__(self, indice: int = 0, ancho: int = 640, alto: int = 480) -> None:
        self.indice = indice
        self.ancho = ancho
        self.alto = alto

    def abrir(self) -> None:
        """Inicia la captura y el hilo de lectura."""
        raise NotImplementedError("Fase 1 — P1")

    def leer(self) -> np.ndarray | None:
        """Último frame disponible, o None si todavía no hay ninguno."""
        raise NotImplementedError("Fase 1 — P1")

    def cerrar(self) -> None:
        """Libera la cámara y detiene el hilo."""
        raise NotImplementedError("Fase 1 — P1")

    def __enter__(self) -> Camara:
        self.abrir()
        return self

    def __exit__(self, *_: object) -> None:
        self.cerrar()
