"""Robot virtual 2D que representa al agente.

Un sprite por estado, cargados una sola vez al arrancar y compuestos sobre el
video respetando el canal alfa. El enunciado es explícito en dos puntos: no
vale un único asset estático cuyo estado se indique solo con texto, y no se
permite 3D.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from aura.contratos import EstadoRobot


class RobotVirtual:
    """Carga los sprites y los compone sobre el frame según el estado."""

    def __init__(
        self,
        ruta_assets: Path | str = "assets/robot",
        escala: float = 0.25,
        posicion: str = "inferior_derecha",
    ) -> None:
        self.ruta_assets = Path(ruta_assets)
        self.escala = escala
        self.posicion = posicion

    def cargar(self) -> None:
        """Lee los ocho PNG con alfa. Falla si falta alguno."""
        raise NotImplementedError("Fase 2 — P3")

    def dibujar(self, imagen: np.ndarray, estado: EstadoRobot) -> None:
        """Compone el sprite del estado sobre la imagen, en sitio."""
        raise NotImplementedError("Fase 2 — P3")
