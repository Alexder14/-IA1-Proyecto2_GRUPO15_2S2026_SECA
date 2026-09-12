"""Los gestos que AURA reconoce y qué significa cada uno.

Las nueve primeras filas son la tabla obligatoria del Módulo 1 y las tres
últimas las del Módulo 3. Aquí vive el texto que la interfaz muestra como
"interpretación", que es parte de lo que la rúbrica exige ver en el video.

Los gestos que el usuario registre con `/addGesture` se guardan aparte, en
`datos/gestos.json`, y se combinan con este catálogo en tiempo de ejecución.
"""

from __future__ import annotations

from dataclasses import dataclass

from aura.contratos import Gesto


@dataclass(frozen=True)
class DefinicionGesto:
    gesto: Gesto
    interpretacion: str
    respuesta: str
    habilitado: bool = True


CATALOGO: dict[Gesto, DefinicionGesto] = {
    Gesto.PERSONA_APARECE: DefinicionGesto(
        Gesto.PERSONA_APARECE, "Usuario presente", "Saludar"
    ),
    Gesto.MANO_LEVANTADA: DefinicionGesto(
        Gesto.MANO_LEVANTADA, "Saludo", "Responder"
    ),
    Gesto.PULGAR_ARRIBA: DefinicionGesto(
        Gesto.PULGAR_ARRIBA, "Aprobación", "Confirmar"
    ),
    Gesto.PULGAR_ABAJO: DefinicionGesto(
        Gesto.PULGAR_ABAJO, "Rechazo", "Cambiar respuesta"
    ),
    Gesto.SENALAR_IZQUIERDA: DefinicionGesto(
        Gesto.SENALAR_IZQUIERDA, "Dirección", "Mostrar opción izquierda"
    ),
    Gesto.SENALAR_DERECHA: DefinicionGesto(
        Gesto.SENALAR_DERECHA, "Dirección", "Mostrar opción derecha"
    ),
    Gesto.BRAZOS_CRUZADOS: DefinicionGesto(
        Gesto.BRAZOS_CRUZADOS, "Comando definido", "Ejecutar acción"
    ),
    Gesto.PERSONA_SE_ACERCA: DefinicionGesto(
        Gesto.PERSONA_SE_ACERCA, "Proximidad", "Activar interacción"
    ),
    Gesto.PERSONA_DESAPARECE: DefinicionGesto(
        Gesto.PERSONA_DESAPARECE, "Fin de interacción", "Despedirse"
    ),
    Gesto.INDICE_ARRIBA: DefinicionGesto(
        Gesto.INDICE_ARRIBA, "Consultar / mostrar información", "Consultar horario"
    ),
    Gesto.INDICE_ABAJO: DefinicionGesto(
        Gesto.INDICE_ABAJO, "Descargar", "Descargar material"
    ),
    Gesto.ESCRITURA: DefinicionGesto(
        Gesto.ESCRITURA, "Ingresar / completar información", "Completar formulario"
    ),
}
