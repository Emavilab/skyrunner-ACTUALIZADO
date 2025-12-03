"""
tile_manager.py - Sistema que usa imágenes Blue.png y Terrain.png como tilesets
"""

import pygame
import random
import os
from objects.constants import *

class Tile:
    """Representa un tile individual del tileset"""
    def __init__(self, x, y, tile_id, tileset_type, tile_size=64):
        self.x = x
        self.y = y
        self.tile_id = tile_id  # ID dentro del tileset (0, 1, 2...)
        self.tileset_type = tileset_type  # 'blue' o 'terrain'
        self.tile_size = tile_size
        self.width = tile_size
        self.height = tile_size
        
        # Determinar si es colisionable
        self.collidable = self.is_collidable()
        
        # Sprite
        self.sprite = None
        
    def is_collidable(self):
        """Determina si este tile específico es colisionable"""
        # Los tiles de suelo son colisionables, los decorativos no
        if self.tileset_type == 'blue':
            # Los tiles azules 0-3 son plataformas, 4+ son decoración
            return self.tile_id < 4
        elif self.tileset_type == 'terrain':
            # Los tiles de terreno 0-2 son suelo, 3+ son decoración
            return self.tile_id < 3
        return True
    
    def load_sprite(self, tileset_image, tile_width=32, tile_height=32):
        """Carga el sprite específico desde el tileset"""
        try:
            # Calcular posición en el tileset
            tiles_per_row = tileset_image.get_width() // tile_width
            tile_x = (self.tile_id % tiles_per_row) * tile_width
            tile_y = (self.tile_id // tiles_per_row) * tile_height
            
            # Extraer tile
            tile_rect = pygame.Rect(tile_x, tile_y, tile_width, tile_height)
            tile_surface = tileset_image.subsurface(tile_rect).copy()
            
            # Escalar si es necesario
            if tile_width != self.tile_size or tile_height != self.tile_size:
                self.sprite = pygame.transform.scale(tile_surface, 
                                                   (self.tile_size, self.tile_size))
            else:
                self.sprite = tile_surface
                
        except Exception as e:
            print(f"[Tile] Error cargando tile {self.tile_id}: {e}")
            # Crear tile de color como fallback
            self.create_fallback_sprite()
    
    def create_fallback_sprite(self):
        """Crea un sprite simple si falla la carga"""
        surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        
        if self.tileset_type == 'blue':
            # Azules
            colors = [
                (100, 100, 255),  # Tile 0
                (80, 80, 220),    # Tile 1
                (60, 60, 200),    # Tile 2
                (120, 120, 255),  # Tile 3
                (150, 150, 255),  # Tile 4
                (180, 180, 255)   # Tile 5
            ]
        else:  # terrain
            # Marrones/verdes
            colors = [
                (139, 69, 19),    # Tile 0 - tierra
                (34, 139, 34),    # Tile 1 - hierba
                (160, 82, 45),    # Tile 2 - tierra oscura
                (107, 142, 35),   # Tile 3 - hierba clara
                (85, 107, 47),    # Tile 4 - musgo
                (188, 143, 143)   # Tile 5 - tierra clara
            ]
        
        color = colors[self.tile_id % len(colors)]
        pygame.draw.rect(surf, color, (0, 0, self.tile_size, self.tile_size))
        
        # Patrón según ID
        if self.tile_id == 1:  # Hierba
            pygame.draw.rect(surf, (0, 100, 0), 
                           (0, 0, self.tile_size, 8))
        elif self.tile_id == 2:  # Tierra con piedras
            for _ in range(5):
                stone_x = random.randint(5, self.tile_size - 5)
                stone_y = random.randint(5, self.tile_size - 5)
                pygame.draw.circle(surf, (100, 100, 100), 
                                 (stone_x, stone_y), 3)
        
        # Borde
        pygame.draw.rect(surf, (255, 255, 255), 
                        (0, 0, self.tile_size, self.tile_size), 1)
        
        # ID de debug
        font = pygame.font.Font(None, 12)
        id_text = font.render(str(self.tile_id), True, (255, 255, 255))
        surf.blit(id_text, (5, 5))
        
        self.sprite = surf
    
    def get_rect(self):
        """Retorna rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface, camera_y=0):
        """Dibuja el tile"""
        screen_y = self.y - camera_y
        
        # Solo dibujar si está en pantalla
        if -self.tile_size < screen_y < SCREEN_HEIGHT + self.tile_size:
            if self.sprite:
                surface.blit(self.sprite, (self.x, screen_y))
            else:
                # Dibujar rectángulo de color si no hay sprite
                color = (100, 100, 255) if self.tileset_type == 'blue' else (139, 69, 19)
                pygame.draw.rect(surface, color,
                               (self.x, screen_y, self.width, self.height))

class TileManager:
    """Gestiona todo el sistema de tiles del nivel"""
    
    def __init__(self, level_number):
        self.level_number = level_number
        self.tile_size = 64
        self.tiles = []
        self.platform_tiles = []  # Tiles que funcionan como plataformas
        
        # Cargar tilesets
        self.blue_tileset = None
        self.terrain_tileset = None
        self.load_tilesets()
        
        # Construir nivel
        self.build_level()
    
    def load_tilesets(self):
        """Carga las imágenes de los tilesets"""
        try:
            # Cargar Blue.png
            blue_path = "./Assets/Terrain/Blue.png"
            if os.path.exists(blue_path):
                self.blue_tileset = pygame.image.load(blue_path).convert_alpha()
                print(f"[TileManager] Blue tileset cargado: {blue_path}")
            else:
                print(f"[TileManager] No se encontró {blue_path}")
                
            # Cargar Terrain.png
            terrain_path = "./Assets/Terrain/Terrain.png"
            if os.path.exists(terrain_path):
                self.terrain_tileset = pygame.image.load(terrain_path).convert_alpha()
                print(f"[TileManager] Terrain tileset cargado: {terrain_path}")
            else:
                print(f"[TileManager] No se encontró {terrain_path}")
                
        except Exception as e:
            print(f"[TileManager ERROR] No se pudieron cargar tilesets: {e}")
    
    def create_tile(self, x, y, tile_id, tileset_type):
        """Crea un tile y carga su sprite"""
        tile = Tile(x, y, tile_id, tileset_type, self.tile_size)
        
        # Cargar sprite del tileset correspondiente
        if tileset_type == 'blue' and self.blue_tileset:
            tile.load_sprite(self.blue_tileset, 32, 32)
        elif tileset_type == 'terrain' and self.terrain_tileset:
            tile.load_sprite(self.terrain_tileset, 32, 32)
        else:
            tile.create_fallback_sprite()
        
        # Añadir a listas
        self.tiles.append(tile)
        if tile.collidable:
            self.platform_tiles.append(tile)
        
        return tile
    
    def build_level(self):
        """Construye el nivel usando tiles"""
        print(f"[TileManager] Construyendo nivel {self.level_number} con tiles...")
        
        if self.level_number == 1:
            self.build_forest_level()
        elif self.level_number == 2:
            self.build_cave_level()
        elif self.level_number == 3:
            self.build_storm_level()
        else:
            self.build_default_level()
    
    def build_forest_level(self):
        """Nivel 1: Bosque con tiles de terreno"""
        print("[TileManager] Construyendo bosque...")
        
        # ============================================
        # 🌳 SUELO BASE (Terrain tiles)
        # ============================================
        for x in range(0, SCREEN_WIDTH + self.tile_size, self.tile_size):
            y = SCREEN_HEIGHT - self.tile_size
            # Usar tile de hierba (tile_id 1) para el suelo
            tile = self.create_tile(x, y, 1, 'terrain')
        
        # ============================================
        # 🪨 PLATAFORMAS ESCALONADAS (Blue tiles)
        # ============================================
        platform_positions = [
            # (x, y, ancho_en_tiles, altura_en_tiles)
            (200, 600, 4, 1),
            (500, 520, 3, 1),
            (300, 440, 5, 1),
            (700, 440, 3, 2),  # Plataforma doble altura
            (150, 360, 2, 1),
            (600, 300, 4, 1),
            (250, 220, 3, 1),
            (800, 160, 4, 1),  # Plataforma final más alta
        ]
        
        for i, (x, y, width, height) in enumerate(platform_positions):
            is_final = (i == len(platform_positions) - 1)
            
            for row in range(height):
                for col in range(width):
                    tile_x = x + (col * self.tile_size)
                    tile_y = y - (row * self.tile_size)
                    
                    # Determinar qué tile usar según posición
                    if row == 0:  # Fila superior
                        if col == 0:  # Esquina izquierda
                            tile_id = 0
                        elif col == width - 1:  # Esquina derecha
                            tile_id = 2
                        else:  # Centro
                            tile_id = 1
                    else:  # Filas inferiores (para plataformas dobles)
                        tile_id = 3 + col % 2
                    
                    tile = self.create_tile(tile_x, tile_y, tile_id, 'blue')
                    
                    if is_final and col == width // 2 and row == 0:
                        self.final_platform = tile
        
        # ============================================
        # 🌿 DECORACIÓN (Terrain tiles decorativos)
        # ============================================
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH - self.tile_size)
            y = random.randint(0, SCREEN_HEIGHT - 300)
            
            # Verificar que no colisione
            if not self.check_collision_at(x, y):
                # Usar tiles decorativos (ID 3-5)
                tile_id = random.choice([3, 4, 5])
                tile = self.create_tile(x, y, tile_id, 'terrain')
                tile.collidable = False  # Decoración no colisionable
    
    def build_cave_level(self):
        """Nivel 2: Caverna con mezcla de tiles"""
        print("[TileManager] Construyendo caverna...")
        
        # ============================================
        # 🗿 PAREDES Y SUELO (Terrain tiles)
        # ============================================
        # Pared izquierda
        for y in range(0, SCREEN_HEIGHT, self.tile_size):
            tile = self.create_tile(0, y, 2, 'terrain')  # Tierra oscura
        
        # Pared derecha
        for y in range(0, SCREEN_HEIGHT, self.tile_size):
            tile = self.create_tile(SCREEN_WIDTH - self.tile_size, y, 2, 'terrain')
        
        # Suelo rocoso
        for x in range(self.tile_size, SCREEN_WIDTH - self.tile_size, self.tile_size):
            y = SCREEN_HEIGHT - self.tile_size
            tile_id = random.choice([2, 4, 5])  # Variedad de tierra/piedra
            tile = self.create_tile(x, y, tile_id, 'terrain')
        
        # ============================================
        # 💎 PLATAFORMAS DE CRISTAL (Blue tiles)
        # ============================================
        cave_platforms = [
            (150, 600, 4, 1),
            (450, 530, 3, 1),
            (200, 460, 5, 1),
            (650, 460, 2, 2),
            (350, 380, 4, 1),
            (700, 320, 3, 1),
            (250, 260, 6, 1),
            (550, 200, 4, 1),  # Salida
        ]
        
        for i, (x, y, width, height) in enumerate(cave_platforms):
            is_exit = (i == len(cave_platforms) - 1)
            
            for row in range(height):
                for col in range(width):
                    tile_x = x + (col * self.tile_size)
                    tile_y = y - (row * self.tile_size)
                    
                    # Tiles azules brillantes para plataformas de cristal
                    tile_id = (4 + row + col) % 6  # Variedad
                    tile = self.create_tile(tile_x, tile_y, tile_id, 'blue')
                    
                    if is_exit and col == width // 2:
                        self.final_platform = tile
        
        # ============================================
        # 🔦 ILUMINACIÓN (Blue tiles decorativos)
        # ============================================
        for _ in range(10):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, 400)
            
            if not self.check_collision_at(x, y):
                # Tiles azules brillantes como luz
                tile_id = random.choice([4, 5])
                tile = self.create_tile(x, y, tile_id, 'blue')
                tile.collidable = False
    
    def build_storm_level(self):
        """Nivel 3: Tormenta con plataformas flotantes"""
        print("[TileManager] Construyendo nivel de tormenta...")
        
        # ============================================
        # ☁️ PLATAFORMAS FLOTANTES (Blue tiles)
        # ============================================
        floating_platforms = [
            (180, 650, 2, 1),
            (450, 580, 3, 1),
            (120, 510, 2, 2),  # Doble altura
            (600, 470, 4, 1),
            (280, 410, 3, 1),
            (700, 360, 2, 1),
            (380, 300, 5, 1),
            (550, 240, 3, 1),
            (220, 180, 4, 1),  # Cima
        ]
        
        for i, (x, y, width, height) in enumerate(floating_platforms):
            is_top = (i == len(floating_platforms) - 1)
            
            for row in range(height):
                for col in range(width):
                    tile_x = x + (col * self.tile_size)
                    tile_y = y - (row * self.tile_size)
                    
                    # Tiles azules eléctricos
                    if is_top and row == 0:
                        tile_id = 5  # Tile más brillante para la cima
                    else:
                        tile_id = (3 + row * 2 + col) % 6
                    
                    tile = self.create_tile(tile_x, tile_y, tile_id, 'blue')
                    
                    if is_top and col == width // 2:
                        self.final_platform = tile
        
        # ============================================
        # ⚡ NUBES Y RAYOS (Terrain tiles decorativos)
        # ============================================
        for _ in range(15):
            x = random.randint(0, SCREEN_WIDTH - self.tile_size)
            y = random.randint(50, SCREEN_HEIGHT - 200)
            
            if random.random() > 0.5:  # 50% probabilidad
                # Nubes (tiles claros)
                tile_id = random.choice([4, 5])
                tile = self.create_tile(x, y, tile_id, 'terrain')
                tile.collidable = False
    
    def build_default_level(self):
        """Nivel por defecto"""
        print("[TileManager] Construyendo nivel por defecto...")
        
        # Suelo simple
        for x in range(0, SCREEN_WIDTH + self.tile_size, self.tile_size):
            y = SCREEN_HEIGHT - self.tile_size
            tile = self.create_tile(x, y, 0, 'terrain')
        
        # Plataformas básicas
        for i in range(5):
            x = 200 + (i * 180)
            y = 500 - (i * 90)
            width = 3
            
            for j in range(width):
                tile_x = x + (j * self.tile_size)
                tile_id = 1 if j == 1 else 0 if j == 0 else 2
                tile = self.create_tile(tile_x, y, tile_id, 'blue')
                
                if i == 4 and j == 1:
                    self.final_platform = tile
    
    def check_collision_at(self, x, y):
        """Verifica si hay colisión en una posición"""
        test_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
        
        for tile in self.tiles:
            if tile.collidable and tile.get_rect().colliderect(test_rect):
                return True
        return False
    
    def get_platforms(self):
        """Retorna tiles colisionables como plataformas"""
        return self.platform_tiles
    
    def get_final_platform(self):
        """Retorna la plataforma final"""
        return self.final_platform
    
    def draw(self, surface, camera_y=0):
        """Dibuja todos los tiles"""
        for tile in self.tiles:
            tile.draw(surface, camera_y)
    
    def draw_background(self, surface, camera_y=0):
        """Dibuja fondo según nivel"""
        # Gradiente de fondo
        for y in range(SCREEN_HEIGHT):
            screen_y = y
            
            if self.level_number == 1:  # Bosque
                r = int(100 * (1 - y/SCREEN_HEIGHT) + 34 * (y/SCREEN_HEIGHT))
                g = int(180 * (1 - y/SCREEN_HEIGHT) + 139 * (y/SCREEN_HEIGHT))
                b = int(100 * (1 - y/SCREEN_HEIGHT) + 34 * (y/SCREEN_HEIGHT))
            elif self.level_number == 2:  # Caverna
                r = int(30 * (1 - y/SCREEN_HEIGHT) + 10 * (y/SCREEN_HEIGHT))
                g = int(30 * (1 - y/SCREEN_HEIGHT) + 10 * (y/SCREEN_HEIGHT))
                b = int(40 * (1 - y/SCREEN_HEIGHT) + 20 * (y/SCREEN_HEIGHT))
            else:  # Tormenta
                r = int(80 * (1 - y/SCREEN_HEIGHT) + 40 * (y/SCREEN_HEIGHT))
                g = int(100 * (1 - y/SCREEN_HEIGHT) + 60 * (y/SCREEN_HEIGHT))
                b = int(150 * (1 - y/SCREEN_HEIGHT) + 100 * (y/SCREEN_HEIGHT))
            
            pygame.draw.line(surface, (r, g, b), (0, screen_y), (SCREEN_WIDTH, screen_y))