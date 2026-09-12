"""Punto de entrada de AURA.

Reparto de hilos:

- **principal**: ventana de OpenCV (`cv2.imshow` no es seguro en otro hilo)
- **cámara**: lectura continua, siempre entrega el frame más reciente
- **bot**: polling de Telegram                              (Fase 3 — P4)
- **rpa**: uno por proceso disparado, para que el video no se congele (Fase 4 — P5)

El bucle principal es corto a propósito: leer, extraer, clasificar, decidir,
dibujar. Todo lo lento vive en otro hilo.

Estado: Fase 1. Por ahora el bucle solo muestra el video y los FPS. Los pasos
de extracción, clasificación, decisión y overlay se enchufan en la Fase 2,
donde están marcados abajo.
"""

from __future__ import annotations

import signal
import sys
from dataclasses import dataclass
from types import FrameType

import cv2

from aura.interfaz.ventana import Ventana
from aura.percepcion.camara import Camara, CamaraNoDisponible
from aura.percepcion.metricas import ContadorFPS
from aura.util import config, registro

log = registro.obtener("aura")


@dataclass
class Aplicacion:
    """Las piezas vivas del agente.

    Va creciendo por fase: en la 2 entran el extractor, el clasificador, el
    agente y el overlay; en la 3, el bot.
    """

    camara: Camara
    ventana: Ventana
    fps: ContadorFPS

    def cerrar(self) -> None:
        self.ventana.cerrar()
        self.camara.cerrar()


def construir(cfg: dict | None = None) -> Aplicacion:
    """Arma las piezas a partir de `config/config.json`."""
    cfg = cfg if cfg is not None else config.cargar_config()

    cam = cfg.get("camara", {})
    interfaz = cfg.get("interfaz", {})

    camara = Camara(
        indice=cam.get("indice", 0),
        ancho=cam.get("ancho", 640),
        alto=cam.get("alto", 480),
    )
    ventana = Ventana(
        titulo="AURA",
        pantalla_completa=interfaz.get("pantalla_completa", False),
    )
    return Aplicacion(camara=camara, ventana=ventana, fps=ContadorFPS())


def _dibujar_fps(imagen, fps: float) -> None:
    """Marcador de FPS mientras desarrollamos.

    No es el overlay del proyecto —ese lo hace P3—, es el instrumento para saber
    si la Pi aguanta. La rúbrica pide video "sin lag evidente" y eso se mide.
    """
    texto = f"{fps:5.1f} FPS"
    cv2.putText(imagen, texto, (11, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)
    cv2.putText(imagen, texto, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)


def bucle(app: Aplicacion) -> None:
    """Leer → extraer → clasificar → decidir → dibujar, hasta que se pida salir."""
    app.camara.abrir()
    app.ventana.abrir()
    log.info("AURA en marcha. Salí con 'q' o Esc.")

    # Seguimos la secuencia para procesar cada frame una sola vez. Sin esto el
    # bucle giraría sobre la misma imagen miles de veces por segundo y los FPS
    # medidos no dirían nada.
    ultima = -1
    sin_frame = 0

    while True:
        resultado = app.camara.esperar_nuevo(desde=ultima, timeout=1.0)
        if resultado is None:
            sin_frame += 1
            if sin_frame >= 5:
                log.error("La cámara dejó de entregar frames")
                break
            continue
        imagen, ultima = resultado
        sin_frame = 0

        # Espejo: la gente espera verse como en un espejo, no invertida.
        imagen = cv2.flip(imagen, 1)

        # Fase 2 — P1: frame = extractor.procesar(imagen)
        # Fase 2 — P2: evento = clasificador.evaluar(frame)
        # Fase 2 — P4: if evento: agente.procesar(evento)
        # Fase 2 — P3: imagen = overlay.dibujar(frame, agente.estado)

        app.fps.marcar()
        _dibujar_fps(imagen, app.fps.fps)

        if not app.ventana.mostrar(imagen):
            log.info("Salida pedida por el usuario")
            break


def main() -> int:
    config.cargar_env()
    registro.configurar()

    app = construir()

    def apagar(_sig: int, _frame: FrameType | None) -> None:
        # systemd manda SIGTERM al reiniciar el servicio; sin esto la cámara
        # queda tomada y el siguiente arranque falla.
        log.info("Señal de apagado recibida")
        app.cerrar()
        sys.exit(0)

    signal.signal(signal.SIGINT, apagar)
    signal.signal(signal.SIGTERM, apagar)

    try:
        bucle(app)
    except CamaraNoDisponible as e:
        log.error("%s", e)
        return 1
    except Exception:
        log.exception("AURA se cayó con un error no previsto")
        return 1
    finally:
        app.cerrar()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
