"""Completar formulario — gesto: simular escritura con el índice.

Accede al formulario que proporcionen los auxiliares y llena los campos con la
información disponible en el sistema. Antes de enviar valida que los campos
requeridos quedaron completos: el enunciado lo pide explícitamente.
"""

from __future__ import annotations

from aura.contratos import ResultadoRPA
from aura.rpa.base import ProcesoRPA


class CompletarFormulario(ProcesoRPA):
    nombre = "completar_formulario"
    descripcion = "Llena y valida el formulario asignado por los auxiliares"

    def ejecutar(self, **parametros) -> ResultadoRPA:
        raise NotImplementedError("Fase 4 — P5")

    def _validar_requeridos(self) -> list[str]:
        """Campos requeridos que quedaron vacíos."""
        raise NotImplementedError("Fase 4 — P5")
