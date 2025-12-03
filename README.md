# 🎮 SkyRunner - Runner Vertical 2D

**Proyecto de  Fundamentos de Informática Gráfica**

## 📋 Descripción

SkyRunner es un juego de plataformas vertical desarrollado en Python con Pygame. El jugador debe ascender a través de tres niveles temáticos, esquivando enemigos, superando obstáculos y recolectando power-ups mientras aplica conceptos avanzados de informática gráfica.

---

## 🎯 Características Principales

### ✨ Conceptos de Informática Gráfica Implementados

1. **Transformaciones Geométricas**
   - **Traslación**: Movimiento del jugador, enemigos, plataformas móviles y parallax scrolling
   - **Rotación**: Enemigos rotantes (murciélagos, trampas), efectos visuales
   - **Escalado**: Power-up de zoom que aumenta el tamaño del jugador

2. **Sistema de Vidas 2D**
   - Cámara con seguimiento suave (smooth following)
   - Viewport de 800x600 píxeles
   - Proyección ortográfica 2D
   - Sistema de layers (fondo → plataformas → enemigos → jugador → UI)

3. **Animaciones e Interpolación**
   - Interpolación lineal (lerp) para movimientos suaves
   - Movimiento sinusoidal para enemigos
   - Parallax scrolling en múltiples capas
   - Efectos de partículas

4. **Física Simulada**
   - Gravedad y aceleración
   - Detección de colisiones (AABB)
   - Movimiento con inercia y fricción

### 🎵 Nuevas Características (Mejoras)

5. **Sistema de Audio**
   - Efectos de sonido sintéticos (salto, daño, power-up)
   - Sonidos generados proceduralmente con ondas sinusoidales
   - Control de volumen

6. **Sistema de Vidas**
   - 3 vidas por partida
   - Regeneración de salud al perder vida
   - Invulnerabilidad temporal

7. **High Scores**
   - Tabla de mejores puntuaciones (Top 10)
   - Guardado persistente en archivo JSON
   - Entrada de nombre del jugador
   - Ranking con fecha y nivel alcanzado

---

## 📁 Estructura del Proyecto

```
skyrunner/
│
├── main.py           # Punto de entrada del juego
├── game.py           # Loop principal y coordinación
├── player.py         # Lógica del jugador
├── enemies.py        # Clases de enemigos (Bat, Trap, Rock, Lightning)
├── platform.py       # Plataformas normales y móviles
├── powerup.py        # Power-ups y efectos de recolección
├── level.py          # Generador y gestor de niveles
├── utils.py          # Funciones auxiliares (lerp, rotación, etc.)
├── constants.py      # Constantes del juego
├── audio.py          # Sistema de audio y efectos de sonido ⭐ NUEVO
├── highscores.py     # Gestor de puntuaciones altas ⭐ NUEVO
├── highscores.json   # Archivo de puntuaciones (generado automáticamente)
└── README.md         # Este archivo
```

---

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| ⬅️ → o A D | Mover izquierda/derecha |
| ESPACIO | Saltar (doble salto disponible) |
| ESC | Pausar juego / Volver al menú |
| R | Reiniciar nivel actual |
| ENTER | Avanzar en menús |
| Q | Salir al menú principal |
| H | Ver High Scores (desde menú) |
| BACKSPACE | Borrar letra (al ingresar nombre) |

---

## 🌍 Niveles

### Nivel 1: Bosque Místico 🌲
- **Tema**: Plataformas de madera en un bosque verde
- **Dificultad**: Básica
- **Enemigos**: 3 murciélagos, 2 trampas rotantes, 1 roca cayendo
- **Power-ups**: 3

### Nivel 2: Caverna Oscura 🗿
- **Tema**: Plataformas de piedra en una caverna
- **Dificultad**: Media
- **Enemigos**: 5 murciélagos, 4 trampas rotantes, 3 rocas cayendo
- **Power-ups**: 4
- **Novedad**: Plataformas móviles

### Nivel 3: Tormenta Eléctrica ⛈️
- **Tema**: Plataformas de nubes en el cielo tormentoso
- **Dificultad**: Alta
- **Enemigos**: 6 murciélagos, 5 trampas, 4 rocas, rayos eléctricos aleatorios
- **Power-ups**: 5
- **Novedad**: Rayos que aparecen dinámicamente

---

## 👾 Enemigos

### 🦇 Murciélagos
- Patrullan en trayectorias **sinusoidales**
- Aplican transformación de **rotación**
- Daño: 20 HP

### 🌪️ Trampas Rotantes
- Giran constantemente 360°
- Implementan **rotación continua**
- Daño: 25 HP

### 🪨 Rocas Cayendo
- Caen aplicando **física de gravedad**
- Rotan mientras caen
- Daño: 30 HP

### ⚡ Rayos Eléctricos (Nivel 3)
- Aparecen aleatoriamente con advertencia
- Animación de zigzag
- Daño: 35 HP

---

## 💎 Power-Ups

### 🛡️ Escudo
- **Color**: Dorado
- **Efecto**: Absorbe un golpe
- **Duración**: 5 segundos

### ⚡ Velocidad
- **Color**: Rojo
- **Efecto**: Movimiento 50% más rápido
- **Duración**: 5 segundos

### 🔍 Zoom
- **Color**: Verde
- **Efecto**: Aumenta tamaño del jugador (escalado)
- **Duración**: 5 segundos

---

## 📊 Sistema de Puntuación

| Acción | Puntos |
|--------|--------|
| Alcanzar plataforma | +10 |
| Recoger power-up | +50 |
| Eliminar enemigo | +100 |
| Completar nivel | +500 |
| Bonus de tiempo | +2 por segundo restante |

---

## 🔧 Algoritmos Implementados

### 1. Interpolación Lineal (LERP)
```python
def lerp(start, end, t):
    return start + (end - start) * t
```
**Uso**: Movimiento suave de la cámara, transiciones

### 2. Movimiento Sinusoidal
```python
def sine_wave(time, amplitude, frequency):
    return amplitude * math.sin(time * frequency)
```
**Uso**: Patrullas de murciélagos, animaciones flotantes

### 3. Rotación 2D
```python
def rotate_point(x, y, cx, cy, angle):
    rad = math.radians(angle)
    tx, ty = x - cx, y - cy
    rx = tx * cos(rad) - ty * sin(rad)
    ry = tx * sin(rad) + ty * cos(rad)
    return rx + cx, ry + cy
```
**Uso**: Rotación de enemigos y efectos visuales

### 4. Detección de Colisiones AABB
```python
def check_collision_rect(rect1, rect2):
    return rect1.colliderect(rect2)
```
**Uso**: Colisiones entre jugador, enemigos, plataformas y power-ups

### 5. Parallax Scrolling
```python
layer_offset = camera_offset * layer_speed
# layer_speed varía: 0.2 (lejano), 0.5 (medio), 0.8 (cercano)
```
**Uso**: Efecto de profundidad en fondos

---

## 🏗️ Arquitectura

### Diagrama de Clases

```
Game (Coordinador Principal)
├── Player (Jugador)
│   ├── Atributos: posición, velocidad, salud, puntuación
│   ├── Métodos: move(), jump(), take_damage()
│   └── Power-ups: shield, speed, zoom
│
├── Level (Generador de Niveles)
│   ├── Platform / MovingPlatform
│   ├── Enemy (clase base)
│   │   ├── Bat (sinusoidal + rotación)
│   │   ├── RotatingTrap (rotación continua)
│   │   ├── FallingRock (física de caída)
│   │   └── Lightning (spawn aleatorio)
│   └── PowerUp (animación flotante)
│
└── Camera (Sistema de Vista)
    ├── smooth_follow()
    └── parallax_layers[]
```

### Flujo de Ejecución

1. **Inicialización** (`main.py`)
   - Inicializar Pygame
   - Crear instancia de `Game`
   - Configurar ventana y recursos

2. **Menú Principal** (`game.py`)
   - Mostrar título e instrucciones
   - Esperar input del usuario (ENTER)

3. **Game Loop** (60 FPS)
   ```python
   while running:
       handle_events()  # Input del usuario
       update(dt)       # Física y lógica
       draw()           # Renderizado
       clock.tick(60)   # Mantener 60 FPS
   ```

4. **Actualización** (`update()`)
   - Procesar input del jugador
   - Aplicar física (gravedad, movimiento)
   - Actualizar enemigos y power-ups
   - Detectar colisiones
   - Actualizar cámara con interpolación

5. **Renderizado** (`draw()`)
   - Parallax background (3 layers)
   - Plataformas
   - Enemigos y power-ups
   - Jugador con efectos
   - HUD (salud, puntuación, tiempo)

---

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.8 o superior
- Pygame 2.0+
- NumPy (para generación de audio)

### Instalación

```bash
# Instalar Pygame y NumPy
pip install pygame numpy

# Ejecutar el juego
python main.py
```

### Solución de Problemas

**Problema**: Error al importar pygame
```bash
# Solución
pip install --upgrade pygame
```

**Problema**: Error con numpy (audio)
```bash
# Solución
pip install numpy
# O deshabilitar audio en constants.py: ENABLE_SOUND = False
```

**Problema**: Pantalla negra al iniciar
- Verificar que todos los archivos estén en el mismo directorio
- Revisar la consola para mensajes de error

---

##  Conceptos Aplicados 

### ✅ Código Fuente Depurado
- ✔️ Sin errores de ejecución
- ✔️ Código limpio y organizado
- ✔️ Identación correcta (PEP 8)
- ✔️ Uso extensivo de funciones modulares
- ✔️ Estructuras de datos apropiadas (listas, diccionarios, clases)
- ✔️ Comentarios detallados en cada función
- ✔️ Documentación interna completa
- ✔️ Separación lógica en 9 archivos

### ✅ Conceptos de Informática Gráfica
- ✔️ **Traslación**: Movimiento de objetos, parallax, plataformas móviles
- ✔️ **Rotación**: Enemigos, trampas, efectos visuales
- ✔️ **Escala**: Power-up de zoom, efectos de pulso
- ✔️ **Vistas 2D**: Sistema de cámara con smooth following
- ✔️ **Proyección ortográfica**: Coordenadas 2D consistentes
- ✔️ **Texturas y primitivas**: Formas geométricas, gradientes, colores
- ✔️ **Animaciones**: Interpolación, movimiento sinusoidal, partículas

### ✅ Producto Final Completo
- ✔️ Menú principal intuitivo
- ✔️ 3 niveles completamente funcionales
- ✔️ HUD con información clara
- ✔️ Navegación fluida entre estados
- ✔️ Sin errores en ejecución
- ✔️ Gameplay balanceado

### ✅ Documentación
- ✔️ README explicativo completo
- ✔️ Comentarios por función
- ✔️ Diagrama de clases
- ✔️ Diagrama de flujo de ejecución
- ✔️ Explicación de algoritmos

---



## 📈 Mejoras Futuras


- Más tipos de enemigos
- Niveles procedurales aleatorios
- Multijugador local
- Power-ups adicionales
- Jefes de nivel

---


**¡Disfruta jugando SkyRunner! 🚀**
