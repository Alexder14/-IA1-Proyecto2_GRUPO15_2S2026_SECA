"""Los trece comandos obligatorios del bot de Telegram.

Cada comando que falte o funcione mal cuesta 5% del proyecto; los trece juntos
son el 65%. Por eso están todos declarados desde el esqueleto: la lista sirve
de checklist para la revisión del 08/10.

Todos leen o escriben sobre el agente real. Respuestas simuladas o estáticas
las castiga la rúbrica explícitamente.
"""

from __future__ import annotations

from aura.agente.nucleo import Agente


class Comandos:
    """Handlers de Telegram, con el agente inyectado."""

    def __init__(self, agente: Agente) -> None:
        self.agente = agente

    # -- estado del sistema --------------------------------------------------

    async def status(self, *args, **kwargs):
        """CPU, RAM y estado de los servicios de la Raspberry Pi."""
        raise NotImplementedError("Fase 3 — P4")

    async def iniciar(self, *args, **kwargs):
        """Inicia el reconocimiento e interacción."""
        raise NotImplementedError("Fase 3 — P1 y P4")

    async def apagar(self, *args, **kwargs):
        """Detiene el reconocimiento o apaga el servicio controladamente."""
        raise NotImplementedError("Fase 3 — P1 y P4")

    async def logs(self, *args, **kwargs):
        """Últimos eventos, errores y acciones ejecutadas."""
        raise NotImplementedError("Fase 3 — P4")

    # -- gestos --------------------------------------------------------------

    async def history(self, *args, **kwargs):
        """Historial de gestos: fecha, confianza y acción ejecutada."""
        raise NotImplementedError("Fase 3 — P4")

    async def gestures(self, *args, **kwargs):
        """Lista los gestos registrados en el sistema."""
        raise NotImplementedError("Fase 3 — P2")

    async def add_gesture(self, *args, **kwargs):
        """Registra o entrena una nueva seña."""
        raise NotImplementedError("Fase 3 — P2")

    async def delete_gesture(self, *args, **kwargs):
        """Elimina o deshabilita una seña."""
        raise NotImplementedError("Fase 3 — P2")

    # -- acciones ------------------------------------------------------------

    async def actions(self, *args, **kwargs):
        """Muestra las acciones disponibles."""
        raise NotImplementedError("Fase 3 — P4")

    async def add_action(self, *args, **kwargs):
        """Crea una acción que pueda ejecutar el agente."""
        raise NotImplementedError("Fase 3 — P4")

    async def link_action(self, *args, **kwargs):
        """Asocia un gesto con una acción determinada."""
        raise NotImplementedError("Fase 3 — P4")

    async def send_message(self, *args, **kwargs):
        """Configura un mensaje como respuesta a determinado gesto."""
        raise NotImplementedError("Fase 3 — P4")

    # -- rpa -----------------------------------------------------------------

    async def rpa(self, *args, **kwargs):
        """Consulta los procesos RPA disponibles."""
        raise NotImplementedError("Fase 3 — P4 y P5")


# Checklist de la revisión del 08/10. Si un nombre no está aquí, es -5%.
OBLIGATORIOS = [
    "status",
    "iniciar",
    "apagar",
    "history",
    "gestures",
    "addGesture",
    "deleteGesture",
    "actions",
    "addAction",
    "linkAction",
    "sendMessage",
    "rpa",
    "logs",
]
