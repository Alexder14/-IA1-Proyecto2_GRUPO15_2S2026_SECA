"""Cada comando obligatorio que falte cuesta 5% del proyecto.

Esta prueba es el checklist del 08/10 hecho automático.
"""

from aura.bot.comandos import OBLIGATORIOS, Comandos


def test_estan_declarados_los_trece_comandos():
    assert len(OBLIGATORIOS) == 13


def test_cada_comando_obligatorio_tiene_handler():
    faltantes = [
        nombre
        for nombre in OBLIGATORIOS
        # /addGesture en Telegram, add_gesture en Python
        if not hasattr(Comandos, "".join(
            "_" + c.lower() if c.isupper() else c for c in nombre
        ))
    ]
    assert faltantes == []
