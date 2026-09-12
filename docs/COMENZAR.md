# Qué le toca a cada quien

Todo lo que hay que hacer de aquí al 16 de octubre, repartido entre los cinco.
Lee el Paso 0 y después salta directo a tu sección.

El enunciado está en `Proyecto 2 - 2S2026.pdf`. Si querés el razonamiento
detrás del reparto y los riesgos, está en [PLANIFICACION.md](PLANIFICACION.md).

---

## Paso 0 — Esto lo hacemos todos

```bash
git clone git@github.com:Alexder14/-IA1-Proyecto2_GRUPO15_2S2026_SECA.git aura
cd aura
cp config/config.example.json config/config.json
cp .env.example .env
```

Y de ahí, con Docker (recomendado) o nativo.

**Con Docker.** Nos da a los cinco las mismas versiones, sin pelear con la
instalación de MediaPipe en cada laptop:

```bash
./scripts/dev.sh                        # shell sin cámara: para el bot y el RPA
./scripts/dev.sh cam                    # con cámara y ventana: para visión
pytest                                  # adentro del contenedor: pasan 13
```

`dev.sh cam` necesita `/dev/video0` y una sesión gráfica, así que funciona en
Linux. En Windows con WSL2 la cámara requiere `usbipd` y es frágil; en macOS
Docker no tiene passthrough de cámara y no hay forma de hacerlo funcionar. Si
estás en alguno de esos dos, trabajá la parte de visión de forma nativa.

**Nativo**, si preferís o si Docker no te sirve:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest                                  # tienen que pasar 13
```

**Ojo con una confusión:** que MediaPipe instale en el contenedor NO significa
que instale en la Pi. En tu laptop se baja el wheel de x86 y en la Pi el de ARM:
son archivos distintos con el mismo número de versión. El riesgo sigue vivo
hasta que P5 lo pruebe en la Pi.

### Git

Trabajamos sobre `development`. A `main` no sube nada hasta el último día.

```bash
git checkout development && git pull
git checkout -b 201020600-percepcion   # tu carné + qué estás haciendo
# trabajás, commiteás
git push -u origin 201020600-percepcion
# y abrís un PR hacia development
```

Una rama por tarea. Commits de una línea que digan qué cambió. Antes de pedir
revisión, `pytest` en verde.

### Dónde está lo tuyo

El esqueleto ya tiene todas las firmas escritas. Para encontrar las tuyas:

```bash
grep -rn "P3" aura/          # cambiá P3 por el tuyo
```

Cada función pendiente dice `NotImplementedError("Fase N — PX")`.

### Tres cosas que no se negocian

1. **Solo OpenCV y MediaPipe.** Instalar otra librería de IA es -100%. Si creés
   que hace falta una, lo consultás en el grupo antes de escribir el import.
2. **Nada en la nube.** Todo el procesamiento corre en la Pi.
3. **`aura/contratos.py` no se toca sin avisar.** Es lo que nos permite trabajar
   en paralelo; si cambiás una firma ahí, le rompés el trabajo a alguien más.

### El calendario

| Fase | Cierra | Día | Qué se cierra |
|------|--------|-----|---------------|
| 1 | 18/09 | viernes | La Pi enciende la cámara y dibuja landmarks |
| 2 | 02/10 | viernes | Gesto → el robot cambia de estado → el panel muestra el razonamiento |
| 3 | 09/10 | viernes | Los 13 comandos de Telegram responden |
| 4 | 14/10 | miércoles | Gesto → RPA → resultado mostrado al usuario |
| 5 | 16/10 | viernes | Video, documentación y **entrega** |
| — | 17/10 | sábado | Defensa |

Los cierres caen en viernes a propósito: nos juntamos ese día a ver la demo y a
repartir la fase siguiente.

**Una fecha no se mueve:** el **martes 15/09** MediaPipe tiene que estar
corriendo en la Raspberry Pi. No es el cierre de la Fase 1, es un control antes.
Si ese día no corre, el grupo entero se dedica a eso hasta que corra, porque no
hay librería de reemplazo permitida.

> Este calendario corre tres días respecto al del enunciado, para que los cierres
> caigan en viernes. La fecha de entrega es la misma, **16/10**, que es la única
> que no depende de nosotros. Los tres días salieron de las fases 3 y 4, no de la
> 2, porque la Fase 2 es la del módulo que vale 50 puntos.

---

# P1 — Percepción e integración

Tus carpetas: `aura/percepcion/`, `aura/interfaz/ventana.py` y `main.py`. Sos
además el que arma las piezas de los demás, así que el bucle principal es tuyo.

### Fase 1 · 11–18/09

1. `Camara` en `aura/percepcion/camara.py`. Abrir la cámara con OpenCV y leer
   frames **en un hilo aparte**, guardando siempre el último. Si la lectura y el
   procesamiento comparten hilo, el video se congela.
2. `registro.configurar()` en `aura/util/registro.py`. Logging a consola y a
   `datos/aura.log`.
3. `construir()` y `bucle()` en `main.py`. Que abra una ventana y muestre el
   video. Sin MediaPipe todavía.
4. Revisar `aura/contratos.py` y avisar al grupo si algo hay que cambiar. Después
   de esta semana esas firmas ya no se mueven.

Cierra cuando `python main.py` abre una ventana con video fluido y sale con `q`.

### Fase 2 · 19/09–02/10

1. `Extractor` en `landmarks.py`. MediaPipe Hands y Pose, cargados una sola vez
   (en la Pi tardan varios segundos en inicializar).
2. `ContadorFPS` en `metricas.py`, y dibujar el número en pantalla mientras
   desarrollamos.
3. Meter el clasificador de P2 y la interfaz de P3 en el bucle.
4. Optimizar. Si no llegás a unos 15 FPS en la Pi: bajar resolución de entrada,
   correr Pose cada N frames en vez de cada uno, achicar el modelo.

Cierra cuando la Pi corre el pipeline completo sin que se note lag.

### Fase 3 · 03/10–09/10

1. `/iniciar` y `/apagar` tienen que controlar el bucle de verdad, no una
   variable suelta. Coordinalo con P4.
2. Revisar los PR de los demás. Esta fase todos están tocando cosas que se
   cruzan y alguien tiene que ver el conjunto.

### Fase 4 · 10–14/10

1. Dejarlo corriendo dos horas seguidas y ver qué pasa con la RAM. Si sube y no
   baja, hay fuga y casi siempre está en los frames que no se liberan.
2. Que un proceso RPA corriendo no congele el video. Va en otro hilo.
3. Ajustar `config.json` con los valores que de verdad funcionaron en la Pi.

### Fase 5 · 15–16/10

Congelar el repo. `requirements.txt` con lo que realmente está instalado en la
Pi, instrucciones de ejecución probadas desde cero, y el merge final a `main`.

---

# P2 — Clasificación de gestos

Tu carpeta: `aura/gestos/`. Todo es geometría sobre coordenadas, no hay que
entrenar nada (y el enunciado tampoco lo permitiría).

### Fase 1 · 11–18/09

No necesitás esperar a P1. Lo que necesitás son datos.

1. Grabá landmarks de los 12 gestos. Un script corto con MediaPipe que imprima
   las coordenadas y las guarde en `tests/datos/<gesto>.json`. Varias muestras
   por gesto, con distintas personas y a distintas distancias de la cámara.
2. Empezá por `geometria.py`: `distancia()`, `angulo()` y `dedo_extendido()`. Son
   geometría pura y se prueban sin cámara.
3. Escribí las pruebas en `tests/test_gestos.py` usando esos JSON.

Cierra cuando `pytest tests/test_gestos.py` reconoce al menos tres gestos desde
landmarks grabados, sin abrir la cámara.

### Fase 2 · 19/09–02/10

1. Los nueve obligatorios. Los de mano salen de Hands; brazos cruzados, persona
   presente y proximidad salen de Pose.
2. Los tres del RPA: índice arriba, índice abajo y simular escritura.
3. `Clasificador.evaluar()` con los dos filtros que importan: confirmar el gesto
   después de N frames seguidos, y enfriar después de dispararlo. Sin eso, a 15
   FPS un pulgar arriba sostenido lanza la acción quince veces por segundo.
4. `candidato()`, que devuelve lo que se está viendo sin confirmar todavía. P3 lo
   usa para el estado "interpretando", que es lo que hace que se vea que AURA
   está pensando y no solo reaccionando.

Ojo con `escala_corporal()`: normalizá las distancias contra el ancho de hombros
para que un gesto se detecte igual de cerca que de lejos.

### Fase 3 · 03/10–09/10

`personalizados.py`, que es lo que consumen `/addGesture`, `/deleteGesture` y
`/gestures`. La idea más simple que cumple: `/addGesture` guarda la posición
actual de los landmarks como plantilla, y el clasificador compara por distancia
contra ella. Tiene que recargarse en caliente, sin reiniciar el agente.

### Fase 4 · 10–14/10

Pruebas largas con gente distinta. Anotá los falsos positivos y ajustá umbrales.
Es aburrido y es lo que separa una demo que funciona de una que se traba.

### Fase 5 · 15–16/10

Escribir cómo funciona cada gesto para `ARQUITECTURA.md`. La rúbrica pide
explícitamente una explicación algorítmica de la detección espacial de
landmarks, y esa parte la escribís vos.

---

# P3 — Interfaz de realidad aumentada y robot 2D

Tus carpetas: `aura/interfaz/` y `assets/robot/`. Tu módulo vale **50 de los 100
puntos**, más otro 30% que se descuenta si el video no muestra el razonamiento.
Es la parte más cara del proyecto.

### Fase 1 · 11–18/09

1. **Los 8 sprites, y es lo primero.** Sin ellos el Módulo 1 no se puede
   evaluar. La tabla de estados está en `assets/robot/LEEME.md`. Pueden ser
   dibujados, generados o de un pack libre, pero tienen que ser **ocho imágenes
   distintas del mismo personaje**. Un solo asset estático con el estado puesto
   nada más en texto no vale, y 3D tampoco.
2. `RobotVirtual.cargar()` y `dibujar()`, componiendo el PNG sobre el frame con
   el canal alfa.
3. Una primera versión del panel de razonamiento.

No esperés a P1 ni a P2. Armate un frame falso:

```python
import numpy as np
from datetime import datetime
from aura.contratos import EstadoAura, EstadoRobot, Frame, Gesto

frame = Frame(imagen=np.zeros((480, 640, 3), np.uint8), timestamp=datetime.now())
estado = EstadoAura(
    estado=EstadoRobot.INTERPRETANDO,
    gesto=Gesto.PULGAR_ARRIBA,
    confianza=0.94,
    interpretacion="Aprobación",
    accion="Confirmar",
)
```

Cierra cuando una imagen de prueba muestra el robot, la caja, el gesto, la
confianza, la interpretación y la acción, y se entiende de un vistazo qué está
pensando AURA.

### Fase 2 · 19/09–02/10

1. `Overlay` completo: landmarks, bounding box de la persona, gesto detectado,
   nivel de confianza, interpretación y acción a ejecutar.
2. Legibilidad. El panel se va a ver en un video grabado con celular, así que
   contraste fuerte, texto grande, y que no tape la cara de la persona.
3. Las transiciones del robot conectadas a los estados reales del agente.

### Fase 3 · 03/10–09/10

Pulir con lo que salga de las pruebas de los demás. Esta fase te toca más
liviana; si te sobra tiempo, ayudá a P4 con las pruebas de los comandos.

### Fase 4 · 10–14/10

Conectar ejecución, éxito y error al resultado real del RPA. Un proceso puede
tardar veinte segundos, así que el estado "ejecutando" tiene que verse vivo, no
congelado.

### Fase 5 · 15–16/10

El video lo graba P5 pero el encuadre es tuyo: que se vea el panel, que se lean
los textos, que el cambio de estado del robot se note. Eso es lo que califican.

---

# P4 — Núcleo del agente y bot de Telegram

Tus carpetas: `aura/agente/`, `aura/bot/` y `aura/util/recursos.py`.

Son 13 comandos y cada uno que falte o falle vale -5%. Juntos son el 65% del
proyecto en descuentos. Están todos declarados en `comandos.py` y
`tests/test_comandos.py` verifica que no falte ninguno.

### Fase 1 · 11–18/09

1. Crear el bot en BotFather. Token en `.env` y tu `TELEGRAM_CHAT_ID` también:
   el bot solo debe atender ese chat, porque estos comandos apagan servicios de
   la Pi.
2. `recursos.medir()` con psutil: CPU, RAM, temperatura y uptime.
3. `/status` funcionando de punta a punta.

Cierra cuando le escribís `/status` desde el teléfono y responde con números
reales de la máquina donde corre. Simulados no sirven, la rúbrica lo castiga.

### Fase 2 · 19/09–02/10

1. `Agente` en `nucleo.py`: la máquina de estados. Recibe un `EventoGesto`,
   decide, ejecuta, y publica el estado para que P3 lo dibuje.
2. `historial.py`, persistido en disco para que sobreviva a un reinicio.
3. El mecanismo de suscripción, que es como la interfaz y el bot se enteran de
   los cambios sin preguntarle al agente todo el tiempo.

Tampoco esperés a nadie, probalo con eventos inventados:

```python
from datetime import datetime
from aura.contratos import EventoGesto, Gesto

agente.procesar(EventoGesto(Gesto.PULGAR_ARRIBA, 0.94, datetime.now()))
```

### Fase 3 · 03/10–09/10

Es tu fase pesada. Los 13 comandos:

`/status` `/iniciar` `/apagar` `/history` `/gestures` `/addGesture`
`/deleteGesture` `/actions` `/addAction` `/linkAction` `/sendMessage` `/rpa`
`/logs`

Más `acciones.py`, que es lo que hace posible `/linkAction`: un gesto no sabe
qué hace, solo sabe a qué acción está vinculado. Esa indirección es la que
permite reasignar qué hace cada gesto sin tocar código.

Y las notificaciones hacia el usuario, con criterio: a 15 FPS no se puede
reenviar todo, solo lo que a una persona le importa.

**El 09/10 probamos los 13 comandos uno por uno, con la lista en la mano.**

### Fase 4 · 10–14/10

Cerrar el circuito con P5: gesto → acción → RPA → respuesta por Telegram. Que el
resultado le llegue al usuario, no que se quede en un log.

### Fase 5 · 15–16/10

`MANUAL_BOT.md` con ejemplos de uso reales, y probar los 13 comandos otra vez en
la Pi ya con todo integrado.

---

# P5 — RPA, infraestructura y documentación

Tus carpetas: `aura/rpa/`, `scripts/` y `docs/`. Tu carga es fuerte esta semana
y en octubre, liviana en medio. Es a propósito.

### Fase 1 · 11–18/09 — lo más urgente del grupo

**Que MediaPipe corra en la Raspberry Pi.**

```bash
# en la Pi
git clone git@github.com:Alexder14/-IA1-Proyecto2_GRUPO15_2S2026_SECA.git aura
cd aura && ./scripts/instalar_pi.sh
```

El script verifica al final arquitectura, OpenCV, MediaPipe y cámara.

Si eso falla, es el único tema del grupo hasta que funcione. No hay plan B: el
enunciado solo permite OpenCV y MediaPipe, así que si no instalan en ARM no hay
proyecto. Probá otras versiones en `requirements.txt` y decinos cuál sirvió.

Después:

1. Instalar el servicio: `sudo cp deploy/aura.service /etc/systemd/system/`
2. **Respaldar la imagen de la microSD** apenas la Pi funcione. Si se corrompe a
   mitad de octubre, ese respaldo nos salva el semestre.

### Fase 2 · 19/09–02/10

`ARQUITECTURA.md` y los diagramas de flujo, mientras los demás construyen. Vas
documentando lo que ves que hacen, que es más fácil que reconstruirlo en
octubre.

### Fase 3 · 03/10–09/10

1. **Pedirle a los auxiliares el formulario y las credenciales del RPA.** Esta
   fase, no la siguiente. Si llegan tarde son 10 puntos perdidos y no hay cómo
   recuperarlos.
2. Dejar Chromium y chromedriver funcionando en la Pi, y probar que Selenium
   abre una página desde ahí.
3. `MANUAL_TECNICO.md`.

### Fase 4 · 10–14/10

Los tres procesos:

1. **Consultar horario** (índice arriba). Entrar al portal académico, llegar al
   curso y sacar el horario de magistral y de laboratorio.
2. **Descargar material** (índice abajo). Entrar a UEDI, ubicar el recurso y
   descargar el enunciado. Verificá el archivo en disco, no solo que el clic no
   tronara.
3. **Completar formulario** (simular escritura). Llenar los campos con lo que hay
   en el sistema y **validar que los requeridos quedaron completos antes de
   enviar** — el enunciado lo pide explícitamente.

Los tres van en un hilo aparte y devuelven un mensaje legible por una persona,
porque ese texto termina en el overlay y en un chat de Telegram.

### Fase 5 · 15–16/10

El video demostrativo y cerrar la documentación. Que en el video se vean los
overlays de razonamiento: si no, son -30% sin discusión.

---

## Antes de entregar — 16/10

Lo revisamos juntos, no cada quien por su lado.

- [ ] Corre en la Raspberry Pi, nativo
- [ ] No hay ninguna librería de IA aparte de OpenCV y MediaPipe
- [ ] Los 9 gestos obligatorios se detectan
- [ ] El robot 2D tiene 8 sprites distintos y cambia de estado
- [ ] El panel de razonamiento se ve en pantalla y en el video
- [ ] Los 13 comandos responden
- [ ] `/status` muestra datos reales de la Pi
- [ ] Los 3 procesos RPA se disparan desde un gesto y devuelven resultado
- [ ] `README.md`, `ARQUITECTURA.md`, `MANUAL_TECNICO.md` y `MANUAL_BOT.md` al día
- [ ] `requirements.txt` coincide con lo instalado en la Pi
- [ ] El video muestra los overlays
- [ ] `development` fusionado a `main`
- [ ] **Cada uno entregó por su cuenta en UEDI** (y en Classroom los del tutor 2)

## El 17/10

La defensa vale 10 puntos y es individual. Preguntan de todo, no solo de tu
módulo. Lo que más cae: cómo funciona MediaPipe, cómo se manejan los recursos en
Linux y cómo está orquestado el código. El que no sepa explicar su parte pierde
sus puntos aunque el proyecto funcione perfecto.
