# AURA — Augmented User Responsive Agent (grupo 15)

Agente reactivo que percibe gestos humanos con una cámara, los interpreta en la
Raspberry Pi, los muestra en una interfaz de realidad aumentada con un robot
virtual 2D, y a partir de ellos dispara procesos RPA y notificaciones por
Telegram.

Proyecto 2 de Inteligencia Artificial 1, Facultad de Ingeniería, USAC,
segundo semestre 2026. Enunciado en `docs/Proyecto 2 - 2S2026.pdf`.

**Equipo: lo que le toca a cada quien, fase por fase, está en
[docs/COMENZAR.md](docs/COMENZAR.md).**

**Entrega: 16 de octubre de 2026. Calificación: 17 de octubre de 2026.**

## Restricciones que anulan el proyecto

Estas tres no son preferencias de diseño, son rechazo inmediato con -100%:

1. **Todo corre nativo en la Raspberry Pi.** Nada de visión en la nube.
2. **Solo OpenCV y MediaPipe** como librerías de IA. Ninguna otra.
3. **Código propio.** Plagio o proyectos de semestres anteriores: 0 puntos y
   reporte a coordinación.

Y dos que descuentan fuerte:

- Cada comando de Telegram obligatorio que falte o falle: **-5%**.
- Video sin overlays de razonamiento (texto/cajas del agente): **-30%**.

## Arquitectura

```
┌──────────────┐   frames   ┌──────────────┐  landmarks  ┌──────────────┐
│   cámara     │ ─────────► │  percepción  │ ──────────► │    gestos    │
│  USB / CSI   │            │  MediaPipe   │             │  heurística  │
└──────────────┘            └──────────────┘             └──────┬───────┘
                                                                │ gesto + confianza
                                   ┌────────────────────────────┘
                                   ▼
                            ┌──────────────┐
                            │    agente    │  percibe → interpreta → decide → ejecuta
                            │ máquina de   │
                            │   estados    │
                            └──┬────────┬──┘
                               │        │
              estado + overlay │        │ acción
                               ▼        ▼
                     ┌──────────────┐  ┌──────────────┐
                     │   interfaz   │  │     rpa      │
                     │  AR + robot  │  │  Selenium    │
                     │   2D (cv2)   │  │  portal/UEDI │
                     └──────────────┘  └──────┬───────┘
                                              │ resultado
                                       ┌──────▼───────┐
                                       │   telegram   │ ◄──► usuario
                                       │  bot + cmds  │
                                       └──────────────┘
```

El bot de Telegram es **bidireccional**: recibe comandos que controlan al agente
(`/apagar`, `/addGesture`) y emite hacia el usuario lo que el agente decide.

## Estructura de carpetas

```
aura-G15-IA/
├── aura/                       # Paquete principal
│   ├── percepcion/             # Captura de cámara + MediaPipe (landmarks)
│   ├── gestos/                 # Clasificación geométrica de gestos
│   ├── interfaz/               # Overlays de AR + robot virtual 2D
│   ├── agente/                 # Máquina de estados, decisión, historial
│   ├── bot/                    # Bot de Telegram, handlers de los 13 comandos
│   ├── rpa/                    # Procesos automatizados (Selenium)
│   └── util/                   # Config, logging, métricas de CPU/RAM
├── assets/robot/               # Sprites 2D por estado (ver LEEME.md)
├── config/                     # config.json (ignorado: config.example.json es la plantilla)
├── datos/                      # Estado en runtime: historial, gestos, acciones (ignorado)
├── docs/                       # Manuales y diagramas — entregable calificado
├── scripts/                    # Instalación, arranque y despliegue en la Pi
├── deploy/                     # Servicio de systemd
├── tests/                      # Pruebas de la lógica de gestos y del agente
├── main.py                     # Punto de entrada del agente
├── requirements.txt
└── .env.example                # Token del bot y credenciales del RPA
```

## Los tres módulos

### Módulo 1 — Percepción, AR y robot virtual 2D

Motor de reconocimiento continuo con estas nueve reglas obligatorias:

| Percepción          | Interpretación     | Respuesta               |
|---------------------|--------------------|-------------------------|
| Persona aparece     | Usuario presente   | Saludar                 |
| Mano levantada      | Saludo             | Responder               |
| Pulgar arriba       | Aprobación         | Confirmar               |
| Pulgar abajo        | Rechazo            | Cambiar respuesta       |
| Señalar izquierda   | Dirección          | Mostrar opción izquierda|
| Señalar derecha     | Dirección          | Mostrar opción derecha  |
| Brazos cruzados     | Comando definido   | Ejecutar acción         |
| Persona se acerca   | Proximidad         | Activar interacción     |
| Persona desaparece  | Fin de interacción | Despedirse              |

El robot virtual 2D recorre: **Esperando → Detectando → Interpretando →
Ejecutando → Éxito/Error**, más saludo y despedida. Sprites distintos por
estado, integrados sobre el video en vivo. Sin 3D.

### Módulo 2 — Bot de Telegram (12 comandos obligatorios)

`/status` `/iniciar` `/apagar` `/history` `/gestures` `/addGesture`
`/deleteGesture` `/actions` `/addAction` `/linkAction` `/sendMessage` `/rpa`
`/logs`

### Módulo 3 — RPA

| Proceso             | Gesto                        | Significado            |
|---------------------|------------------------------|------------------------|
| Consultar horario   | ☝️ Índice hacia arriba        | Consultar / mostrar    |
| Descargar material  | 👇 Índice hacia abajo         | Descargar              |
| Completar formulario| ✍️ Simular escritura con índice | Ingresar información |

Flujo invariable, también para las funcionalidades opcionales:
**reconocer gesto → interpretar intención → ejecutar acción → presentar resultado**.

## Cronograma

| Fase | Actividad                                              | Inicio     | Fin        |
|------|--------------------------------------------------------|------------|------------|
| 1    | Planificación, hardware y entorno Linux en la Pi       | 11/09/2026 | 15/09/2026 |
| 2    | Visión computacional, MediaPipe y detección de gestos  | 16/09/2026 | 29/09/2026 |
| 3    | Bot de Telegram, handlers y vinculación de comandos    | 30/09/2026 | 08/10/2026 |
| 4    | Flujos RPA y estabilización de consumo de recursos     | 09/10/2026 | 14/10/2026 |
| 5    | Pruebas integrales, video demostrativo y documentación | 15/10/2026 | 16/10/2026 |
| —    | Evaluación técnica y defensa oral                      | 17/10/2026 | 17/10/2026 |

## Entregables

| Tipo                 | Qué                                                         | Formato    |
|----------------------|-------------------------------------------------------------|------------|
| Código fuente        | Repositorio con dependencias y scripts de ejecución          | GitHub     |
| Documentación técnica| Arquitectura, flujo de datos, procesos RPA, manual del bot   | Markdown   |

Repositorio: `[IA1]Proyecto2_GRUPO15_2S2026_SECA` (sección A, tutores roberto1206
y JavierB20). **Cada integrante entrega el proyecto de forma individual en UEDI**
(y también en Classroom si es del tutor 2).

## Rúbrica (100 pts)

| Área                            | Puntos |
|---------------------------------|--------|
| Realidad Aumentada              | 50     |
| Integración Telegram            | 20     |
| Implementación RPA              | 10     |
| Documentación técnica           | 10     |
| Defensa del proyecto (preguntas)| 10     |

Habilidades 80 / Conocimientos 20. El punteo más grande, con diferencia, está en
que la AR se vea fluida y muestre el razonamiento del agente.

## Puesta en marcha

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # y llenar el token del bot
cp config/config.example.json config/config.json
python main.py
```

## Despliegue en la Raspberry Pi

Se corre nativo, sin contenedores. Docker se evaluó y se descartó: las laptops
del equipo son x86 y la Pi es ARM, así que una imagen construida en la laptop no
arranca en la Pi — habría que construirla en la Pi de todos modos. A eso se suma
el passthrough de cámara y de la ventana de X11, que son justo el módulo que
vale 50 puntos.

Una sola vez, en la Pi:

```bash
git clone <repo> ~/aura-G15-IA && cd ~/aura-G15-IA
./scripts/instalar_pi.sh            # paquetes, venv, y verifica OpenCV, MediaPipe y cámara
sudo cp deploy/aura.service /etc/systemd/system/
sudo systemctl enable --now aura
```

Después, cada cambio viaja en un comando desde cualquier laptop:

```bash
./scripts/desplegar.sh pi@raspberrypi.local
```

Bitácora en vivo: `ssh pi@raspberrypi.local 'journalctl -u aura -f'`
