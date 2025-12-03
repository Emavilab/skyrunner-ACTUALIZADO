# constants.py - CONSTANTES EXPANDIDAS

# ============= CONFIGURACIÓN DE VENTANA =============
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# ============= FÍSICA BASE (valores por defecto) =============
BASE_GRAVITY = 0.6
BASE_JUMP_FORCE = -18
BASE_PLAYER_SPEED = 7
TERMINAL_VELOCITY = 20

# Añade esta línea:
GRAVITY = BASE_GRAVITY * 100  # O ajusta según necesites

# ============= JUGADOR =============
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 50
PLAYER_MAX_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_LIVES = 3  # <-- Añadida esta línea
PLAYER_COLOR = (0, 200, 255)

# ============= PLATAFORMAS =============
PLATFORM_WIDTH = 120
PLATFORM_HEIGHT = 20
PLATFORM_VERTICAL_SPACING = 80

# ============= ENEMIGOS =============
BAT_WIDTH = 35
BAT_HEIGHT = 30
BAT_SPEED = 1.5
BAT_AMPLITUDE = 40

TRAP_SIZE = 40
TRAP_ROTATION_SPEED = 2

ROCK_SIZE = 30
ROCK_FALL_SPEED = 3

LIGHTNING_WIDTH = 15
LIGHTNING_HEIGHT = 100

# ============= POWER-UPS =============
POWERUP_SIZE = 25
POWERUP_DURATION = 8
SHIELD_COLOR = (255, 215, 0)
SPEED_COLOR = (255, 100, 100)
ZOOM_COLOR = (100, 255, 100)

# ============= COLORES =============
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 100, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# ============= SISTEMA DE DIFICULTAD COMPLETO =============
DIFFICULTY_SETTINGS = {
    "easy": {
        "name": "🌱 FÁCIL",
        "color": (100, 255, 100),
        
        # FÍSICA DEL JUGADOR (lo más importante)
        "player_speed": 5.5,           # Más lento para mayor control
        "jump_strength": 10.0,         # Salto más controlado
        "gravity": 0.35,               # Gravedad MUCHO más baja
        "double_jump": True,           # Doble salto por defecto
        "lives": 5,                    # Más vidas
        "health": 150,                 # Más salud
        "coyote_time": 0.20,           # Más tiempo para saltar después de caer
        
        # STICKINESS (adherencia a plataformas)
        "platform_stickiness": 25,     # Margen muy generoso
        "fall_forgiveness": 15,        # Perdón al caer (píxeles)
        
        # ELEMENTOS DEL NIVEL
        "scroll_speed": 2,
        "enemy_rate": 0.4,             # Muchos menos enemigos
        "enemy_speed_multiplier": 0.7, # Enemigos más lentos
        "enemy_damage_multiplier": 0.5,# Enemigos hacen menos daño
        "platform_gap": (50, 120),     # Huecos más pequeños
        "powerup_rate": 2.0,           # Muchos más power-ups
        "powerup_duration_multiplier": 1.5, # Power-ups duran más
        
        # LAVA
        "lava_speed": 0.5,
        "lava_acceleration": 0.0003,
        "lava_warning_time": 4.0,      # Más tiempo de advertencia
        
        # AUDIO
        "music_volume": 0.6,
        "sfx_volume": 0.7,
        
        # PUNTUACIÓN
        "score_multiplier": 0.8        # Menos puntos en fácil
    },
    "normal": {
        "name": "⚡ NORMAL",
        "color": (255, 255, 100),
        
        # FÍSICA DEL JUGADOR
        "player_speed": 7.0,
        "jump_strength": 12.0,
        "gravity": 0.5,
        "double_jump": False,
        "lives": 3,
        "health": 100,
        "coyote_time": 0.10,
        
        # STICKINESS
        "platform_stickiness": 15,
        "fall_forgiveness": 8,
        
        # ELEMENTOS DEL NIVEL
        "scroll_speed": 4,
        "enemy_rate": 1.0,
        "enemy_speed_multiplier": 1.0,
        "enemy_damage_multiplier": 1.0,
        "platform_gap": (70, 160),
        "powerup_rate": 1.0,
        "powerup_duration_multiplier": 1.0,
        
        # LAVA
        "lava_speed": 1.0,
        "lava_acceleration": 0.0008,
        "lava_warning_time": 2.5,
        
        # AUDIO
        "music_volume": 0.7,
        "sfx_volume": 0.8,
        
        # PUNTUACIÓN
        "score_multiplier": 1.0
    },
    "hard": {
        "name": "🔥 DIFÍCIL",
        "color": (255, 100, 100),
        
        # FÍSICA DEL JUGADOR
        "player_speed": 8.5,
        "jump_strength": 14.0,
        "gravity": 0.7,                # Gravedad más alta
        "double_jump": False,
        "lives": 1,
        "health": 80,
        "coyote_time": 0.05,           # Muy poco tiempo para reaccionar
        
        # STICKINESS
        "platform_stickiness": 5,      # Muy poco margen
        "fall_forgiveness": 2,         # Casi ningún perdón
        
        # ELEMENTOS DEL NIVEL
        "scroll_speed": 6,
        "enemy_rate": 1.8,
        "enemy_speed_multiplier": 1.4,
        "enemy_damage_multiplier": 1.5,
        "platform_gap": (90, 200),
        "powerup_rate": 0.4,
        "powerup_duration_multiplier": 0.7,
        
        # LAVA
        "lava_speed": 2.2,
        "lava_acceleration": 0.003,
        "lava_warning_time": 0.8,
        
        # AUDIO
        "music_volume": 0.8,
        "sfx_volume": 0.9,
        
        # PUNTUACIÓN
        "score_multiplier": 1.5        # Más puntos en difícil
    }
}

# ============= SISTEMA DE LAVA =============
LAVA_CONFIG = {
    "height": 60,
    "wave_amplitude": 15,
    "particle_density": 30,
    "damage": 1000,
    
    "colors": {
        "surface": (255, 70, 0),
        "middle": (255, 120, 30),
        "deep": (180, 40, 0),
        "glow": (255, 180, 80)
    }
}

# Colores por nivel
LEVEL_COLORS = {
    1: {'bg': (34, 139, 34), 'platform': (139, 69, 19), 'accent': (0, 100, 0)},
    2: {'bg': (64, 64, 64), 'platform': (105, 105, 105), 'accent': (139, 69, 19)},
    3: {'bg': (70, 130, 180), 'platform': (200, 200, 255), 'accent': (255, 255, 0)}
}

# Configuración de niveles
LEVELS_CONFIG = {
    1: {'name': 'Bosque Místico', 'platforms': 10, 'bats': 2, 'traps': 1, 'rocks': 0, 'lightning': 0, 'powerups': 4},
    2: {'name': 'Caverna Oscura', 'platforms': 12, 'bats': 3, 'traps': 2, 'rocks': 1, 'lightning': 0, 'powerups': 5},
    3: {'name': 'Tormenta Eléctrica', 'platforms': 15, 'bats': 3, 'traps': 2, 'rocks': 2, 'lightning': 2, 'powerups': 6}
}

# Puntuación
POINTS_PLATFORM = 10
POINTS_POWERUP = 50
POINTS_ENEMY_KILL = 100
POINTS_LEVEL_COMPLETE = 500
TIME_BONUS_MULTIPLIER = 2

# Cámara
CAMERA_SMOOTHING = 0.15
CAMERA_OFFSET_Y = 300

# UI
FONT_SIZE_TITLE = 64
FONT_SIZE_SUBTITLE = 32
FONT_SIZE_HUD = 24
FONT_SIZE_SMALL = 20

# Estados del juego
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_PAUSED = 'paused'
STATE_GAME_OVER = 'game_over'
STATE_LEVEL_COMPLETE = 'level_complete'
STATE_VICTORY = 'victory'
STATE_HIGH_SCORES = 'high_scores'
STATE_DIFFICULTY_SELECT = 'difficulty_select'

# High scores
HIGH_SCORES_FILE = 'highscores.json'
MAX_HIGH_SCORES = 10

# Audio
ENABLE_SOUND = True