# Arquitectura

> Entregable calificado (2.1, 10 pts). Debe detallar arquitectura, diagramas de
> flujo y la explicación algorítmica de la detección espacial de landmarks.

## 1. Vista general

## 2. Flujo de datos

frame → landmarks → vector de características → gesto + confianza → decisión →
acción (RPA / Telegram) → resultado → overlay + estado del robot

## 3. Detección espacial de landmarks

Cómo se traducen las coordenadas de MediaPipe a cada gesto: ángulos, distancias
relativas y normalización respecto al tamaño de la persona en cuadro.

## 4. Máquina de estados del agente

## 5. Concurrencia

Qué corre en qué hilo (captura, inferencia, bot, RPA) y cómo se sincronizan.

## 6. Consumo de recursos en la Raspberry Pi
