#!/usr/bin/env bash
# Deja una Raspberry Pi lista para correr AURA.
#
# El riesgo que este script tiene que despejar primero es MediaPipe sobre ARM:
# no todas las versiones publican wheel para aarch64 y el enunciado no permite
# reemplazarlo por otra librería. Si la verificación del final falla, eso es lo
# único en lo que el grupo debe trabajar hasta resolverlo.
set -euo pipefail

echo "==> Paquetes de sistema"
sudo apt-get update
sudo apt-get install -y \
    python3-venv python3-dev python3-pip \
    libgl1 libglib2.0-0 \
    libatlas-base-dev \
    chromium-browser chromium-chromedriver

echo "==> Entorno virtual"
python3 -m venv .venv
# shellcheck source=/dev/null
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Configuración"
[ -f config/config.json ] || cp config/config.example.json config/config.json
[ -f .env ] || cp .env.example .env

echo "==> Verificación: arquitectura y librerías de visión"
uname -m
python - <<'PY'
import cv2, mediapipe
print("opencv   ", cv2.__version__)
print("mediapipe", mediapipe.__version__)
PY

echo "==> Verificación: cámara"
python - <<'PY'
import cv2
cap = cv2.VideoCapture(0)
ok, frame = cap.read()
cap.release()
print("camara   ", "ok" if ok else "SIN SEÑAL", frame.shape if ok else "")
PY

echo "==> Listo"
