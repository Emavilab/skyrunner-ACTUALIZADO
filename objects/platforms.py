"""
platforms.py - Clases de Plataformas con Tilesets REALES
Usa Blue.png y Terrain.png como gráficos
"""

import pygame
import random
import math
import os
from objects.constants import *

# ============================================
# 🎨 TILESET MANAGER (PRIMERO - carga las imágenes)
# ============================================

class TilesetManager:
    """Maneja la carga y extracción de tiles de Blue.png y Terrain.png"""
    
    def __init__(self):
        self.tilesets = {}
        self.tile_size = 32  # Tamaño original en los archivos PNG
        self._loaded = False  # Bandera para carga diferida
    
    def ensure_loaded(self):
        """Carga los tilesets solo cuando se necesitan por primera vez"""
        if not self._loaded:
            self.load_tilesets()
            self._loaded = True
    
    def load_tilesets(self):
        """Carga los tilesets desde los archivos"""
        try:
            # Cargar Blue.png
            blue_path = "./Assets/Terrain/Blue.png"
            if os.path.exists(blue_path):
                # Usar convert() en lugar de convert_alpha() para evitar el error
                self.tilesets['blue'] = pygame.image.load(blue_path).convert()
                self.tilesets['blue'].set_colorkey(self.tilesets['blue'].get_at((0, 0)))

                # Añadir transparencia manualmente si es necesario
                self.tilesets['blue'].set_colorkey((0, 0, 0))  # Negro como transparente
                print(f"[Tileset] Blue.png cargado: {blue_path}")
            else:
                print(f"[Tileset ERROR] No se encontró {blue_path}")
                self.tilesets['blue'] = self.create_fallback_tileset('blue')
            
            # Cargar Terrain.png
            terrain_path = "./Assets/Terrain/Terrain.png"
            if os.path.exists(terrain_path):
                self.tilesets['terrain'] = pygame.image.load(terrain_path).convert()
                self.tilesets['terrain'].set_colorkey((0, 0, 0))
                print(f"[Tileset] Terrain.png cargado: {terrain_path}")
            else:
                print(f"[Tileset ERROR] No se encontró {terrain_path}")
                self.tilesets['terrain'] = self.create_fallback_tileset('terrain')
                
        except Exception as e:
            print(f"[Tileset ERROR] Error cargando tilesets: {e}")
            self.create_fallback_tilesets()
    
    def create_fallback_tileset(self, tileset_name):
        """Crea tileset de emergencia si no se cargan los archivos"""
        colors = {
            'blue': [
                (100, 100, 255), (80, 80, 220), (60, 60, 200),
                (120, 120, 255), (150, 150, 255), (180, 180, 255)
            ],
            'terrain': [
                (139, 69, 19), (34, 139, 34), (160, 82, 45),
                (107, 142, 35), (85, 107, 47), (188, 143, 143)
            ]
        }
        
        surf = pygame.Surface((self.tile_size * 8, self.tile_size * 8))
        
        for i in range(8):  # 8 filas
            for j in range(8):  # 8 columnas
                tile_idx = (i * 8 + j) % len(colors[tileset_name])
                color = colors[tileset_name][tile_idx]
                
                rect = pygame.Rect(j * self.tile_size, i * self.tile_size, 
                                 self.tile_size, self.tile_size)
                pygame.draw.rect(surf, color, rect)
                pygame.draw.rect(surf, (255, 255, 255), rect, 1)
        
        return surf
    
    def create_fallback_tilesets(self):
        """Crea ambos tilesets de emergencia"""
        self.tilesets['blue'] = self.create_fallback_tileset('blue')
        self.tilesets['terrain'] = self.create_fallback_tileset('terrain')
    
    def get_tile(self, tileset_name, tile_id, width, height):
        """
        Extrae un tile del tileset y lo escala al tamaño deseado.
        """
        # Asegurarse de que los tilesets están cargados
        self.ensure_loaded()
        
        if tileset_name not in self.tilesets:
            print(f"[Tileset ERROR] Tileset '{tileset_name}' no encontrado")
            return self.create_simple_tile(width, height, tileset_name)
        
        tileset = self.tilesets[tileset_name]
        tiles_per_row = tileset.get_width() // self.tile_size
        
        # Calcular posición en el tileset
        tile_x = (tile_id % tiles_per_row) * self.tile_size
        tile_y = (tile_id // tiles_per_row) * self.tile_size
        
        # Verificar que esté dentro del tileset
        if (tile_x + self.tile_size > tileset.get_width() or 
            tile_y + self.tile_size > tileset.get_height()):
            print(f"[Tileset WARN] Tile ID {tile_id} fuera de rango, usando tile 0")
            tile_x = 0
            tile_y = 0
        
        # Extraer tile
        try:
            tile_rect = pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size)
            tile = tileset.subsurface(tile_rect).copy()
            
            # Escalar al tamaño deseado
            if width != self.tile_size or height != self.tile_size:
                tile = pygame.transform.scale(tile, (width, height))
            
            return tile
        except:
            print(f"[Tileset ERROR] No se pudo extraer tile {tile_id}")
            return self.create_simple_tile(width, height, tileset_name)
    
    def create_simple_tile(self, width, height, tileset_name):
        """Crea un tile simple de color como fallback"""
        surf = pygame.Surface((width, height))
        
        if tileset_name == 'blue':
            color = (100, 100, 255)
        else:  # terrain
            color = (139, 69, 19)
        
        pygame.draw.rect(surf, color, (0, 0, width, height))
        pygame.draw.rect(surf, (255, 255, 255), (0, 0, width, height), 1)
        return surf

# Instancia global del tileset manager (NO carga todavía)
tileset_manager = TilesetManager()

# ============================================
# 🏗️ CLASE BASE PLATFORM (usa tilesets REALES)
# ============================================

class Platform:
    """Plataforma estática que usa imágenes de Blue.png y Terrain.png"""
    
    def __init__(self, x, y, width=PLATFORM_WIDTH, platform_type=1):
        """
        Inicializa una plataforma con gráficos reales.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT
        self.type = platform_type
        self.touched = False
        self.is_spawn = False
        self.is_final = False
        
        # Configuración según tipo
        if self.type == 1:  # Bosque - Usar Terrain.png
            self.tileset_name = 'terrain'
            # IDs sugeridos para plataformas de bosque
            self.tile_ids = {
                'left': 0,    # Borde izquierdo
                'middle': 1,  # Centro
                'right': 2    # Borde derecho
            }
        elif self.type == 2:  # Caverna - Usar Blue.png
            self.tileset_name = 'blue'
            # IDs sugeridos para plataformas de caverna
            self.tile_ids = {
                'left': 0,    # Borde izquierdo azul
                'middle': 1,  # Centro azul
                'right': 2    # Borde derecho azul
            }
        elif self.type == 3:  # Tormenta - Usar Blue.png con otros IDs
            self.tileset_name = 'blue'
            # IDs sugeridos para plataformas eléctricas
            self.tile_ids = {
                'left': 3,    # Borde eléctrico
                'middle': 4,  # Centro eléctrico
                'right': 5    # Borde eléctrico
            }
        else:
            # Default
            self.tileset_name = 'terrain'
            self.tile_ids = {'left': 0, 'middle': 1, 'right': 2}
        
        # El sprite se creará cuando se dibuje por primera vez
        self.sprite = None
    
    def create_sprite(self):
        """Crea un sprite compuesto de varios tiles del tileset"""
        # Crear superficie
        sprite = pygame.Surface((self.width, self.height))
        
        # Ancho de cada tile
        num_tiles = max(1, self.width // 32)
        tile_width = self.width // num_tiles
        
        for i in range(num_tiles):
            # Determinar qué tile usar según posición
            if i == 0:  # Primer tile - borde izquierdo
                tile_id = self.tile_ids['left']
            elif i == num_tiles - 1:  # Último tile - borde derecho
                tile_id = self.tile_ids['right']
            else:  # Tiles del medio
                tile_id = self.tile_ids['middle']
            
            # Obtener tile del tileset
            tile = tileset_manager.get_tile(
                self.tileset_name, 
                tile_id,
                tile_width,
                self.height
            )
            
            if tile:
                # Posicionar tile en el sprite
                sprite.blit(tile, (i * tile_width, 0))
            else:
                # Fallback: dibujar rectángulo de color
                color = (139, 69, 19) if self.tileset_name == 'terrain' else (100, 100, 255)
                pygame.draw.rect(sprite, color, 
                               (i * tile_width, 0, tile_width, self.height))
        
        return sprite
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2,
                          self.width, self.height)
    
    def update(self, dt):
        """Actualiza la plataforma"""
        pass
    
    def draw(self, surface, camera_offset):
        """Dibuja la plataforma usando sprite de tileset"""
        screen_y = self.y - camera_offset
        
        # No dibujar si está fuera de pantalla
        if screen_y < -50 or screen_y > SCREEN_HEIGHT + 50:
            return
        
        # Crear sprite si no existe
        if self.sprite is None:
            self.sprite = self.create_sprite()
        
        # Calcular posición para dibujar
        draw_x = self.x - self.width // 2
        draw_y = screen_y - self.height // 2
        
        # Dibujar sprite
        surface.blit(self.sprite, (draw_x, draw_y))

# ============================================
# 🚄 PLATAFORMA MÓVIL (usa los mismos tilesets)
# ============================================

class MovingPlatform(Platform):
    """
    Plataforma que se mueve horizontalmente usando tilesets.
    """
    
    def __init__(self, x, y, width=PLATFORM_WIDTH, platform_type=1,
                 move_range=100, speed=2):
        super().__init__(x, y, width, platform_type)
        self.start_x = x
        self.move_range = move_range
        self.speed = speed
        self.direction = 1
    
    def update(self, dt):
        """Actualiza la posición de la plataforma"""
        # Mover plataforma
        self.x += self.speed * self.direction
        
        # Cambiar dirección al llegar al límite
        if abs(self.x - self.start_x) > self.move_range:
            self.direction *= -1
    
    def draw(self, surface, camera_offset):
        """Dibuja la plataforma móvil con indicador"""
        # Dibujar plataforma base (usando el sprite del padre)
        super().draw(surface, camera_offset)
        
        screen_y = self.y - camera_offset
        
        # Indicador visual de que es móvil (flechas simples)
        arrow_color = YELLOW
        arrow_size = 5
        
        # Flecha izquierda
        left_x = self.x - self.width//2 - 15
        pygame.draw.polygon(surface, arrow_color, [
            (left_x, screen_y),
            (left_x - 8, screen_y - arrow_size),
            (left_x - 8, screen_y + arrow_size)
        ])
        
        # Flecha derecha
        right_x = self.x + self.width//2 + 15
        pygame.draw.polygon(surface, arrow_color, [
            (right_x, screen_y),
            (right_x + 8, screen_y - arrow_size),
            (right_x + 8, screen_y + arrow_size)
        ])

# ============================================
# 🏰 CASTILLO FINAL (también usa tilesets)
# ============================================

class CastlePlatform(Platform):
    """Plataforma final con apariencia de castillo usando tilesets"""
    
    def __init__(self, x, y, width=PLATFORM_WIDTH, platform_type=1):
        super().__init__(x, y, width, platform_type)
        self.is_final = True
        
        # Configuración de castillo según tipo
        if self.type == 1:  # Bosque
            self.castle_colors = {
                'wall': (90, 70, 50),
                'roof': (160, 40, 40),
                'gate': (120, 90, 60),
                'banner': (0, 150, 0)
            }
        elif self.type == 2:  # Caverna
            self.castle_colors = {
                'wall': (80, 80, 100),
                'roof': (100, 50, 50),
                'gate': (90, 70, 50),
                'banner': (150, 0, 150)
            }
        else:  # Tormenta
            self.castle_colors = {
                'wall': (100, 100, 120),
                'roof': (80, 80, 100),
                'gate': (70, 70, 90),
                'banner': (0, 150, 150)
            }
    
    def draw(self, surface, camera_offset):
        """Dibuja el castillo usando la plataforma base + decoraciones"""
        # Primero dibujar la plataforma base (con tileset)
        super().draw(surface, camera_offset)
        
        screen_y = self.y - camera_offset
        
        # Añadir elementos de castillo encima
        wall_height = 40
        wall_rect = pygame.Rect(
            self.x - self.width//2,
            screen_y - wall_height,
            self.width,
            wall_height
        )
        pygame.draw.rect(surface, self.castle_colors['wall'], wall_rect)
        
        # Detalles del muro
        for i in range(self.width // 40 - 1):
            window_x = self.x - self.width//2 + (i + 1) * 40
            pygame.draw.rect(surface, YELLOW,
                           (window_x - 7, screen_y - 20, 14, 25))

# ============================================
# BANDERA DE VICTORIA
# ============================================

class VictoryFlag:
    """Bandera de victoria estilo Mario Bros"""
    
    def __init__(self, x, y, level_type=1):
        self.x = x
        self.y = y
        self.base_y = y
        self.level_type = level_type
        self.height = 180
        self.width = 12
        
        # Animación
        self.raised = False
        self.raise_progress = 0.0
        self.raise_speed = 150
        
        # Color según nivel
        self.flag_colors = {
            1: (0, 200, 0),    # Verde bosque
            2: (180, 0, 180),  # Púrpura caverna
            3: (0, 200, 200)   # Cian tormenta
        }
    
    def raise_flag(self):
        """Comienza a izar la bandera"""
        if not self.raised:
            self.raised = True
            return True
        return False
    
    def update(self, dt):
        """Actualiza la animación de la bandera"""
        if self.raised and self.raise_progress < 1.0:
            self.raise_progress += dt * (self.raise_speed / self.height)
            self.raise_progress = min(self.raise_progress, 1.0)
    
    def draw(self, surface, camera_offset):
        """Dibuja la bandera completa"""
        screen_x = self.x
        screen_base_y = self.base_y - camera_offset
        
        # Calcular posición actual
        current_flag_y = self.base_y - (self.height * self.raise_progress)
        screen_flag_y = current_flag_y - camera_offset
        
        # Asta
        pole_rect = pygame.Rect(
            screen_x - self.width//2,
            screen_base_y - self.height,
            self.width,
            self.height
        )
        pygame.draw.rect(surface, (120, 120, 140), pole_rect)
        
        # Bandera
        flag_color = self.flag_colors.get(self.level_type, YELLOW)
        wave_offset = math.sin(pygame.time.get_ticks() * 0.003) * 5
        
        flag_points = [
            (screen_x + self.width//2, screen_flag_y),
            (screen_x + self.width//2 + 70 + wave_offset, screen_flag_y + 15),
            (screen_x + self.width//2 + 50, screen_flag_y + 70),
            (screen_x + self.width//2, screen_flag_y + 50)
        ]
        
        pygame.draw.polygon(surface, flag_color, flag_points)
        pygame.draw.polygon(surface, BLACK, flag_points, 3)
    
    def get_rect(self):
        """
        Retorna el rectángulo de colisión para la bandera.
        El área de colisión es alrededor de la base de la bandera.
        """
        # Área de colisión: un rectángulo en la base de la bandera
        collision_width = 50
        collision_height = 80
        return pygame.Rect(
            self.x - collision_width // 2,
            self.base_y - collision_height,
            collision_width,
            collision_height
        )
    
    def is_fully_raised(self):
        """Verifica si la bandera está completamente izada"""
        return self.raised and self.raise_progress >= 1.0