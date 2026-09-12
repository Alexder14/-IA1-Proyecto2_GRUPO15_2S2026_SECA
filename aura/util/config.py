"""Carga de `config/config.json` y de las variables de entorno de `.env`."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[2]
RUTA_CONFIG = RAIZ / "config" / "config.json"
RUTA_ENV = RAIZ / ".env"


def cargar_config(ruta: Path | None = None) -> dict[str, Any]:
    """Devuelve la configuración del agente.

    Lanza `FileNotFoundError` con instrucciones si falta el archivo: es el
    error más común al clonar el repo, porque `config.json` no se versiona.
    """
    ruta = ruta or RUTA_CONFIG
    if not ruta.exists():
        raise FileNotFoundError(
            f"Falta {ruta}. Copiá la plantilla: "
            "cp config/config.example.json config/config.json"
        )
    return json.loads(ruta.read_text(encoding="utf-8"))


def cargar_env(ruta: Path | None = None) -> None:
    """Mete las variables de `.env` en `os.environ` sin pisar las existentes.

    Se hace a mano en vez de con python-dotenv para no sumar una dependencia
    por diez líneas.
    """
    ruta = ruta or RUTA_ENV
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        os.environ.setdefault(clave.strip(), valor.strip())


def variable(nombre: str, obligatoria: bool = True) -> str:
    """Lee una variable de entorno; falla temprano si falta una obligatoria."""
    valor = os.environ.get(nombre, "")
    if obligatoria and not valor:
        raise RuntimeError(f"Falta la variable {nombre} en el archivo .env")
    return valor
