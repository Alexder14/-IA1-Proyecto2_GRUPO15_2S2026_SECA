#!/usr/bin/env bash
# Lleva el código a la Raspberry Pi en un solo comando.
#
#   ./scripts/desplegar.sh [usuario@host]
#
# Actualiza el repo en la Pi, instala dependencias nuevas si las hay y
# reinicia el servicio. Es el reemplazo de un rebuild de imagen: segundos en
# vez de minutos, porque solo viaja el diff.
set -euo pipefail

DESTINO="${1:-${AURA_PI:-pi@raspberrypi.local}}"
RUTA="${AURA_RUTA:-~/aura-G15-IA}"

echo "==> Desplegando en ${DESTINO}:${RUTA}"

ssh "$DESTINO" bash -s <<EOSSH
set -euo pipefail
cd ${RUTA}
git pull --ff-only
source .venv/bin/activate
pip install -q -r requirements.txt
sudo systemctl restart aura
sleep 2
systemctl is-active aura
EOSSH

echo "==> Listo. Bitácora en vivo:  ssh ${DESTINO} 'journalctl -u aura -f'"
