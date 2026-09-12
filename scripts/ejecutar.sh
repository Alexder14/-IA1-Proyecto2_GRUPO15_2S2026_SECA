#!/usr/bin/env bash
# Arranca AURA con el entorno virtual del proyecto.
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck source=/dev/null
source .venv/bin/activate
exec python main.py
