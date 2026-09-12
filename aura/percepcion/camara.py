"""Captura de video.

En la Raspberry Pi el cuello de botella es la inferencia, no la captura: si la
lectura de frames y el procesamiento comparten hilo, la imagen se congela. Por
eso la cámara corre en su propio hilo y siempre entrega el frame más reciente,
descartando los atrasados.

Descartar es deliberado. Si en vez de eso encoláramos los frames, con MediaPipe
corriendo más lento que la cámara la cola crecería sin fin y terminaríamos
mostrando video de hace diez segundos.
"""

from __future__ import annotations

import threading

import cv2
import numpy as np

from aura.util import registro

log = registro.obtener(__name__)


class CamaraNoDisponible(RuntimeError):
    """La cámara no abrió. En la Pi casi siempre es el índice o los permisos."""


class Camara:
    """Lector de cámara en segundo plano."""

    def __init__(self, indice: int = 0, ancho: int = 640, alto: int = 480) -> None:
        self.indice = indice
        self.ancho = ancho
        self.alto = alto

        self._captura: cv2.VideoCapture | None = None
        self._hilo: threading.Thread | None = None
        self._frame: np.ndarray | None = None
        # Condition y no Lock: el bucle principal necesita dormirse hasta que
        # haya un frame nuevo, en vez de girar en vacío gastando CPU de la Pi.
        self._cond = threading.Condition()
        # Cada captura incrementa este número. Así el consumidor distingue un
        # frame nuevo de el mismo de antes, y no procesa dos veces la misma
        # imagen (que con MediaPipe encima sería tirar CPU a la basura).
        self._secuencia = 0
        self._corriendo = threading.Event()
        # Se levanta con el primer frame, para que abrir() no devuelva antes de
        # que haya imagen y el bucle principal no tenga que adivinar.
        self._hay_frame = threading.Event()

    def abrir(self, espera_segundos: float = 5.0) -> None:
        """Inicia la captura y el hilo de lectura."""
        captura = cv2.VideoCapture(self.indice)
        if not captura.isOpened():
            captura.release()
            raise CamaraNoDisponible(
                f"No se pudo abrir la cámara {self.indice}. "
                "Revisá el índice en config.json y que el usuario esté en el "
                "grupo 'video'."
            )

        captura.set(cv2.CAP_PROP_FRAME_WIDTH, self.ancho)
        captura.set(cv2.CAP_PROP_FRAME_HEIGHT, self.alto)
        # Buffer de 1: que el driver no nos guarde frames viejos.
        captura.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self._captura = captura
        self._corriendo.set()
        self._hilo = threading.Thread(target=self._leer_continuo, daemon=True)
        self._hilo.start()

        if not self._hay_frame.wait(espera_segundos):
            self.cerrar()
            raise CamaraNoDisponible(
                f"La cámara {self.indice} abrió pero no entregó ningún frame en "
                f"{espera_segundos:g} s."
            )

        real = (
            int(captura.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
        log.info("Cámara %d abierta a %dx%d", self.indice, *real)

    def _leer_continuo(self) -> None:
        fallos = 0
        while self._corriendo.is_set() and self._captura is not None:
            ok, frame = self._captura.read()
            if not ok:
                fallos += 1
                if fallos >= 30:
                    log.error("La cámara dejó de entregar frames; detengo el hilo")
                    break
                continue
            fallos = 0
            with self._cond:
                self._frame = frame
                self._secuencia += 1
                self._cond.notify_all()
            self._hay_frame.set()

    def leer(self) -> np.ndarray | None:
        """Último frame disponible, o None si todavía no hay ninguno.

        Devuelve una copia: el hilo de captura sobreescribe `_frame` y sin la
        copia el bucle principal estaría dibujando sobre una imagen que cambia
        bajo sus pies.
        """
        with self._cond:
            if self._frame is None:
                return None
            return self._frame.copy()

    @property
    def secuencia(self) -> int:
        """Número del último frame capturado."""
        with self._cond:
            return self._secuencia

    def esperar_nuevo(
        self, desde: int = -1, timeout: float = 1.0
    ) -> tuple[np.ndarray, int] | None:
        """Bloquea hasta que haya un frame posterior a `desde`.

        Devuelve `(imagen, secuencia)`, o None si se venció el timeout. El
        consumidor guarda la secuencia que recibió y la pasa en la siguiente
        llamada; así el bucle corre al ritmo de la cámara y no más rápido.
        """
        with self._cond:
            if self._secuencia <= desde:
                self._cond.wait(timeout)
            if self._frame is None or self._secuencia <= desde:
                return None
            return self._frame.copy(), self._secuencia

    def cerrar(self) -> None:
        """Libera la cámara y detiene el hilo."""
        self._corriendo.clear()
        if self._hilo is not None:
            self._hilo.join(timeout=2.0)
            self._hilo = None
        if self._captura is not None:
            self._captura.release()
            self._captura = None
        self._hay_frame.clear()
        log.info("Cámara %d cerrada", self.indice)

    def __enter__(self) -> Camara:
        self.abrir()
        return self

    def __exit__(self, *_: object) -> None:
        self.cerrar()
