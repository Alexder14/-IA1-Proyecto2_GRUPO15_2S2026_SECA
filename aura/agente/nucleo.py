"""El agente: percibe, interpreta, decide, ejecuta.

Es el punto donde se cruzan los tres módulos. Recibe eventos de gestos, decide
qué acción corresponde, la ejecuta (RPA o mensaje), y publica su estado para
que la interfaz lo dibuje y el bot lo reporte.

Todo lo que el agente sabe de sí mismo vive aquí; la interfaz y el bot solo
leen. Así el estado nunca queda descrito en dos lugares distintos.
"""

from __future__ import annotations

from collections.abc import Callable

from aura.contratos import EstadoAura, EventoGesto, ResultadoRPA


class Agente:
    """Máquina de estados de AURA."""

    def __init__(self) -> None:
        self._estado = EstadoAura()
        self._activo = False
        self._observadores: list[Callable[[EstadoAura], None]] = []

    # -- ciclo de vida (lo controla `/iniciar` y `/apagar`) ------------------

    def iniciar(self) -> None:
        """Habilita el reconocimiento y la interacción."""
        raise NotImplementedError("Fase 2 — P4")

    def apagar(self) -> None:
        """Detiene el reconocimiento de forma controlada."""
        raise NotImplementedError("Fase 2 — P4")

    @property
    def activo(self) -> bool:
        return self._activo

    # -- ciclo de razonamiento ----------------------------------------------

    def procesar(self, evento: EventoGesto) -> ResultadoRPA | None:
        """Interpreta el gesto, decide la acción y la ejecuta.

        Recorre los estados del robot en el camino: detectando → interpretando
        → ejecutando → éxito o error.
        """
        raise NotImplementedError("Fase 2 — P4")

    @property
    def estado(self) -> EstadoAura:
        """Instantánea de lo que el agente está pensando ahora mismo."""
        return self._estado

    # -- notificación a interfaz y bot --------------------------------------

    def suscribir(self, observador: Callable[[EstadoAura], None]) -> None:
        """Registra a quien deba enterarse de cada cambio de estado.

        La interfaz se suscribe para redibujar; el bot, para avisar por
        Telegram lo que el agente decidió.
        """
        self._observadores.append(observador)
