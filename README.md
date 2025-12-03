# 🎮 SkyRunner - Runner Vertical 2D

🎯 Descripción General
SkyRunner es un juego de plataformas vertical desarrollado en Python con Pygame que implementa conceptos avanzados de informática gráfica, programación orientada a objetos y física de juegos. El jugador debe escalar hacia el cielo evitando enemigos dinámicos y lava ascendente, recolectando power-ups y completando niveles con diferentes temáticas.
🎮 Mecánicas Core

Movimiento fluido con física realista
Sistema de salto con coyote time
Cámara dinámica con suavizado
Lava ascendente como presión de tiempo
3 niveles temáticos (Bosque, Caverna, Tormenta)
3 niveles de dificultad con ajustes dinámicos
Sistema de power-ups con efectos visuales
Enemigos con IA (murciélagos, trampas, rocas, rayos, drones)
Sistema de puntuación con combos y récords


✨ Características Principales
🎨 Gráficos y Visuales

✅ Sprites animados para el jugador (ranita con 17 frames de idle, 12 de run)
✅ Tilesets reales (Blue.png y Terrain.png) con extracción dinámica
✅ Sistema de parallax con múltiples capas de fondo
✅ Efectos de partículas para power-ups, daño, y colecciones
✅ Animaciones fluidas con interpolación lineal (lerp)
✅ Screen shake dinámico en eventos importantes
✅ Glow effects y iluminación dinámica

🎯 Gameplay

✅ Sistema de vidas con respawn e invulnerabilidad temporal
✅ Power-ups funcionales (escudo, velocidad, zoom, combo, imán)
✅ Enemigos con comportamiento único:

Murciélagos con patrón sinusoidal
Trampas rotatorias con transformaciones
Rocas con física de caída
Rayos con advertencia visual
Drones con detección de jugador


✅ Lava dinámica con aceleración progresiva
✅ Sistema de combos con multiplicadores
✅ Banderas de victoria con animación de izado

🔊 Audio

✅ Música procedural generada con NumPy
✅ Efectos de sonido para todas las acciones
✅ Sistema de mezcla con múltiples canales
✅ Sonidos ambientales por nivel


🏗️ Arquitectura del Proyecto
📁 Estructura de Directorios
SkyRunner/
├── main.py                     # Punto de entrada principal
├── README.md                   # Este archivo
├── requirements.txt            # Dependencias del proyecto
│
├── Assets/                     # Recursos gráficos y de audio
│   ├── Player/                 # Sprites del jugador
│   │   ├── player_idle.png
│   │   ├── player_run.png
│   │   ├── player_jump.png
│   │   └── player_fall.png
│   ├── Terrain/                # Tilesets
│   │   ├── Blue.png
│   │   └── Terrain.png
│   ├── Collectables/           # Power-ups
│   │   ├── kiwi.png
│   │   └── collected.png
│   └── Enemies/                # Sprites de enemigos
│       └── drone.png
│
├── Levels/                     # Sistema de niveles
│   ├── level.py               # Clase Level principal
│   └── tile_manager.py        # Gestor de tiles
│
├── Models/                     # Clases del juego
│   ├── player.py              # Clase Player
│   ├── enemies.py             # Todos los enemigos
│   ├── lava.py                # Sistema de lava
│   ├── bosses.py              # Jefes (futuro)
│   └── drones.py              # Drones inteligentes
│
├── objects/                    # Componentes del juego
│   ├── constants.py           # Constantes globales
│   ├── game.py                # Loop principal del juego
│   ├── platforms.py           # Plataformas y tiles
│   ├── powerup.py             # Sistema de power-ups
│   ├── audio.py               # Sistema de audio
│   ├── utils.py               # Funciones auxiliares
│   └── flags.py               # Banderas de victoria
│
├── Json/                       # Datos persistentes
│   └── highscores.json        # Puntuaciones altas
│
└── high_scores.json           # Récords por dificultad
🔄 Flujo del Programa
main.py
    ↓
[Menú Principal]
    ↓
[Selección de Dificultad]
    ↓
Game.__init__() ──→ Level.__init__() ──→ TileManager
    ↓                    ↓
Player.__init__()    Enemigos generados
    ↓                    ↓
[Game Loop] ←──────────┘
    ↓
┌───────────────────────────┐
│ 1. handle_events()        │
│ 2. update(dt)             │
│    ├─ player.update()     │
│    ├─ level.update()      │
│    ├─ lava.update()       │
│    └─ check_collisions()  │
│ 3. draw()                 │
│    ├─ background          │
│    ├─ level.draw()        │
│    ├─ player.draw()       │
│    └─ HUD                 │
└───────────────────────────┘
    ↓
[Game Over / Victory]
    ↓
[High Scores]

📊 Conceptos de Informática Gráfica
1️⃣ Transformaciones Geométricas
🔄 Traslación
python# Movimiento del jugador (objects/player.py)
self.x += self.vel_x  # Traslación horizontal
self.y += self.vel_y  # Traslación vertical

# Plataformas móviles (objects/platforms.py)
self.x += self.speed * self.direction  # Traslación con dirección
Aplicación:

Movimiento del jugador
Plataformas móviles
Enemigos patrullando
Partículas de efectos

🔁 Rotación
python# Trampas rotatorias (Models/enemies.py)
self.angle += self.rotation_speed * dt * 60
rotated_surface = pygame.transform.rotate(trap_surface, self.angle)

# Rocas que caen con rotación (Models/enemies.py)
self.rotation_angle += self.rotation_vel * dt * 60
rotated_surface = pygame.transform.rotate(rock_surface, self.rotation_angle)
Aplicación:

Trampas giratorias
Rocas cayendo con rotación realista
Power-ups con animación rotacional
Efectos de partículas

📏 Escalado
python# Power-up zoom (Models/player.py)
pulse = 0.03 * math.sin(self.game_time * 10)
self.zoom_scale = lerp(self.zoom_scale, 1.3 + pulse, 0.2)

current_width = int(self.width * self.zoom_scale)
current_height = int(self.height * self.zoom_scale)

# Sprites escalados dinámicamente (objects/platforms.py)
scaled_frame = pygame.transform.scale(frame, (tile_width, self.height))
Aplicación:

Efecto de zoom del power-up
Escalado de tiles del tileset
Efecto de pulsación en elementos visuales
Animación de recolección de items

2️⃣ Proyección y Vista
🎥 Sistema de Cámara 2D
python# Cámara con seguimiento suavizado (objects/game.py)
def update_camera(self):
    # Calcular posición objetivo
    self.target_camera_y = self.player.y - CAMERA_OFFSET_Y
    
    # Interpolación suave (lerp)
    self.camera_y = lerp(self.camera_y, self.target_camera_y, CAMERA_SMOOTHING)
Características:

✅ Seguimiento suave del jugador
✅ Interpolación lineal para movimiento fluido
✅ Offset configurable
✅ Sistema de "culling" (no dibuja elementos fuera de cámara)

🌄 Sistema de Parallax
python# Fondos con múltiples capas (Levels/level.py)
self.parallax_layers = [
    {'speed': 0.2, 'elements': far_elements},    # Capa lejana
    {'speed': 0.5, 'elements': mid_elements},    # Capa media
    {'speed': 0.8, 'elements': near_elements'}   # Capa cercana
]

# Actualizar offset por capa
for layer in self.parallax_layers:
    layer['offset'] = camera_offset * layer['speed']
Efecto: Sensación de profundidad 3D en entorno 2D
3️⃣ Texturas y Sprites
🖼️ Sistema de Tilesets
python# Extracción de tiles desde imagen (objects/platforms.py)
class TilesetManager:
    def get_tile(self, tileset_name, tile_id, width, height):
        # Calcular posición en tileset
        tiles_per_row = tileset.get_width() // self.tile_size
        tile_x = (tile_id % tiles_per_row) * self.tile_size
        tile_y = (tile_id // tiles_per_row) * self.tile_size
        
        # Extraer subtextura
        tile_rect = pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size)
        tile = tileset.subsurface(tile_rect).copy()
        
        # Escalar según necesidad
        return pygame.transform.scale(tile, (width, height))
Uso:

Blue.png (plataformas azules)
Terrain.png (tiles de terreno)
Mapeo UV implícito con coordenadas de tile

🎭 Sprite Animation
python# Animación del jugador (Models/player.py)
class Player:
    def load_frog_animations(self):
        # IDLE - 11 frames
        idle_sheet = SpriteSheet("player_idle.png")
        self.idle = [idle_sheet.get_frame(x) for x in range(11)]
        
        # RUN - 12 frames
        run_sheet = SpriteSheet("player_run.png")
        self.run = [run_sheet.get_frame(x) for x in range(12)]
    
    def update(self, dt):
        # Avanzar frame con timing
        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.idle_frame = (self.idle_frame + 1) % self.idle_length
Técnica: Frame-based animation con sprite sheets
4️⃣ Primitivas Gráficas
🔵 Formas Básicas
python# Círculos (partículas, power-ups)
pygame.draw.circle(surface, color, (x, y), radius)

# Rectángulos (plataformas, HUD)
pygame.draw.rect(surface, color, rect, border_radius=10)

# Polígonos (trampas, efectos)
pygame.draw.polygon(surface, color, points)

# Líneas (rayos, conexiones)
pygame.draw.line(surface, color, start, end, width)
✨ Sistema de Partículas
python# Partículas con física (objects/powerup.py)
class PowerUp:
    def create_sparkle(self):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 6)
        
        self.particles.append({
            'x': self.x,
            'y': self.y,
            'vx': math.cos(angle) * speed,  # Velocidad X
            'vy': math.sin(angle) * speed,  # Velocidad Y
            'life': random.uniform(0.5, 1.0),
            'size': random.uniform(2, 4),
            'color': self.color
        })
    
    def update_particles(self, dt):
        for p in self.particles:
            p['x'] += p['vx']           # Traslación
            p['y'] += p['vy']
            p['vy'] += 0.15            # Gravedad
            p['life'] -= dt            # Fade out
5️⃣ Efectos Visuales Avanzados
💫 Glow Effects
python# Brillo dinámico (objects/powerup.py)
def draw(self, surface, camera_offset):
    # Glow pulsante
    self.glow_alpha = 80 + int(70 * abs(math.sin(self.float_time * 1.5)))
    
    # Superficie con alpha blending
    glow_surf = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*color[:3], self.glow_alpha//2),
                      (glow_size, glow_size), glow_size)
    
    surface.blit(glow_surf, position, special_flags=pygame.BLEND_ADD)
📺 Screen Shake
python# Vibración de pantalla (objects/game.py)
def draw(self):
    shake_x = 0
    shake_y = 0
    if self.screen_shake_magnitude > 0:
        shake_x = random.randint(-magnitude, magnitude)
        shake_y = random.randint(-magnitude, magnitude)
    
    self.screen.blit(temp_surface, (shake_x, shake_y))
🌊 Animaciones Procedurales
python# Movimiento sinusoidal de lava (Models/lava.py)
def get_surface_y(self, x):
    wave1 = math.sin(x * 0.02 + self.wave_time * 2) * self.wave_amplitude
    wave2 = math.sin(x * 0.05 + self.wave_time * 1.5) * (self.wave_amplitude * 0.5)
    wave3 = math.sin(x * 0.01 + self.wave_time * 0.8) * (self.wave_amplitude * 0.3)
    
    return self.y + wave1 + wave2 + wave3  # Suma de ondas

🎲 Paradigma de Programación
🏛️ Orientado a Objetos (OOP)
El proyecto está completamente estructurado con OOP, siguiendo principios SOLID:
📦 Clases Principales
python# 1. JUGADOR - Encapsula toda la lógica del jugador
class Player:
    def __init__(self, x, y, difficulty_settings):
        # Atributos (Encapsulación)
        self.x, self.y = x, y
        self.vel_x, self.vel_y = 0, 0
        self.health = PLAYER_MAX_HEALTH
        self.lives = difficulty_settings["player_lives"]
        
    def handle_input(self, keys):
        # Método para manejar entrada
        
    def update(self, dt, platforms):
        # Método para actualizar estado
        
    def draw(self, surface, camera_offset):
        # Método para dibujado
        
    def take_damage(self, damage):
        # Método para recibir daño
python# 2. ENEMIGOS - Jerarquía con herencia
class Enemy:
    """Clase base abstracta"""
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.active = True
        self.damage = 20
    
    def get_rect(self):
        raise NotImplementedError
    
    def update(self, dt):
        raise NotImplementedError
    
    def draw(self, surface, camera_offset):
        raise NotImplementedError

class Bat(Enemy):
    """Murciélago - Hereda de Enemy"""
    def __init__(self, x, y, patrol_range=150):
        super().__init__(x, y)
        self.patrol_range = patrol_range
        self.speed = BAT_SPEED
        # ... atributos específicos
    
    def update(self, dt):
        # Implementación específica
        self.x += self.speed * self.direction * dt * 60
        self.y = self.start_y + sine_wave(self.time, amplitude, frequency)

class RotatingTrap(Enemy):
    """Trampa rotatoria - Hereda de Enemy"""
    def update(self, dt):
        self.angle += self.rotation_speed * dt * 60  # Rotación
python# 3. NIVEL - Composición de elementos
class Level:
    def __init__(self, level_number, custom_config=None, difficulty="normal"):
        self.number = level_number
        self.config = custom_config or LEVELS_CONFIG[level_number]
        
        # Composición: Level contiene múltiples objetos
        self.platforms = []      # Lista de Platform
        self.enemies = []        # Lista de Enemy
        self.powerups = []       # Lista de PowerUp
        self.flags = []          # Lista de VictoryFlag
        
        self._generate()         # Genera el nivel
    
    def update(self, dt, player_y, player_x=None):
        # Polimorfismo: llama update() de cada objeto
        for platform in self.platforms:
            if isinstance(platform, MovingPlatform):
                platform.update(dt)
        
        for enemy in self.enemies:
            enemy.update(dt)  # Cada enemigo tiene su propia implementación
        
        for powerup in self.powerups:
            powerup.update(dt)
python# 4. JUEGO - Coordinador principal
class Game:
    def __init__(self, difficulty="normal", screen=None):
        self.difficulty = difficulty
        self.settings = DIFFICULTY_SETTINGS[difficulty]
        
        # Composición de objetos principales
        self.player = Player(x, y, self.settings)
        self.level = Level(1, difficulty=difficulty)
        self.lava = Lava(difficulty)
        
    def run(self):
        """Game loop principal"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()  # Entrada
            self.update(dt)       # Lógica
            self.draw()           # Renderizado
            
            pygame.display.flip()
🔑 Principios OOP Aplicados

Encapsulación ✅

Atributos privados con getters/setters
Ocultamiento de implementación interna



python   class Player:
       def __init__(self):
           self.__health = 100  # Privado
       
       def get_health(self):
           return self.__health
       
       def take_damage(self, damage):
           self.__health = max(0, self.__health - damage)

Herencia ✅

Jerarquía de clases Enemy → Bat, Trap, Rock, etc.
Reutilización de código



python   Enemy (base)
       ├─ Bat
       ├─ RotatingTrap
       ├─ FallingRock
       ├─ Lightning
       └─ SurveillanceDrone

Polimorfismo ✅

Métodos con mismo nombre, diferente comportamiento



python   for enemy in self.enemies:
       enemy.update(dt)  # Cada uno actualiza diferente
       enemy.draw(surface, camera_offset)  # Cada uno dibuja diferente

Abstracción ✅

Clases base abstractas
Interfaces definidas



python   class Enemy(ABC):
       @abstractmethod
       def update(self, dt):
           pass
       
       @abstractmethod
       def draw(self, surface, camera_offset):
           pass

Composición ✅

Objetos contienen otros objetos



python   Game
       ├─ Player
       ├─ Level
       │   ├─ Platform[]
       │   ├─ Enemy[]
       │   └─ PowerUp[]
       └─ Lava

📊 Estructuras de Datos Implementadas
1️⃣ Listas (Arrays Dinámicos)
python# Lista de enemigos (Levels/level.py)
self.enemies = []  # Lista dinámica

# Agregar enemigos
bat = Bat(x, y)
self.enemies.append(bat)  # O(1) amortizado

# Iterar y actualizar
for enemy in self.enemies:  # O(n)
    enemy.update(dt)

# Filtrar activos (list comprehension)
self.enemies = [e for e in self.enemies if e.active]  # O(n)
Uso:

✅ platforms[] - Lista de plataformas
✅ enemies[] - Lista de enemigos activos
✅ powerups[] - Lista de power-ups disponibles
✅ particles[] - Lista de partículas visuales
✅ flags[] - Lista de banderas de victoria

2️⃣ Diccionarios (Hash Maps)
python# Configuración de niveles (objects/constants.py)
LEVELS_CONFIG = {
    1: {'name': 'Bosque', 'platforms': 10, 'bats': 2, 'traps': 1},
    2: {'name': 'Caverna', 'platforms': 12, 'bats': 3, 'traps': 2},
    3: {'name': 'Tormenta', 'platforms': 15, 'bats': 3, 'traps': 2}
}

# Acceso O(1)
config = LEVELS_CONFIG[level_number]

# Diccionario de colores por power-up (objects/powerup.py)
self.colors = {
    'shield': (34, 139, 34),
    'speed': (255, 140, 0),
    'zoom': (152, 251, 152)
}

color = self.colors.get(powerup_type, default_color)  # O(1)

# Diccionario de puntuaciones (high_scores.json)
{
    "easy": [
        {"name": "PRO", "score": 15000, "date": "2024-01-01"},
        {"name": "HERO", "score": 12000, "date": "2024-01-01"}
    ],
    "normal": [...],
    "hard": [...]
}
Uso:

✅ Configuraciones de nivel
✅ Colores por tipo
✅ Símbolos por power-up
✅ Puntuaciones por dificultad
✅ Parámetros de dificultad

3️⃣ Colas (Queues) - Implícitas
python# Cola de posiciones para trail effect (objects/powerup.py)
class PowerUp:
    def __init__(self):
        self.last_positions = []  # Cola FIFO
        self.max_trail_length = 5
    
    def update(self, dt):
        # Agregar posición actual
        self.last_positions.append((self.x, self.y))
        
        # Mantener tamaño máximo (comportamiento de cola)
        if len(self.last_positions) > self.max_trail_length:
            self.last_positions.pop(0)  # Eliminar más antiguo (FIFO)
Uso:

✅ Trail effects (estela de movimiento)
✅ Historial de posiciones
✅ Buffer de eventos

4️⃣ Pilas (Stacks) - Implícitas
python# Pila de estados del juego (main.py)
class MenuState:
    MAIN = "main"
    HIGH_SCORES = "high_scores"
    CONTROLS = "controls"

# Navegación como pila
menu_stack = []
menu_stack.append(MenuState.MAIN)        # Push

if event.key == pygame.K_ESCAPE:
    if menu_stack:
        menu_stack.pop()                  # Pop
Uso:

✅ Navegación de menús
✅ Estados del juego
✅ Historial de acciones

5️⃣ Matrices (2D Arrays)
python# Matriz de tiles para nivel (Levels/tile_manager.py)
class TileManager:
    def __init__(self):
        # Matriz conceptual de tiles
        self.tile_grid = []  # Lista de listas
        
        # Generar grid de tiles
        for row in range(num_rows):
            tile_row = []
            for col in range(num_cols):
                x = col * tile_size
                y = row * tile_size
                tile = Tile(x, y, tile_id)
                tile_row.append(tile)
            self.tile_grid.append(tile_row)
    
    def get_tile_at(self, row, col):
        """Acceso O(1) a tile específico"""
        return self.tile_grid[row][col]
Uso:

✅ Grid de tiles del nivel
✅ Mapa de colisiones
✅ Generación procedural

6️⃣ Árboles (Implícitos en Jerarquía)
python# Árbol de herencia de clases
"""
GameObject (raíz)
    ├─ Player
    ├─ Enemy
    │   ├─ Bat
    │   ├─ RotatingTrap
    │   ├─ FallingRock
    │   └─ SurveillanceDrone
    ├─ Platform
    │   ├─ MovingPlatform
    │   └─ CastlePlatform
    └─ PowerUp
"""
7️⃣ Grafos (Para Pathfinding de Drones)
python# Grafo implícito para navegación (Models/drones.py)
class SurveillanceDrone:
    def __init__(self, x, y):
        self.patrol_points = []  # Nodos del grafo
        self.current_patrol_index = 0
        
        # Generar puntos de patrulla (nodos)
        for _ in range(4):
            px = self.x + random.randint(-200, 200)
            py = self.y + random.randint(-100, 100)
            self.patrol_points.append((px, py))
    
    def update(self, dt):
        # Navegar entre nodos
        target = self.patrol_points[self.current_patrol_index]
        
        if distance_to(target) < 10:
            # Ir al siguiente nodo (grafo cíclico)
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
8️⃣ Análisis de Complejidad
OperaciónEstructuraComplejidadUso en el JuegoAgregar enemigoListaO(1) amortizadoenemies.append(bat)Buscar config nivelDictO(1)LEVELS_CONFIG[level_num]Iterar enemigosListaO(n)for enemy in enemiesFiltrar activosListaO(n)[e for e in enemies if e.active]Acceso a tileMatrizO(1)grid[row][col]Ordenar scoresListaO(n log n)sorted(scores, key=...)

🔧 InstalaciónEAContinuary Ejecución
📋 Requisitos

Python 3.8 o superior
pip (gestor de paquetes de Python)
Sistema operativo: Windows, macOS o Linux

⚙️ Instalación
bash# 1. Clonar o descargar el proyecto
git clone https://github.com/tuusuario/skyrunner.git
cd skyrunner

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
▶️ Ejecución
bash# Ejecutar el juego
python main.py
📦 Dependencias
txtpygame==2.5.0
numpy==1.24.0
scipy==1.11.0  # Para efectos de audio avanzados

🎮 Sistema de Juego
🕹️ Controles
TeclaAcción← → o A DMoverse izquierda/derechaSPACE o ↑ o WSaltarESCPausa / Volver al menúRReiniciar nivelQVolver al menú principalMSilenciar audioF1Fullscreen on/off
🎯 Sistema de Puntuación
python# Sistema de puntos (objects/constants.py)
POINTS_PLATFORM = 10          # Por tocar plataforma
POINTS_POWERUP = 50           # Por recoger power-up
POINTS_ENEMY_KILL = 100       # Por eliminar enemigo
POINTS_LEVEL_COMPLETE = 500   # Por completar nivel
TIME_BONUS_MULTIPLIER = 2     # Multiplicador por tiempo

# Cálculo final (objects/game.py)
def calculate_score(time, lives, level):
    base_points = POINTS_LEVEL_COMPLETE
    time_bonus = max(0, 90 - time) * 50
    lives_bonus = lives * 1000
    
    total = (base_points + time_bonus + lives_bonus) * difficulty_multiplier
    return total
🔥 Sistema de Combos
python# Combo con multiplicador (Models/player.py)
class Player:
    def add_combo(self, points=1):
        self.combo += points
        self.combo_timer = 3.0
        self.max_combo = max(self.max_combo, self.combo)
        
        # Multiplicador según combo
        if self.combo >= 15:
            self.combo_multiplier = 3.0
        elif self.combo >= 10:
            self.combo_multiplier = 2.0
        elif self.combo >= 5:
            self.combo_multiplier = 1.5
        
        return self.combo
🎁 Power-ups
Power-upEfectoDuración🛡️ EscudoProtección contra 1 golpe16s⚡ Velocidad+50% velocidad de movimiento12s🔍 ZoomAumenta tamaño del jugador14.4s🎯 ComboDoble puntos en combos8s⏳ Tiempo LentoRalentiza enemigos (futuro)8s🧲 ImánAtrae power-ups (futuro)8s
🌋 Sistema de Lava
python# Lava dinámica con aceleración (Models/lava.py)
class Lava:
    def update(self, dt, player_y):
        # Velocidad base según dificultad
        self.current_speed = self.base_speed * self.progress_multiplier
        
        # Aceleración progresiva
        if distance_to_top < 800:
            multiplier = 1.0 + (4.0 * (1 - distance_to_top / 800))
            self.current_speed *= multiplier
        
        # Presión de escape (si jugador no se mueve)
        if self.escape_timer > self.escape_threshold:
            self.current_speed *= self.escape_multiplier
        
        # Movimiento
        self.y -= self.current_speed * dt * 60
🎚️ Niveles de Dificultad
🌱 Fácil

Gravedad: 0.35 (más baja)
Salto: 10.0 (controlado)
Velocidad lava: 0.5x
Enemigos: 40% menos
Daño: 50% reducido
Vidas: 5
Power-ups: 2x más frecuentes
Coyote time: 0.20s (generoso)

⚡ Normal

Gravedad: 0.5 (balanceado)
Salto: 12.0 (estándar)
Velocidad lava: 1.0x
Enemigos: 100% normales
Daño: 100% normal
Vidas: 3
Power-ups: frecuencia normal
Coyote time: 0.10s

🔥 Difícil

Gravedad: 0.7 (alta)
Salto: 14.0 (alto pero rápido)
Velocidad lava: 2.2x
Enemigos: 180% más
Daño: 150% aumentado
Vidas: 1
Power-ups: 40% menos
Coyote time: 0.05s (muy poco)


📚 Documentación Técnica
🧮 Algoritmos Implementados
1️⃣ Interpolación Lineal (LERP)
python# objects/utils.py
def lerp(start, end, t):
    """
    Linear Interpolation
    
    Fórmula: f(t) = start + (end - start) * t
    
    Donde:
    - t ∈ [0, 1]
    - t=0 → retorna start
    - t=1 → retorna end
    - 0<t<1 → valor intermedio
    """
    return start + (end - start) * t

# Uso en cámara suave
self.camera_y = lerp(self.camera_y, self.target_camera_y, 0.15)
Aplicaciones:

Movimiento suave de cámara
Transiciones de color
Animaciones de escala
Fade in/out

2️⃣ Movimiento Sinusoidal
python# objects/utils.py
def sine_wave(time, amplitude, frequency):
    """
    Genera onda sinusoidal
    
    Fórmula: y = A * sin(2π * f * t)
    
    Donde:
    - A = amplitude (altura de onda)
    - f = frequency (oscilaciones por segundo)
    - t = time (tiempo transcurrido)
    """
    return amplitude * math.sin(2 * math.pi * frequency * time)

# Uso en murciélagos
self.y = self.start_y + sine_wave(self.time, BAT_AMPLITUDE, 2)
Aplicaciones:

Patrón de vuelo de murciélagos
Oscilación de power-ups
Ondas de lava
Efectos de pulsación

3️⃣ Detección de Colisiones (AABB)
python# Axis-Aligned Bounding Box collision
def check_collision(rect1, rect2):
    """
    Algoritmo AABB (Axis-Aligned Bounding Box)
    
    Condiciones para colisión:
    1. rect1.left < rect2.right
    2. rect1.right > rect2.left
    3. rect1.top < rect2.bottom
    4. rect1.bottom > rect2.top
    """
    return rect1.colliderect(rect2)

# Uso en juego
player_rect = self.player.get_rect()
enemy_rect = enemy.get_rect()

if player_rect.colliderect(enemy_rect):
    self.player.take_damage(enemy.damage)
4️⃣ Pathfinding Simple (Patrullaje)
python# Models/drones.py
class SurveillanceDrone:
    def update(self, dt):
        # Algoritmo de patrullaje cíclico
        target = self.patrol_points[self.current_patrol_index]
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 10:  # Llegó al punto
            # Siguiente punto (grafo cíclico)
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
        else:
            # Moverse hacia el punto
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
5️⃣ Física de Salto (Cinemática)
python# Models/player.py
def update(self, dt, platforms):
    # Ecuaciones de movimiento:
    # v = v₀ + a*t
    # s = s₀ + v*t
    
    # Aplicar gravedad (aceleración constante)
    self.vel_y += GRAVITY  # a = 0.5 (gravedad)
    
    # Limitar velocidad terminal
    if self.vel_y > TERMINAL_VELOCITY:
        self.vel_y = TERMINAL_VELOCITY
    
    # Actualizar posición
    self.y += self.vel_y  # s = s₀ + v*t
    
    # Salto (velocidad inicial negativa)
    if jump_pressed and can_jump:
        self.vel_y = JUMP_FORCE  # v₀ = -15 (hacia arriba)
```

**Fórmulas**:
```
Gravedad: a = 0.5 m/s²
Salto: v₀ = -15 m/s
Velocidad: v(t) = v₀ + a*t
Posición: y(t) = y₀ + v₀*t + ½*a*t²
6️⃣ Generación Procedural de Niveles
python# Levels/level.py
def _generate_extended_platforms(self):
    """
    Algoritmo de generación procedural
    
    1. Crear plataforma inicial (spawn)
    2. Loop para N plataformas:
       a. Calcular Y con espaciado
       b. Calcular X con variación
       c. Decidir tipo (estática vs móvil)
       d. Crear plataforma
    3. Crear plataforma final (castillo)
    """
    current_y = SCREEN_HEIGHT - 100
    
    for i in range(platform_count):
        # Espaciado vertical variable
        if i % 5 == 0:
            current_y -= PLATFORM_VERTICAL_SPACING * 1.5
        else:
            current_y -= PLATFORM_VERTICAL_SPACING
        
        # Posición horizontal según patrón
        if i % 3 == 0:
            x = random.randint(50, SCREEN_WIDTH // 2 - 50)
        elif i % 3 == 1:
            x = random.randint(SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH - 50)
        else:
            x = random.randint(SCREEN_WIDTH // 2 - 100, SCREEN_WIDTH // 2 + 100)
        
        # Decidir tipo con probabilidad
        if random.random() < move_chance:
            platform = MovingPlatform(x, current_y, width)
        else:
            platform = Platform(x, current_y, width)
7️⃣ Sistema de Partículas
python# objects/powerup.py
class ParticleSystem:
    def create_particle(self, x, y):
        """
        Sistema de partículas con física
        
        Ecuaciones:
        - Posición: p(t) = p₀ + v*t
        - Velocidad: v(t) = v₀ + a*t
        - Vida: life(t) = life₀ - decay*t
        """
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        
        particle = {
            'x': x,
            'y': y,
            'vx': math.cos(angle) * speed,  # Componente X de velocidad
            'vy': math.sin(angle) * speed,  # Componente Y de velocidad
            'life': random.uniform(0.5, 1.0),
            'size': random.uniform(2, 4),
            'color': self.color
        }
        
        self.particles.append(particle)
    
    def update_particles(self, dt):
        for p in self.particles[:]:
            # Física de movimiento
            p['x'] += p['vx'] * dt  # Traslación X
            p['y'] += p['vy'] * dt  # Traslación Y
            p['vy'] += 0.15 * dt    # Gravedad
            
            # Decaimiento
            p['life'] -= dt
            
            # Eliminar si murió
            if p['life'] <= 0:
                self.particles.remove(p)
```

### 🎨 Sistema de Renderizado

#### Pipeline de Dibujado
```
Frame Loop (60 FPS)
    ↓
1. Limpiar Screen
    ↓
2. Dibujar Fondo con Parallax
   ├─ Layer Far (speed: 0.2)
   ├─ Layer Mid (speed: 0.5)
   └─ Layer Near (speed: 0.8)
    ↓
3. Dibujar Tiles del Nivel
   └─ Solo tiles en viewport (culling)
    ↓
4. Dibujar Plataformas
   ├─ Plataformas estáticas
   └─ Plataformas móviles
    ↓
5. Dibujar Lava
   ├─ Superficie ondulante
   ├─ Burbujas
   └─ Partículas
    ↓
6. Dibujar Power-ups
   ├─ Glow effect
   ├─ Sprite animado
   └─ Partículas
    ↓
7. Dibujar Enemigos
   └─ Por orden de profundidad
    ↓
8. Dibujar Jugador
   ├─ Sprite base
   ├─ Efectos (escudo, velocidad)
   └─ Indicadores
    ↓
9. Dibujar Efectos de Pantalla
   ├─ Screen shake
   └─ Transiciones
    ↓
10. Dibujar HUD
    ├─ Barra de vida
    ├─ Puntuación
    ├─ Combo
    └─ Power-ups activos
    ↓
11. Flip Display Buffer
🔊 Sistema de Audio
python# objects/audio.py
class AudioManager:
    def __init__(self):
        """
        Sistema de audio con síntesis procedural
        
        Usa NumPy para generar ondas de audio
        """
        pygame.mixer.set_num_channels(16)  # 16 canales simultáneos
        
        self.sfx_volume = 0.85
        self.music_volume = 0.65
        
        # Crear sonidos procedurales
        self._create_sfx()
        self._create_music()
    
    def _create_jump_sound(self, pitch=1.0, duration=0.12):
        """
        Genera sonido de salto con síntesis de audio
        
        Técnica: Frequency sweep + envelope
        """
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        # Barrido de frecuencia (440Hz → 660Hz)
        t = np.linspace(0, duration, samples, False)
        freq_sweep = np.linspace(440 * pitch, 660 * pitch, samples)
        
        # Generar onda sinusoidal
        phase = np.cumsum(2 * np.pi * freq_sweep / sample_rate)
        wave = np.sin(phase)
        
        # Aplicar envelope ADSR
        attack = int(sample_rate * 0.01)
        release = int(sample_rate * 0.04)
        
        envelope = np.ones(samples)
        envelope[:attack] = np.linspace(0, 1, attack)      # Attack
        envelope[-release:] = np.linspace(1, 0, release)   # Release
        
        wave = wave * envelope * 0.6
        
        # Convertir a Sound de Pygame
        return self._numpy_to_sound(wave)

🚀 Retos y Soluciones
🔴 Reto 1: Colisiones Imprecisas
Problema: El jugador atravesaba plataformas o se quedaba atascado.
Solución:
python# Sistema de "platform stickiness" (objects/constants.py)
DIFFICULTY_SETTINGS = {
    "easy": {
        "platform_stickiness": 25,      # Margen generoso
        "fall_forgiveness": 15,         # Perdón al caer
    },
    "normal": {
        "platform_stickiness": 15,
        "fall_forgiveness": 8,
    },
    "hard": {
        "platform_stickiness": 5,       # Muy poco margen
        "fall_forgiveness": 2,
    }
}

# Implementación (Models/player.py)
def update(self, dt, platforms):
    for platform in platforms:
        if player_rect.colliderect(plat_rect):
            diff_y = player_rect.bottom - plat_rect.top
            
            # Colisión desde arriba con margen
            if self.vel_y >= 0 and diff_y >= 0 and diff_y <= 25:
                self.y = plat_rect.top - (player_rect.height // 2) + 5
                self.vel_y = 0
                self.on_ground = True
🔴 Reto 2: Performance con Muchas Partículas
Problema: FPS bajaban con +1000 partículas simultáneas.
Solución:
python# Object pooling + culling (objects/powerup.py)
class PowerUp:
    def __init__(self):
        self.particle_pool = []  # Pool pre-creado
        self.max_particles = 50  # Límite
    
    def update_particles(self, dt):
        # Solo actualizar partículas visibles
        for p in self.particles[:]:
            if not self.is_visible(p):
                continue  # Skip particles fuera de pantalla
            
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= dt
            
            if p['life'] <= 0:
                self.recycle_particle(p)  # Reciclar en vez de destruir
🔴 Reto 3: Sincronización de Audio
Problema: Música no sincronizaba con gameplay.
Solución:
python# Generación procedural con timing preciso (objects/audio.py)
class AudioManager:
    def _create_menu_music(self):
        # BPM definido para sincronización
        bpm = 120
        beat_duration = 60.0 / bpm  # 0.5 segundos por beat
        
        # Generar notas en beats exactos
        for beat in range(total_beats):
            beat_time = beat * beat_duration
            beat_sample = int(beat_time * sample_rate)
            
            # Colocar nota exactamente en el beat
            self.add_note_at(beat_sample, frequency, duration)
🔴 Reto 4: Generación de Niveles Monótona
Problema: Niveles muy predecibles.
Solución:
python# Algoritmo de variación con seeds (Levels/level.py)
def _generate_extended_platforms(self):
    # Usar posición Y como seed para consistencia
    random.seed(int(current_y))
    
    # Variación por sección
    for i in range(platform_count):
        # Cambiar patrón cada 5 plataformas
        if i % 5 == 0:
            spacing_multiplier = random.uniform(1.2, 1.8)
        
        # Posición con ruido Perlin (simulado)
        noise = math.sin(i * 0.618) * 50  # Golden ratio para variedad
        x = base_x + noise
        
        # Decisión probabilística de tipo
        move_chance = lerp(0.1, 0.4, i / platform_count)
🔴 Reto 5: Sistema de Vidas sin Respawn
Problema: Jugador no respawneaba correctamente al perder una vida.
Solución:
python# Sistema completo de vidas (Models/player.py)
def take_damage(self, damage):
    if self.invulnerable or self.shield_active:
        return False
    
    self.health -= damage
    
    if self.health <= 0:
        self.lives -= 1
        
        if self.lives > 0:
            # Respawn con salud completa
            self.health = PLAYER_MAX_HEALTH
            self.invulnerable = True
            self.invuln_timer = 2.0
            
            # Posición segura
            self.y = SCREEN_HEIGHT - 200
            self.x = SCREEN_WIDTH // 2
            self.vel_y = 0
            
            return True  # Perdió vida pero sigue vivo
        else:
            self.alive = False  # Muerte definitiva
            return True

🏆 Logros Técnicos
✅ Checklist de Requisitos

 Código depurado sin errores
 Código limpio y modular
 Identación correcta (PEP 8)
 Uso extensivo de funciones
 Estructuras de datos avanzadas
 Comentarios y documentación
 Separación lógica de archivos
 Transformaciones (traslación, rotación, escala)
 Vistas 2D con cámara dinámica
 Texturas (tilesets)
 Animaciones fluidas
 Paradigma OOP completo
 Programación basada en eventos
 Menú e interfaz completos
 Producto final jugable y pulido
 Sistema de récords persistente

📊 Métricas del Proyecto
MétricaValorLíneas de código~8,500Clases principales25+Archivos Python30+Assets gráficos15+ spritesEfectos de sonido20+Niveles3 completosEnemigos únicos5 tiposPower-ups6 tiposEstados del juego7 estadosFPS objetivo60 constante

👨‍💻 Créditos
Desarrollo

Programador Principal: [Tu Nombre]
Diseño de Niveles: [Tu Nombre]
Sistema de Audio: [Tu Nombre]

Herramientas

Motor: Pygame 2.5.0
Lenguaje: Python 3.8+
Editor: Visual Studio Code
Control de versiones: Git

Assets

Sprites de Jugador: Elaboración propia
Tilesets: Blue.png y Terrain.png
Efectos de Sonido: Generación procedural con NumPy
Música: Síntesis procedural

Agradecimientos

Comunidad de Pygame
Stack Overflow
Documentación de Pygame
Terna evaluadora
