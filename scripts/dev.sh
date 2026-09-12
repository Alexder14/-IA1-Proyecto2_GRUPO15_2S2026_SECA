#!/usr/bin/env bash
# Abre una shell en el contenedor de desarrollo.
#
#   ./scripts/dev.sh          # sin cámara: para el bot y el RPA
#   ./scripts/dev.sh cam      # con cámara y ventana: para visión
#
# Esto es SOLO para desarrollar en tu laptop. En la Raspberry Pi el agente
# corre nativo; ver scripts/instalar_pi.sh.
set -euo pipefail
cd "$(dirname "$0")/.."

# HOST_UID y no UID: en bash UID es de solo lectura y exportarla revienta el
# script en algunas shells.
export HOST_UID="$(id -u)"
export HOST_GID="$(id -g)"
export VIDEO_GID="$(getent group video | cut -d: -f3)"
: "${VIDEO_GID:=44}"

if [[ "${1:-}" == "cam" ]]; then
    if [[ ! -e /dev/video0 ]]; then
        echo "No hay /dev/video0. Conectá la cámara o usá ./scripts/dev.sh sin 'cam'." >&2
        exit 1
    fi
    # Permitir que el contenedor dibuje en tu sesión gráfica.
    if command -v xhost >/dev/null; then
        xhost +local:docker >/dev/null
        trap 'xhost -local:docker >/dev/null 2>&1 || true' EXIT
    fi
    exec docker compose run --rm aura-cam "${@:2}"
fi

exec docker compose run --rm aura "$@"
