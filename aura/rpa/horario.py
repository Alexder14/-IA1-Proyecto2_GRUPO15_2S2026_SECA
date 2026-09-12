"""Consultar horario — gesto: índice hacia arriba.

Entra al portal académico, navega hasta el curso y obtiene el horario de clase
magistral y de laboratorio. El resultado se le presenta al usuario por medio
del asistente.
"""

from __future__ import annotations

from aura.contratos import ResultadoRPA
from aura.rpa.base import ProcesoRPA


class ConsultarHorario(ProcesoRPA):
    nombre = "consultar_horario"
    descripcion = "Consulta el horario de magistral y laboratorio en el portal"

    def ejecutar(self, **parametros) -> ResultadoRPA:
        raise NotImplementedError("Fase 4 — P5")
