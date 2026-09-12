# Sprites del robot virtual 2D

Un PNG con transparencia por estado. El enunciado exige representaciones
visuales **diferenciadas** para cada uno: un único asset estático con el estado
puesto solo como texto se califica como no entregado.

| Archivo            | Estado        | Cuándo se muestra                          |
|--------------------|---------------|--------------------------------------------|
| `espera.png`       | Esperando     | No hay persona en cuadro                   |
| `saludo.png`       | Saludo        | Persona aparece / mano levantada           |
| `deteccion.png`    | Detectando    | Persona presente, buscando gesto           |
| `interpretacion.png` | Interpretando | Gesto candidato, acumulando confianza      |
| `ejecucion.png`    | Ejecutando    | RPA o acción en curso                      |
| `exito.png`        | Éxito         | La acción terminó bien                     |
| `error.png`        | Error         | La acción falló                            |
| `despedida.png`    | Despedida     | La persona desaparece del cuadro           |

Tamaño sugerido: 512×512 px, fondo transparente, mismo encuadre del personaje
en todos para que el cambio de estado se lea como un cambio de pose y no como
un salto de posición.
