# Planificación — AURA (5 integrantes)

Proyecto 2, IA1, 2S2026. Entrega **16/10/2026**, defensa **17/10/2026**.
Hoy es viernes 11/09/2026: primer día de la Fase 1. Son **5 semanas**.

Movimos los cierres de fase a viernes, así que este calendario corre tres
días respecto al del enunciado. La entrega es la misma. Los tres días los
sacamos de las fases 3 y 4; la Fase 2 se queda con sus 14 días porque es la
del módulo que vale 50 puntos.

Estimado del enunciado: 70 hrs por persona ≈ **14 hrs/semana**.

---

## 1. De dónde sale el reparto: la rúbrica

| Área                             | Pts | Quién responde |
|----------------------------------|-----|----------------|
| Realidad Aumentada (visualización)| 50 | P1 + P2 + P3   |
| Integración y control por Telegram| 20 | P4             |
| Implementación de RPA             | 10 | P5             |
| Documentación técnica             | 10 | P5 coordina, todos escriben lo suyo |
| Defensa del proyecto (preguntas)  | 10 | todos, individual |
| **Total**                         |100 |                |

La mitad del punteo está en que el video se vea fluido y muestre el
razonamiento del agente. Por eso **3 de 5 personas van al Módulo 1**, no una.

Ojo con los descuentos, que son más caros que varias tareas juntas:

- Correr fuera de la Raspberry Pi → **-100%**
- Librería de IA que no sea OpenCV o MediaPipe → **-100%**
- Plagio o proyecto de semestre anterior → **0 pts + reporte**
- Cada comando de Telegram faltante o defectuoso → **-5%** (son 13: hasta -65%)
- Sin overlays de razonamiento en el video → **-30%**

---

## 2. Roles

### P1 — Percepción e integración (*el que arma el bucle*)
Captura de cámara, pipeline de MediaPipe, extracción de landmarks, hilos y
rendimiento (FPS, CPU, RAM). Es además el **integrador**: dueño de `main.py`,
de armar las piezas de los demás y de resolver conflictos de merge.

- `aura/percepcion/`, `main.py`
- Métrica de la que responde: **FPS estables en la Pi sin lag visible** (la
  rúbrica dice literal "de forma clara y sin lag evidente").

### P2 — Clasificación de gestos
Geometría sobre landmarks: ángulos, distancias relativas, normalización por
tamaño de la persona en cuadro. Los 9 gestos obligatorios del Módulo 1 más los
3 del RPA, confianza, *debounce* (N frames para confirmar) y enfriamiento para
que un gesto no se dispare 30 veces por segundo. También el registro dinámico
que consume `/addGesture`.

- `aura/gestos/`
- Métrica: **cada gesto se detecta y no se auto-dispara**.

### P3 — Interfaz AR + robot virtual 2D
Overlays sobre el video: bounding boxes, landmarks, gesto detectado, nivel de
confianza, interpretación y acción a ejecutar. Y el robot 2D con sprites
distintos por estado (esperando, saludo, detección, interpretación, ejecución,
éxito, error, despedida).

- `aura/interfaz/`, `assets/robot/`
- Métrica: **el panel de razonamiento se ve en el video** (si no, -30%).
- Trampa: un solo asset estático cambiando solo el texto **no es válido**.
  Tampoco 3D. Necesita conseguir o dibujar 8 sprites — que empiece por eso.

### P4 — Núcleo del agente + bot de Telegram
La máquina de estados (percibe → interpreta → decide → ejecuta), el historial,
la persistencia de gestos/acciones/vínculos, y los 13 comandos. 10 de los 13
comandos son CRUD sobre ese estado, por eso van con la misma persona.

- `aura/agente/`, `aura/bot/`
- Métrica: **los 13 comandos responden**, y `/status` lee CPU/RAM reales de la
  Pi con `psutil`, no valores simulados (la rúbrica castiga respuestas estáticas).

### P5 — RPA + infraestructura de la Raspberry Pi + documentación
Fase 1 monta la Pi (SO, venv, OpenCV, MediaPipe, cámara, systemd). Fases 2–3
escribe documentación y prepara el video. Fase 4 implementa los 3 procesos RPA.
Su carga es pesada al inicio y al final, ligera en medio — a propósito.

- `aura/rpa/`, `scripts/`, `docs/`
- Métrica: **los 3 procesos RPA se disparan desde un gesto y devuelven resultado**.

---

## 3. El contrato entre módulos (lo más importante de la Fase 1)

Con 5 personas, lo que mata el proyecto no es la dificultad técnica sino que
todos se bloqueen esperando al de al lado. La forma de evitarlo es acordar
**el día 1** las estructuras de datos que cruzan los módulos, y que cada quien
programe contra ellas con datos falsos hasta que el otro termine.

```
Percepción → Gestos     Frame(imagen, landmarks_mano, landmarks_pose, timestamp)
Gestos → Agente         EventoGesto(nombre, confianza, timestamp, metadatos)
Agente → Interfaz       EstadoAura(estado, gesto, confianza, interpretacion,
                                   accion, resultado)
Agente → RPA            ejecutar(accion, parametros) -> ResultadoRPA(ok, mensaje, datos)
Agente ↔ Telegram       comandos entran, eventos salen
```

Con esto:

- P3 dibuja la interfaz alimentándola de un `EstadoAura` inventado, sin cámara.
- P4 prueba los comandos con un agente falso, sin visión.
- P5 prueba el RPA llamándolo directo, sin gestos.
- P2 prueba los gestos con landmarks grabados en un JSON, sin cámara.

Estas firmas las define **P1 el 11–12/09** y se congelan. Cambiarlas después
requiere avisar al grupo.

---

## 4. Plan por fases

### Fase 1 — 11/09 a 18/09 · Planificación, hardware y entorno

| Quién | Qué |
|-------|-----|
| P5 | **Prioridad absoluta, con fecha dura el martes 15/09:** instalar MediaPipe en la Pi y comprobar que corre |
| P1 | Definir el contrato de datos, esqueleto del repo, `main.py` con hilos |
| P2 | Capturar landmarks de referencia de los 12 gestos (JSON para pruebas) |
| P3 | Conseguir/dibujar los 8 sprites del robot |
| P4 | Crear el bot en BotFather, token, `/status` funcionando |
| Todos | Acordar convenciones de Git y ramas |

**Riesgo #1 del proyecto:** MediaPipe en ARM. No todas las versiones tienen
*wheel* para Raspberry Pi y **no hay plan B**, porque el enunciado solo permite
OpenCV y MediaPipe. Si el 15/09 no corre en la Pi, eso pasa a ser el único tema
del grupo hasta que corra. No dejarlo para la Fase 2.

**Cierre de fase:** la Pi muestra el video en pantalla, en vivo y sin lag.

Los landmarks no entran acá: dibujarlos necesita el extractor de MediaPipe, que
es Fase 2. Adelantarlo antes de que P5 confirme que MediaPipe instala en ARM
sería construir sobre algo que quizás haya que rehacer.

### Fase 2 — 19/09 a 02/10 · Visión, MediaPipe y detección de gestos (2 semanas)

La fase más larga y la que vale 50 pts.

| Quién | Qué |
|-------|-----|
| P1 | Pipeline de captura + inferencia optimizado; medir FPS y RAM |
| P2 | Los 9 gestos obligatorios + los 3 del RPA, con confianza y enfriamiento |
| P3 | Overlays completos y robot 2D cambiando de estado |
| P4 | Máquina de estados del agente, historial y persistencia |
| P5 | `docs/ARQUITECTURA.md` y diagramas de flujo |

**Cierre de fase (02/10):** demo de punta a punta sin Telegram y sin RPA — hago
un gesto, el robot cambia de estado y el panel muestra qué percibió, qué
interpretó y qué decidió.

### Fase 3 — 03/10 a 09/10 · Bot de Telegram

| Quién | Qué |
|-------|-----|
| P4 | Los 13 comandos, comunicación bidireccional con el agente |
| P2 | `/addGesture` y `/deleteGesture` contra el clasificador |
| P1 | `/iniciar` y `/apagar` controlando el bucle de verdad |
| P3 | Pulir la interfaz con lo que salga de las pruebas |
| P5 | `docs/MANUAL_BOT.md` y preparar el entorno del RPA (credenciales, formulario) |

**Cierre de fase (09/10):** los 13 comandos responden. Probarlos uno por uno
con la lista en mano: cada uno vale 5% del proyecto.

### Fase 4 — 10/10 a 14/10 · RPA y estabilización

| Quién | Qué |
|-------|-----|
| P5 | Consultar horario, descargar material, completar formulario |
| P4 | Vincular gesto → acción → RPA → respuesta por Telegram |
| P1 | Estabilizar consumo: fugas de memoria, umbrales, horas de ejecución continua |
| P2 | Ajustar umbrales con los falsos positivos que aparezcan en pruebas largas |
| P3 | Estados de ejecución/éxito/error del robot conectados al resultado real |

**Cierre de fase (14/10):** gesto → RPA → resultado mostrado al usuario.

### Fase 5 — 15/10 a 16/10 · Pruebas, video y documentación

| Quién | Qué |
|-------|-----|
| Todos | Prueba integral en la Pi, corrida larga |
| P5 | Grabar el video demostrativo y cerrar la documentación |
| P1 | Congelar el repo, `requirements.txt`, instrucciones de ejecución |
| Todos | **Entregar individualmente en UEDI** (y en Classroom si son del tutor 2) |

**El video debe mostrar los overlays de razonamiento.** Sin eso, -30%.

### 17/10 — Defensa

Cada quien responde por su módulo, pero preguntan de todo. Los 10 pts de
defensa son individuales: el que no sepa explicar MediaPipe, el uso de recursos
en Linux o cómo se orquesta el código, pierde sus puntos aunque el proyecto
funcione.

---

## 5. Reglas de trabajo

1. **Todo se prueba en la Pi.** Que funcione en tu laptop no cuenta; correr
   fuera de la Pi es -100%. Mínimo una prueba en la Pi por semana, por persona.
2. **Una rama por persona**, PR a `develop`, y `main` solo con lo que corre.
3. **Reunión de 15 min, dos veces por semana.** Qué hice, qué me bloquea.
4. **Cero librerías de IA nuevas.** Si alguien va a instalar algo, lo consulta
   con el grupo antes. Una sola importación equivocada anula el proyecto.
5. **Nadie espera a nadie**: si tu módulo depende de otro, programá contra el
   contrato con datos falsos.

---

## 6. Riesgos

| Riesgo | Impacto | Qué hacemos |
|--------|---------|-------------|
| MediaPipe no instala en la Pi | Proyecto inviable | Validar en los primeros 2 días |
| La Pi no da los FPS necesarios | -50 pts (lag evidente) | Bajar resolución, saltar frames, medir desde Fase 2 |
| Sprites del robot sin conseguir | Rechazo del Módulo 1 | P3 los tiene el 18/09 |
| Credenciales/formulario del RPA no llegan | -10 pts | P5 los pide a los auxiliares en Fase 3, no en Fase 4 |
| Un comando de Telegram a medias | -5% cada uno | Lista de verificación el 09/10 |
| Una sola Pi para 5 personas | Cuello de botella | Calendario de uso; el resto trabaja con datos falsos |
