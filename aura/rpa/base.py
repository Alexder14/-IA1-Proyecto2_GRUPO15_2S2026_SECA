"""Base común de los procesos RPA.

Todos siguen la misma forma: abrir el navegador, autenticarse, hacer la tarea,
cerrar, y devolver un `ResultadoRPA` con un mensaje legible por una persona
—porque ese texto termina en el overlay y en un chat de Telegram—.

Corren en un hilo aparte: un proceso puede tardar decenas de segundos y el
video no puede congelarse mientras tanto. En la Pi se usa Chromium en modo
headless.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from aura.contratos import ResultadoRPA


class ProcesoRPA(ABC):
    """Un proceso automatizado que el agente puede disparar."""

    nombre: str = ""
    descripcion: str = ""

    @abstractmethod
    def ejecutar(self, **parametros) -> ResultadoRPA:
        """Corre el proceso y devuelve qué pasó."""

    def _navegador(self):
        """Chromium headless configurado para la Raspberry Pi."""
        raise NotImplementedError("Fase 4 — P5")


def disponibles() -> list[ProcesoRPA]:
    """Procesos registrados. Alimenta el comando `/rpa`."""
    raise NotImplementedError("Fase 4 — P5")
