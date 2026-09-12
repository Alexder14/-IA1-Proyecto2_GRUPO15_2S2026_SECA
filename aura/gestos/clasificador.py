"""Traduce landmarks a gestos.

Dos problemas aparte de reconocer la forma de la mano:

1. **Ruido.** Un gesto reconocido en un solo cuadro puede ser un dedo a medio
   camino. Se exige verlo N cuadros seguidos antes de confirmarlo.
2. **Repetición.** A 15 FPS, un pulgar arriba sostenido dispararía la acción
   quince veces por segundo. Tras confirmar un gesto se aplica un enfriamiento
   durante el cual ese mismo gesto se ignora.
"""

from __future__ import annotations

from aura.contratos import EventoGesto, Frame, Gesto


class Clasificador:
    """Reconoce gestos cuadro a cuadro y emite eventos ya estabilizados."""

    def __init__(
        self,
        umbral_confianza: float = 0.75,
        frames_para_confirmar: int = 5,
        enfriamiento_segundos: float = 3.0,
    ) -> None:
        self.umbral_confianza = umbral_confianza
        self.frames_para_confirmar = frames_para_confirmar
        self.enfriamiento_segundos = enfriamiento_segundos

    def evaluar(self, frame: Frame) -> EventoGesto | None:
        """Devuelve un gesto solo cuando queda confirmado y fuera de enfriamiento."""
        raise NotImplementedError("Fase 2 — P2")

    def candidato(self, frame: Frame) -> tuple[Gesto | str | None, float]:
        """Gesto y confianza de este cuadro, sin estabilizar.

        La interfaz lo usa para mostrar el estado "interpretando": el usuario ve
        que AURA ya está viendo algo antes de que la acción se dispare.
        """
        raise NotImplementedError("Fase 2 — P2")

    def recargar_personalizados(self) -> None:
        """Relee los gestos registrados con `/addGesture`."""
        raise NotImplementedError("Fase 3 — P2")
