"""Los contratos se prueban porque son el acuerdo entre los cinco módulos.

Si alguien cambia una firma de `aura/contratos.py`, estas pruebas truenan antes
de que el cambio rompa el trabajo de otro.
"""

from datetime import datetime

import numpy as np

from aura.contratos import EstadoAura, EstadoRobot, EventoGesto, Frame, Gesto


def test_frame_sin_pose_no_tiene_persona():
    frame = Frame(imagen=np.zeros((2, 2, 3), np.uint8), timestamp=datetime.now())
    assert not frame.hay_persona


def test_catalogo_cubre_los_nueve_gestos_obligatorios():
    from aura.gestos.catalogo import CATALOGO

    obligatorios = [
        Gesto.PERSONA_APARECE,
        Gesto.MANO_LEVANTADA,
        Gesto.PULGAR_ARRIBA,
        Gesto.PULGAR_ABAJO,
        Gesto.SENALAR_IZQUIERDA,
        Gesto.SENALAR_DERECHA,
        Gesto.BRAZOS_CRUZADOS,
        Gesto.PERSONA_SE_ACERCA,
        Gesto.PERSONA_DESAPARECE,
    ]
    assert all(g in CATALOGO for g in obligatorios)


def test_cada_estado_del_robot_tiene_nombre_de_sprite_unico():
    nombres = [e.value for e in EstadoRobot]
    assert len(nombres) == len(set(nombres)) == 8


def test_estado_inicial_es_esperando():
    assert EstadoAura().estado is EstadoRobot.ESPERANDO


def test_evento_gesto_acepta_gestos_personalizados():
    evento = EventoGesto(gesto="saludo_maya", confianza=0.9, timestamp=datetime.now())
    assert evento.gesto == "saludo_maya"
