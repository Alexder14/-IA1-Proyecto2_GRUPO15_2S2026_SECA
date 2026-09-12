"""Ventana de OpenCV donde se muestra todo.

Corre en el hilo principal porque `cv2.imshow` no es seguro fuera de él.
"""

from __future__ import annotations

import numpy as np


class Ventana:
    def __init__(self, titulo: str = "AURA", pantalla_completa: bool = False) -> None:
        self.titulo = titulo
        self.pantalla_completa = pantalla_completa

    def abrir(self) -> None:
        raise NotImplementedError("Fase 2 — P3")

    def mostrar(self, imagen: np.ndarray) -> bool:
        """Pinta el frame. Devuelve False si el usuario pidió salir."""
        raise NotImplementedError("Fase 2 — P3")

    def cerrar(self) -> None:
        raise NotImplementedError("Fase 2 — P3")
