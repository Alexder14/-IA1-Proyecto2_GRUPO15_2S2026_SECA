"""Estructuras de datos que cruzan los módulos de AURA.

Este archivo es el acuerdo entre los cinco módulos. Cada quien programa contra
estas estructuras y puede alimentarlas con datos falsos mientras el módulo
vecino todavía no existe: la interfaz se dibuja sin cámara, el bot se prueba sin
visión y el RPA se ejecuta sin gestos.

Cambiar una firma de aquí rompe el trabajo de alguien más. Avisar al grupo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

import numpy as np

# --------------------------------------------------------------------------
# Percepción → Gestos
# --------------------------------------------------------------------------

# Un landmark es (x, y, z) normalizado a [0, 1] respecto al ancho y alto del
# frame, tal como lo entrega MediaPipe. Se conserva normalizado para que la
# clasificación no dependa de la resolución de la cámara.
Landmark = tuple[float, float, float]


@dataclass
class Frame:
    """Un cuadro de video con lo que MediaPipe encontró en él."""

    imagen: np.ndarray
    timestamp: datetime
    # 21 landmarks por mano detectada.
    manos: list[list[Landmark]] = field(default_factory=list)
    # 33 landmarks del cuerpo, o None si no hay persona en cuadro.
    pose: list[Landmark] | None = None

    @property
    def hay_persona(self) -> bool:
        return self.pose is not None


# --------------------------------------------------------------------------
# Gestos → Agente
# --------------------------------------------------------------------------


class Gesto(str, Enum):
    """Gestos que el sistema reconoce.

    Los primeros nueve son las percepciones obligatorias del Módulo 1; los tres
    últimos son los que disparan RPA en el Módulo 3.
    """

    PERSONA_APARECE = "persona_aparece"
    MANO_LEVANTADA = "mano_levantada"
    PULGAR_ARRIBA = "pulgar_arriba"
    PULGAR_ABAJO = "pulgar_abajo"
    SENALAR_IZQUIERDA = "senalar_izquierda"
    SENALAR_DERECHA = "senalar_derecha"
    BRAZOS_CRUZADOS = "brazos_cruzados"
    PERSONA_SE_ACERCA = "persona_se_acerca"
    PERSONA_DESAPARECE = "persona_desaparece"

    INDICE_ARRIBA = "indice_arriba"
    INDICE_ABAJO = "indice_abajo"
    ESCRITURA = "escritura"


@dataclass
class EventoGesto:
    """Un gesto ya confirmado, listo para que el agente decida qué hacer."""

    gesto: Gesto | str
    confianza: float
    timestamp: datetime
    metadatos: dict[str, Any] = field(default_factory=dict)


# --------------------------------------------------------------------------
# Agente → Interfaz
# --------------------------------------------------------------------------


class EstadoRobot(str, Enum):
    """Los estados del robot virtual 2D.

    Cada uno necesita su propio sprite en `assets/robot/`. Representarlos solo
    con texto sobre un asset estático invalida el Módulo 1.
    """

    ESPERANDO = "espera"
    SALUDO = "saludo"
    DETECTANDO = "deteccion"
    INTERPRETANDO = "interpretacion"
    EJECUTANDO = "ejecucion"
    EXITO = "exito"
    ERROR = "error"
    DESPEDIDA = "despedida"


@dataclass
class EstadoAura:
    """Lo que la interfaz dibuja sobre el video en un instante dado.

    Es el razonamiento del agente hecho visible: qué percibió, qué interpretó,
    qué decidió y qué resultado obtuvo. Que esto se vea en el video es el 30%
    del proyecto.
    """

    estado: EstadoRobot = EstadoRobot.ESPERANDO
    gesto: Gesto | str | None = None
    confianza: float = 0.0
    interpretacion: str = ""
    accion: str = ""
    resultado: str = ""


# --------------------------------------------------------------------------
# Agente → RPA
# --------------------------------------------------------------------------


@dataclass
class ResultadoRPA:
    """Lo que devuelve un proceso automatizado.

    `mensaje` es texto para el usuario: se muestra en el overlay y se envía por
    Telegram, así que debe ser legible por una persona, no un volcado técnico.
    """

    ok: bool
    mensaje: str
    datos: dict[str, Any] = field(default_factory=dict)


# --------------------------------------------------------------------------
# Agente → Historial / Telegram
# --------------------------------------------------------------------------


@dataclass
class RegistroHistorial:
    """Una entrada del historial que consulta `/history`."""

    timestamp: datetime
    gesto: str
    confianza: float
    accion: str
    resultado: str
