"""Pruebas de la salida de la ventana.

El criterio de cierre de la Fase 1 es "sale con q". Eso no se puede probar
apretando una tecla en CI, así que se simula lo que devuelve cv2.waitKey.
"""

import numpy as np
import pytest

from aura.interfaz import ventana as modulo
from aura.interfaz.ventana import Ventana

NEGRO = np.zeros((4, 4, 3), np.uint8)


@pytest.fixture
def ventana_abierta(monkeypatch):
    """Una ventana que se cree abierta, sin tocar el servidor gráfico."""
    monkeypatch.setattr(modulo.cv2, "imshow", lambda *a: None)
    monkeypatch.setattr(modulo.cv2, "getWindowProperty", lambda *a: 1.0)
    v = Ventana()
    v._abierta = True
    return v


def test_la_tecla_q_pide_salir(ventana_abierta, monkeypatch):
    monkeypatch.setattr(modulo.cv2, "waitKey", lambda _: ord("q"))
    assert ventana_abierta.mostrar(NEGRO) is False


def test_la_tecla_esc_pide_salir(ventana_abierta, monkeypatch):
    monkeypatch.setattr(modulo.cv2, "waitKey", lambda _: 27)
    assert ventana_abierta.mostrar(NEGRO) is False


def test_sin_tecla_sigue_corriendo(ventana_abierta, monkeypatch):
    # -1 es lo que devuelve waitKey cuando nadie apretó nada.
    monkeypatch.setattr(modulo.cv2, "waitKey", lambda _: -1)
    assert ventana_abierta.mostrar(NEGRO) is True


def test_cerrar_con_la_x_tambien_pide_salir(ventana_abierta, monkeypatch):
    monkeypatch.setattr(modulo.cv2, "waitKey", lambda _: -1)
    monkeypatch.setattr(modulo.cv2, "getWindowProperty", lambda *a: 0.0)
    assert ventana_abierta.mostrar(NEGRO) is False


def test_ventana_sin_abrir_no_dibuja():
    assert Ventana().mostrar(NEGRO) is False
