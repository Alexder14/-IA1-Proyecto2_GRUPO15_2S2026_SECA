"""Pruebas de la capa de percepción que no necesitan cámara.

Lo que sí necesita hardware se prueba en la Pi, a mano. Acá queda lo que puede
correr en cualquier laptop y en CI.
"""

import time

import pytest

from aura.percepcion.camara import Camara, CamaraNoDisponible
from aura.percepcion.metricas import ContadorFPS


def test_contador_sin_marcas_reporta_cero():
    assert ContadorFPS().fps == 0.0


def test_contador_con_una_sola_marca_no_divide_entre_cero():
    c = ContadorFPS()
    c.marcar()
    assert c.fps == 0.0


def test_contador_mide_la_tasa_real():
    c = ContadorFPS()
    for _ in range(6):
        c.marcar()
        time.sleep(0.02)
    # 50 Hz nominales; el sleep no es exacto, así que damos margen.
    assert 25 < c.fps < 100


def test_contador_solo_promedia_la_ventana():
    c = ContadorFPS(ventana=3)
    for _ in range(10):
        c.marcar()
    assert len(c._marcas) == 3


def test_camara_inexistente_falla_con_mensaje_util():
    # Índice absurdo: ninguna máquina tiene 99 cámaras.
    with pytest.raises(CamaraNoDisponible) as error:
        Camara(indice=99).abrir(espera_segundos=0.5)
    assert "99" in str(error.value)


def test_camara_cerrada_no_entrega_frames():
    cam = Camara(indice=99)
    assert cam.leer() is None
    assert cam.esperar_nuevo(timeout=0.05) is None
