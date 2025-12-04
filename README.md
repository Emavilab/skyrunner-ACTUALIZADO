# 🎮 SkyRunner - Runner Vertical 2D

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)
![NumPy](https://img.shields.io/badge/NumPy-Latest-orange.svg)
![Status](https://img.shields.io/badge/Status-Completo-success.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **Proyecto de Informática Gráfica** - Runner vertical con física realista, efectos visuales avanzados y audio procedural.


## 🎯 Descripción

**SkyRunner** es un runner vertical 2D desarrollado en Python con Pygame que implementa conceptos avanzados de:

- **Informática Gráfica**: Transformaciones 2D, animaciones, sistemas de partículas, parallax scrolling
- **Programación Orientada a Objetos**: Herencia, polimorfismo, encapsulación, composición
- **Física de Videojuegos**: Gravedad, colisiones AABB, interpolación, cinemática
- **Síntesis de Audio**: Generación procedural de música y efectos con NumPy

El jugador controla una rana que debe escalar hacia el cielo evitando enemigos dinámicos, lava ascendente y obstáculos, mientras recolecta power-ups y completa niveles temáticos con diferentes mecánicas.

---

## ✨ Características Principales

### 🎨 **Gráficos y Visuales**

| Característica | Descripción |
|---------------|-------------|
| **Sprites Animados** | 17 frames de idle + 12 frames de run + 8 frames de salto/caída |
| **Tilesets Reales** | Extracción dinámica de `Blue.png` y `Terrain.png` (8x8 tiles) |
| **Sistema de Parallax** | 3 capas de fondo con profundidad |
| **Partículas Avanzadas** | Sistema con física, colores, transparencia y vida útil |
| **Animaciones Fluidas** | Interpolación lineal (lerp) a 60 FPS |
| **Screen Shake** | Efecto dinámico en daño y explosiones |
| **Efectos de Luz** | Glow, pulsación de color, sombras dinámicas |
| **Transformaciones 2D** | Rotación, escalado, traslación en enemigos y power-ups |

### 🎮 **Gameplay**

- ✅ **Sistema de Vidas**: 3 vidas con respawn e invulnerabilidad temporal (2s)
- ✅ **7 Power-ups Únicos**: Escudo, velocidad, zoom, combo, time-slow, imán, salto doble
- ✅ **5 Tipos de Enemigos**: Con IA y patrones únicos
- ✅ **Lava Dinámica**: Ascenso progresivo con aceleración por altura ganada
- ✅ **3 Niveles Temáticos**: Bosque místico, caverna oscura, tormenta eléctrica
- ✅ **3 Dificultades**: Easy, Normal, Hard (afecta velocidad, daño, spawn rate)
- ✅ **Sistema de Combos**: Multiplicadores de puntuación (x2, x3, x5)
- ✅ **High Scores**: Persistencia en JSON con top 10 por dificultad
- ✅ **Física Realista**: Gravedad, velocidad, aceleración, fricción

### 🔊 **Audio Procedural**

- 🎵 **Música Épica**: Generada con NumPy (sin archivos externos)
  - Tema de menú: Marcha de guerra a 120 BPM
  - Tema de juego: Batalla intensa a 140 BPM
- 🔔 **30+ Efectos de Sonido**: Saltos, daño, power-ups, enemigos, lava
- 🌊 **Sonidos Ambientales**: Viento, pájaros, goteo, truenos por nivel
- 🎛️ **Sistema de Mezcla**: 16 canales simultáneos, control de volumen por categoría
- 🔇 **Tecla M**: Silenciar/activar audio en cualquier momento

### 🎯 **Interfaz y UX**

- 📱 **Menú Principal**: Navegación completa con teclado/ratón
- 🏆 **Tabla de Puntuaciones**: Top 10 por dificultad con fecha
- ⚙️ **Pantalla de Controles**: Tutorial interactivo
- 🌟 **Pantalla de Créditos**: Scroll automático cinematográfico
- 📊 **HUD Dinámico**: Vidas, puntuación, tiempo, nivel de peligro de lava
- ⏸️ **Menú de Pausa**: Continuar, reiniciar o volver al menú

---

## 🛠️ Tecnologías Utilizadas

### **Lenguajes y Frameworks**

```python
Python 3.13.1        # Lenguaje principal
Pygame 2.6.1         # Motor de juego y renderizado
NumPy 1.26+          # Síntesis de audio y matemáticas
```

### **Librerías Core**

| Librería | Propósito | Uso |
|----------|-----------|-----|
| `pygame` | Motor gráfico | Renderizado, input, colisiones, audio |
| `numpy` | Computación numérica | Síntesis de ondas de audio, FFT |
| `math` | Matemáticas | Sin, cos, exp para física y animaciones |
| `random` | Aleatoriedad | Generación procedural, variaciones |
| `json` | Persistencia | Guardar/cargar high scores |
| `datetime` | Timestamps | Fechas en tabla de puntuaciones |

---

## 📦 Instalación

### **Requisitos Previos**

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### **Paso 1: Clonar el Repositorio**

```bash
git clone https://github.com/Emavilab/skyrunner-ACTUALIZADO.git
cd skyrunner-ACTUALIZADO
```

### **Paso 2: Instalar Dependencias**

```bash
pip install pygame numpy
```

### **Paso 3: Ejecutar el Juego**

```bash
python main.py
```

### **Configuración Opcional**

Editar `objects/constants.py` para ajustar:
- Resolución de pantalla
- FPS objetivo
- Configuración de audio
- Parámetros de física

---

## 🎮 Controles

### **Movimiento**

| Tecla | Acción |
|-------|--------|
| `←` `→` | Mover izquierda/derecha |
| `ESPACIO` | Saltar |
| `ESPACIO` (doble) | Salto doble (con power-up) |

### **Sistema**

| Tecla | Acción |
|-------|--------|
| `ESC` | Pausar / Volver al menú |
| `R` | Reiniciar nivel |
| `Q` | Volver al menú principal |
| `M` | Silenciar/activar audio |
| `F` | Pantalla completa |
| `F1` | Alternar pantalla completa |

### **Menú Principal**

| Tecla | Acción |
|-------|--------|
| `↑` `↓` | Navegar opciones |
| `ENTER` | Seleccionar opción |
| `E` | Dificultad: Fácil |
| `N` | Dificultad: Normal |
| `H` | Dificultad: Difícil |

---

## 🏗️ Arquitectura del Proyecto

### **Estructura de Directorios**

```
skyrunner-main/
├── main.py                      # Punto de entrada, menú principal
├── README.md                    # Este archivo
├── EVALUACION_PROYECTO.md       # Documentación académica completa
├── DIAGRAMA_CLASES.md          # Diagrama de clases ASCII
├── high_scores.json            # Persistencia de puntuaciones
│
├── Assets/                     # Recursos gráficos
│   ├── Player/                # Sprites del jugador (17 idle, 12 run)
│   ├── Terrain/               # Tilesets (Blue.png, Terrain.png)
│   ├── Enemies/               # Sprites de enemigos
│   ├── Collectables/          # Power-ups y objetos
│   └── Castle/                # Elementos decorativos
│
├── Models/                    # Modelos de entidades
│   ├── player.py             # Jugador con física y animación
│   ├── enemies.py            # Enemigos base + 5 tipos
│   ├── lava.py               # Sistema de lava dinámica
│   ├── drones.py             # Drones de vigilancia
│   └── bosses.py             # Jefes (futuro)
│
├── objects/                   # Objetos y sistemas del juego
│   ├── game.py               # Loop principal, colisiones
│   ├── platforms.py          # Plataformas y tileset manager
│   ├── powerup_simple.py     # Sistema de power-ups
│   ├── audio.py              # Síntesis de audio procedural
│   ├── flags.py              # Banderas de victoria
│   ├── constants.py          # Constantes globales
│   └── utils.py              # Funciones auxiliares
│
├── Levels/                    # Generación de niveles
│   └── level.py              # Level class con generación procedural
│
├── Platform/                  # Sistema de terreno
│   └── terrain_manager.py    # Gestión de terreno dinámico
│
└── Json/                      # Persistencia de datos
    ├── highscores.json       # Puntuaciones guardadas
    └── highscores.py         # Manager de high scores
```

### **Patrón de Diseño: MVC Modificado**

```
┌─────────────┐
│   main.py   │  ← Controlador Principal (Menús)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Game      │  ← Controlador de Juego (Loop, Lógica)
└──────┬──────┘
       │
       ├──────▶ Player (Modelo)
       ├──────▶ Level (Modelo + Vista)
       ├──────▶ Enemies (Modelos)
       ├──────▶ Lava (Modelo)
       └──────▶ AudioManager (Controlador Audio)
```

---

## 🎓 Conceptos de Informática Gráfica

### **1. Transformaciones 2D**

#### **Traslación**
```python
# Movimiento del jugador
self.x += self.vel_x * dt
self.y += self.vel_y * dt

# Movimiento de cámara
camera_y = lerp(camera_y, target_y, 0.1)
```

#### **Rotación**
```python
# Enemigos rotatorios (trampas)
self.angle += self.rotation_speed * dt
rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
```

#### **Escalado**
```python
# Power-up de zoom
if zoom_active:
    scaled_sprite = pygame.transform.scale(sprite, (w * 1.5, h * 1.5))
```

### **2. Proyección Ortográfica**

- Vista 2D con scroll vertical
- Cámara sigue al jugador con interpolación
- Culling de objetos fuera de pantalla

### **3. Sistema de Partículas**

```python
class Particle:
    x, y: float          # Posición
    vx, vy: float        # Velocidad
    life: float          # Tiempo de vida
    size: int            # Tamaño
    color: tuple         # RGB/RGBA
    gravity: float       # Aceleración vertical
```

**Tipos implementados:**
- Partículas de lava (física balística)
- Burbujas (crecimiento + explosión)
- Humo (desvanecimiento)
- Efectos de colección (explosión radial)

### **4. Animación por Sprites**

- **Spritesheet splitting**: Extracción de frames individuales
- **Frame interpolation**: Cambio suave entre frames
- **State machines**: Idle → Run → Jump → Fall

### **5. Parallax Scrolling**

```python
# Capa 1 (fondo): Velocidad 0.3x
bg_layer1_y = camera_y * 0.3

# Capa 2 (medio): Velocidad 0.6x  
bg_layer2_y = camera_y * 0.6

# Capa 3 (frente): Velocidad 1.0x
foreground_y = camera_y * 1.0
```

### **6. Colisiones AABB**

```python
def check_collision(rect1, rect2):
    return (rect1.left < rect2.right and
            rect1.right > rect2.left and
            rect1.top < rect2.bottom and
            rect1.bottom > rect2.top)
```

---

## 🔧 Sistemas Implementados

### **1. Sistema de Física**

```python
# Gravedad
GRAVITY = 0.8

# Ecuaciones de movimiento
vel_y += GRAVITY * dt
y += vel_y * dt

# Fricción
vel_x *= FRICTION_COEFFICIENT
```

### **2. Sistema de Cámara**

- **Smooth follow**: Interpolación con lerp
- **Dead zone**: Zona sin movimiento de cámara
- **Look ahead**: Anticipa movimiento del jugador
- **Screen shake**: Trauma-based shake effect

### **3. Sistema de Audio Procedural**

#### **Síntesis Aditiva**
```python
# Onda sinusoidal básica
t = np.linspace(0, duration, samples)
wave = np.sin(2 * np.pi * frequency * t)

# Envelope ADSR
envelope = attack + decay + sustain + release
wave *= envelope
```

#### **Música Épica de Guerra**
```python
# Bajo de marcha militar (55 Hz)
bass = 0.5 * np.sin(2 * π * 55 * t)

# Acordes power (quintas)
chord = 0.35 * np.sin(2 * π * 110 * t)  # A
chord += 0.35 * np.sin(2 * π * 165 * t) # E

# Percusión sintética
kick = noise * np.exp(-20 * t)
```

### **4. Sistema de Generación Procedural**

```python
def generate_platforms(height):
    platforms = []
    y = 0
    while y < height:
        x = random.randint(50, SCREEN_WIDTH - 50)
        y += random.randint(80, 150)  # Gap vertical
        width = random.choice([2, 3, 4]) * TILE_SIZE
        platforms.append(Platform(x, y, width))
    return platforms
```

### **5. Sistema de Power-ups**

Cada power-up tiene:
- Animación flotante (sin/cos wave)
- Efecto de brillo (glow pulsante)
- Partículas de brillo constantes
- Explosión al recolectar
- Duración temporal con barra de progreso

---

## 🌍 Niveles y Dificultad

### **Nivel 1: Bosque Místico** 🌲

- **Altura**: 1600px
- **Tema**: Verde/Marrón
- **Enemigos**: Murciélagos, trampas rotatorias
- **Plataformas**: Regulares con árboles
- **Ambiente**: Viento, pájaros

### **Nivel 2: Caverna Oscura** ⛰️

- **Altura**: 1920px
- **Tema**: Azul oscuro/Gris
- **Enemigos**: Rocas cayendo, trampas, murciélagos
- **Plataformas**: Estalactitas y estalagmitas
- **Ambiente**: Goteo, ecos

### **Nivel 3: Tormenta Eléctrica** ⚡

- **Altura**: 2400px
- **Tema**: Púrpura/Amarillo
- **Enemigos**: Rayos, drones, murciélagos
- **Plataformas**: Flotantes en tormenta
- **Ambiente**: Truenos, viento fuerte

### **Dificultades**

| Parámetro | Easy | Normal | Hard |
|-----------|------|--------|------|
| Velocidad Jugador | 5.0 | 4.5 | 4.0 |
| Fuerza Salto | -16 | -15 | -14 |
| Velocidad Lava | 0.5 | 1.0 | 1.5 |
| Daño Enemigos | 15 | 25 | 40 |
| Spawn Enemigos | Bajo | Medio | Alto |
| Puntos Base | 50 | 100 | 200 |

---

## 💎 Power-ups

| Icono | Nombre | Efecto | Duración |
|-------|--------|--------|----------|
| 🛡️ | **Shield** | Inmunidad a daño | 8s |
| ⚡ | **Speed** | Velocidad +50% | 6s |
| 🔍 | **Zoom** | Tamaño +50% | 7s |
| 🎯 | **Combo** | Puntos x2 | 10s |
| ⏱️ | **Time Slow** | Tiempo -50% | 5s |
| 🧲 | **Magnet** | Atrae power-ups | 8s |
| 🦘 | **Double Jump** | Salto doble | Permanente |

### **Efectos Visuales**

- Rotación continua 3D
- Partículas de brillo
- Glow pulsante
- Animación flotante
- Explosión al recolectar (15 partículas)

---

## 👾 Enemigos

### **1. Murciélago** 🦇

```python
Comportamiento: Patrulla horizontal con movimiento sinusoidal
Patrón: x += vel, y += sin(time) * amplitude
Daño: 15-40 (según dificultad)
Velocidad: 2-4 px/frame
```

### **2. Trampa Rotatoria** ⭐

```python
Comportamiento: Rotación continua estática
Patrón: angle += rotation_speed * dt
Transformación: pygame.transform.rotate()
Daño: 25-50
Radio: 30-50px
```

### **3. Roca Cayendo** 🪨

```python
Comportamiento: Caída con gravedad
Física: vel_y += gravity, rotation += vel_rotation
Daño: 30-60
Velocidad Terminal: 12 px/frame
```

### **4. Rayo** ⚡

```python
Comportamiento: Advertencia → Caída instantánea
Fases: Warning (1s) → Strike → Fade
Daño: 35-70
Velocidad: Instantánea
```

### **5. Drone de Vigilancia** 🛸

```python
Comportamiento: Detección → Persecución
IA: Pathfinding hacia jugador
Estados: Patrol → Alert → Chase → Attack
Daño: 20-45
Rango Detección: 200-400px
```

---

## 📊 Algoritmos y Complejidad

### **Colisión AABB**
```
Complejidad: O(n)
donde n = número de enemigos activos
Optimización: Culling por distancia
```

### **Interpolación Lineal (Lerp)**
```
Complejidad: O(1)
Uso: Cámara, transiciones, animaciones
```

### **Generación Procedural**
```
Complejidad: O(h)
donde h = altura del nivel
Algoritmo: Distribución aleatoria con validación de alcanzabilidad
```

### **Ordenamiento (High Scores)**
```
Complejidad: O(n log n)
Algoritmo: Timsort (built-in de Python)
```

### **Síntesis de Audio**
```
Complejidad: O(n)
donde n = número de muestras (sample_rate * duration)
```

---

## 🎓 Requisitos Académicos Cumplidos

### ✅ **Código Fuente Depurado**
- Organización modular (7 módulos)
- Nomenclatura consistente (snake_case)
- Comentarios exhaustivos
- Docstrings en todas las clases/métodos
- Sin errores de linting

### ✅ **Conceptos de Informática Gráfica**
- Transformaciones 2D (traslación, rotación, escalado)
- Proyección ortográfica
- Texturas y sprites
- Animaciones por frames
- Sistemas de partículas
- Culling y optimización
- Colisiones AABB

### ✅ **Paradigma de Programación Orientada a Objetos**
- 35+ clases implementadas
- Herencia: `Enemy` → `Bat`, `RotatingTrap`, `FallingRock`, etc.
- Polimorfismo: `enemy.update()`, `enemy.draw()`
- Encapsulación: Atributos privados, getters/setters
- Composición: `Game` contiene `Player`, `Level`, `Lava`

### ✅ **Producto Final Completo**
- Menú principal funcional
- 3 niveles jugables
- Sistema de puntuación
- High scores persistentes
- Pantallas de victoria/derrota
- Tutorial de controles
- Créditos

---

## 🏆 Créditos

### **Desarrollo**
- **Programación**: Proyecto SkyRunner Team
- **Diseño de Juego**: Inspirado en runners verticales clásicos
- **Informática Gráfica**: Implementación de conceptos académicos

### **Recursos**
- **Sprites**: OpenGameArt / Kenney Assets
- **Audio**: Generación procedural con NumPy
- **Fuentes**: Pygame built-in fonts

### **Tecnologías**
- Python 3.13.1
- Pygame 2.6.1
- NumPy 1.26+



---

## 📜 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

```
MIT License

Copyright (c) 2025 SkyRunner Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

</div>
