"""Ventana de OpenCV donde se muestra todo.

Corre en el hilo principal porque `cv2.imshow` no es seguro fuera de él. Todo
lo demás (cámara, bot, RPA) vive en otros hilos justamente para que este quede
libre de dibujar.
"""

from __future__ import annotations

import cv2
import numpy as np

from aura.util import registro

log = registro.obtener(__name__)

# Teclas que cierran la ventana: q y Esc.
SALIR = (ord("q"), 27)


class Ventana:
    def __init__(self, titulo: str = "AURA", pantalla_completa: bool = False) -> None:
        self.titulo = titulo
        self.pantalla_completa = pantalla_completa
        self._abierta = False

    def abrir(self) -> None:
        cv2.namedWindow(self.titulo, cv2.WINDOW_NORMAL)
        if self.pantalla_completa:
            cv2.setWindowProperty(
                self.titulo, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
            )
        self._abierta = True
        log.info("Ventana '%s' abierta", self.titulo)

    def mostrar(self, imagen: np.ndarray) -> bool:
        """Pinta el frame. Devuelve False si el usuario pidió salir.

        También devuelve False si cerraron la ventana con la X, que de otro modo
        dejaría el proceso corriendo sin nada en pantalla.
        """
        if not self._abierta:
            return False

        cv2.imshow(self.titulo, imagen)

        # El waitKey no es opcional: es lo que le da tiempo a OpenCV de dibujar.
        if (cv2.waitKey(1) & 0xFF) in SALIR:
            return False

        if cv2.getWindowProperty(self.titulo, cv2.WND_PROP_VISIBLE) < 1:
            return False

        return True

    def cerrar(self) -> None:
        if self._abierta:
            cv2.destroyWindow(self.titulo)
            cv2.waitKey(1)  # que el gestor de ventanas procese el cierre
            self._abierta = False
            log.info("Ventana '%s' cerrada", self.titulo)

    def __enter__(self) -> Ventana:
        self.abrir()
        return self

    def __exit__(self, *_: object) -> None:
        self.cerrar()
