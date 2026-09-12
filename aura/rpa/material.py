"""Descargar material — gesto: índice hacia abajo.

Entra a UEDI, localiza el recurso indicado y descarga el enunciado. Al terminar
informa al usuario si la descarga se realizó correctamente, así que hay que
verificar el archivo en disco y no solo que el clic no tronara.
"""

from __future__ import annotations

from aura.contratos import ResultadoRPA
from aura.rpa.base import ProcesoRPA


class DescargarMaterial(ProcesoRPA):
    nombre = "descargar_material"
    descripcion = "Descarga desde UEDI el enunciado solicitado"

    def ejecutar(self, **parametros) -> ResultadoRPA:
        raise NotImplementedError("Fase 4 — P5")
