"""Punto de entrada de AURA.

Reparto de hilos:

- **principal**: ventana de OpenCV (`cv2.imshow` no es seguro en otro hilo)
- **cámara**: lectura continua, siempre entrega el frame más reciente
- **bot**: polling de Telegram
- **rpa**: uno por proceso disparado, para que el video no se congele

El bucle principal es corto a propósito: leer, extraer, clasificar, decidir,
dibujar. Todo lo lento vive en otro hilo.
"""

from __future__ import annotations

from aura.agente.nucleo import Agente
from aura.gestos.clasificador import Clasificador
from aura.interfaz.overlay import Overlay
from aura.interfaz.robot import RobotVirtual
from aura.interfaz.ventana import Ventana
from aura.percepcion.camara import Camara
from aura.percepcion.landmarks import Extractor
from aura.util import config, registro


def construir() -> tuple[Camara, Extractor, Clasificador, Agente, Overlay, RobotVirtual, Ventana]:
    """Arma todas las piezas a partir de `config/config.json`."""
    raise NotImplementedError("Fase 1 — P1")


def bucle() -> None:
    """Leer → extraer → clasificar → decidir → dibujar, hasta que se pida salir."""
    raise NotImplementedError("Fase 1 — P1")


def main() -> None:
    config.cargar_env()
    registro.configurar()
    bucle()


if __name__ == "__main__":
    main()
