# Entorno de desarrollo de AURA.
#
# Sirve para que los cinco trabajemos con las mismas versiones y se acabe el
# "a mí no me instala MediaPipe". NO es la forma de desplegar en la Raspberry
# Pi: allá el código corre nativo con systemd (ver scripts/instalar_pi.sh).
#
# La imagen base es multiarquitectura, así que también construye en la Pi si
# alguna vez hiciera falta. Python 3.11 es la versión que trae Raspberry Pi OS
# Bookworm, y la idea es desarrollar contra lo mismo que corre allá.

FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# libgl1 y libglib son de OpenCV; el resto son las X11 que necesita la ventana
# de cv2.imshow. chromium y su driver los usa el RPA de P5.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libxcb1 \
        libxkbcommon0 \
        libdbus-1-3 \
        libgomp1 \
        v4l-utils \
        chromium \
        chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Mismas versiones que la Pi. Si este archivo y el de allá se separan,
# aparecen bugs que solo se ven en la Pi.
WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip && pip install -r requirements-dev.txt

# Usuario con el mismo UID del host: si no, los archivos que cree el contenedor
# quedan como root en tu carpeta y después no los podés editar.
ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" aura 2>/dev/null || true \
    && useradd -m -u "${UID}" -g "${GID}" aura 2>/dev/null || true \
    && mkdir -p /app/datos && chown -R "${UID}:${GID}" /app

USER ${UID}:${GID}

CMD ["bash"]
