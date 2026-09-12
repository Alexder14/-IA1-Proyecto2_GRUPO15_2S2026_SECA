"""Bot de Telegram: la interfaz de administración del agente.

Bidireccional. De entrada recibe los comandos que controlan a AURA; de salida
avisa al usuario qué gesto se reconoció y cómo terminó la acción. Corre en su
propio hilo para no frenar el bucle de video.

Solo atiende al chat autorizado en `.env`: el token es público en la práctica y
estos comandos apagan servicios de la Raspberry Pi.
"""

from __future__ import annotations

from aura.agente.nucleo import Agente
from aura.contratos import EstadoAura


class BotAura:
    def __init__(self, token: str, chat_autorizado: str, agente: Agente) -> None:
        self.token = token
        self.chat_autorizado = chat_autorizado
        self.agente = agente

    def registrar_handlers(self) -> None:
        """Engancha los trece comandos de `comandos.py`."""
        raise NotImplementedError("Fase 3 — P4")

    def iniciar(self) -> None:
        """Arranca el polling en segundo plano."""
        raise NotImplementedError("Fase 3 — P4")

    def detener(self) -> None:
        raise NotImplementedError("Fase 3 — P4")

    def notificar(self, estado: EstadoAura) -> None:
        """Avisa al usuario un cambio relevante del agente.

        Se suscribe al agente, pero no reenvía todo: a 15 FPS eso sería un
        diluvio de mensajes. Solo eventos que le importan a una persona.
        """
        raise NotImplementedError("Fase 3 — P4")
