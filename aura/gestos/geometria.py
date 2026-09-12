"""Operaciones geométricas sobre landmarks.

Todo el reconocimiento de gestos se apoya en estas tres ideas: ángulos entre
articulaciones, distancias normalizadas y posiciones relativas. Nada de esto
requiere entrenar un modelo, y el enunciado tampoco lo permitiría.

Las distancias se normalizan contra una referencia del propio cuerpo (el ancho
de hombros, o el largo de la palma) para que un gesto se detecte igual de cerca
que de lejos de la cámara.
"""

from __future__ import annotations

from aura.contratos import Landmark


def distancia(a: Landmark, b: Landmark) -> float:
    """Distancia euclidiana en el plano de la imagen."""
    raise NotImplementedError("Fase 2 — P2")


def angulo(a: Landmark, vertice: Landmark, b: Landmark) -> float:
    """Ángulo en grados que forman a-vertice-b."""
    raise NotImplementedError("Fase 2 — P2")


def dedo_extendido(mano: list[Landmark], dedo: int) -> bool:
    """Si el dedo está estirado, comparando la punta contra sus falanges."""
    raise NotImplementedError("Fase 2 — P2")


def escala_corporal(pose: list[Landmark]) -> float:
    """Referencia para normalizar distancias: ancho de hombros en el frame.

    Crece cuando la persona se acerca, y de ahí sale también la detección de
    proximidad.
    """
    raise NotImplementedError("Fase 2 — P2")
