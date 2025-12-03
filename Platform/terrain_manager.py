"""
terrain_manager.py - Sistema de gestión de terrenos manual
Carga y dibuja tiles de Blue y Terrain
"""

import pygame
import os
import random
from objects.constants import *
from objects.utils import lerp

class TerrainTile:
    """Clase para un tile individual del terreno"""
    
    def __init__(self, x, y, tile_type, variant=0, tile_size=64):
        self.x = x
        self.y = y
        self.tile_type = tile_type  # 'blue' o 'terrain'
        self.variant = variant      # Variante del tile (0, 1, 2...)
        self.tile_size = tile_size
        self.width = tile_size
        self.height = tile_size
        
        # Cargar sprite
        self.sprite = self.load_tile_sprite()
        
        # Para colisiones (solo algunos tiles)
        self.collidable = True
        if tile_type == 'blue' and variant in [0, 1, 2]:  # Solo ciertos tiles azules son plataformas
            self.collidable = True
        elif tile_type == 'terrain':
            self.collidable = True
    
    def load_tile_sprite(self):
        """Carga el sprite del tile según su tipo"""
        try:
            # Rutas a tus carpetas de tiles
            if self.tile_type == 'blue':
                tile_path = f"./Assets/Terrain/Blue/blue_{self.variant}.png"
            else:  # 'terrain'
                tile_path = f"./Assets/Terrain/Terrain/terrain_{self.variant}.png"
            
            # Intentar cargar la imagen
            sprite = pygame.image.load(tile_path).convert_alpha()
            return pygame.transform.scale(sprite, (self.tile_size, self.tile_size))
            
        except:
            # Si falla, crear tile de colores
            print(f"[TerrainTile] No se pudo cargar tile: {self.tile_type}_{self.variant}")
            surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            
            if self.tile_type == 'blue':
                color = (100, 100, 255)  # Azul
            else:
                color = (139, 69, 19)    # Marrón terreno
                
            pygame.draw.rect(surf, color, (0, 0, self.tile_size, self.tile_size))
            pygame.draw.rect(surf, (255, 255, 255), (0, 0, self.tile_size, self.tile_size), 1)
            
            # Texto para debug
            font = pygame.font.Font(None, 20)
            text = font.render(f"{self.variant}", True, (255, 255, 255))
            surf.blit(text, (5, 5))
            
            return surf
    
    def get_rect(self):
        """Retorna rectángulo para colisiones"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface, camera_y=0):
        """Dibuja el tile"""
        screen_y = self.y - camera_y
        
        # Solo dibujar si está en pantalla
        if -self.tile_size < screen_y < SCREEN_HEIGHT + self.tile_size:
            surface.blit(self.sprite, (self.x, screen_y))
            
            # Debug: mostrar rectángulo de colisión
            # pygame.draw.rect(surface, (255, 0, 0, 100), 
            #                 (self.x, screen_y, self.width, self.height), 1)

class TerrainManager:
    """Gestor de todo el terreno del nivel"""
    
    def __init__(self, level_number):
        self.level_number = level_number
        self.tile_size = 64
        self.tiles = []
        self.platform_tiles = []  # Tiles que funcionan como plataformas
        
        # Configurar según nivel
        self.setup_level()
    
    def setup_level(self):
        """Configura el terreno según el nivel"""
        if self.level_number == 1:
            self.create_forest_level()
        elif self.level_number == 2:
            self.create_cave_level()
        elif self.level_number == 3:
            self.create_storm_level()
        else:
            self.create_default_level()
    
    def create_forest_level(self):
        """Crea nivel de bosque con tiles de terreno"""
        print("[TerrainManager] Creando nivel de bosque...")
        
        # Crear suelo base
        for x in range(0, SCREEN_WIDTH + self.tile_size, self.tile_size):
            y = SCREEN_HEIGHT - self.tile_size
            tile = TerrainTile(x, y, 'terrain', variant=0, tile_size=self.tile_size)
            self.tiles.append(tile)
            self.platform_tiles.append(tile)
        
        # Crear plataformas escalonadas
        platforms_data = [
            # (x, y, ancho_en_tiles)
            (200, 600, 3),
            (500, 500, 2),
            (300, 400, 4),
            (700, 400, 3),
            (100, 300, 2),
            (600, 250, 5),
            (200, 150, 3),
            (900, 100, 4)  # Plataforma final
        ]
        
        for x, y, width in platforms_data:
            for i in range(width):
                tile_x = x + (i * self.tile_size)
                # Usar tiles azules para plataformas especiales
                if i == 0:  # Borde izquierdo
                    variant = 0
                elif i == width - 1:  # Borde derecho
                    variant = 2
                else:  # Centro
                    variant = 1
                
                tile = TerrainTile(tile_x, y, 'blue', variant=variant, tile_size=self.tile_size)
                self.tiles.append(tile)
                self.platform_tiles.append(tile)
                
                # Si es la última plataforma, marcar como final
                if y == 100 and i == width - 2:
                    self.final_platform = tile
        
        # Añadir tiles de decoración (no colisionables)
        for _ in range(15):
            x = random.randint(0, SCREEN_WIDTH - self.tile_size)
            y = random.randint(0, SCREEN_HEIGHT - 200)
            
            # Solo decoración en áreas vacías
            if not self.check_collision_at(x, y):
                variant = random.choice([3, 4, 5])  # Variantes decorativas
                tile = TerrainTile(x, y, 'terrain', variant=variant, tile_size=self.tile_size)
                tile.collidable = False
                self.tiles.append(tile)
    
    def create_cave_level(self):
        """Crea nivel de caverna"""
        print("[TerrainManager] Creando nivel de caverna...")
        
        # Paredes laterales
        for y in range(0, SCREEN_HEIGHT, self.tile_size):
            # Pared izquierda
            tile_left = TerrainTile(0, y, 'terrain', variant=6, tile_size=self.tile_size)
            self.tiles.append(tile_left)
            
            # Pared derecha
            tile_right = TerrainTile(SCREEN_WIDTH - self.tile_size, y, 'terrain', variant=6, tile_size=self.tile_size)
            self.tiles.append(tile_right)
        
        # Plataformas en la caverna
        cave_platforms = [
            (100, 650, 4),
            (400, 550, 3),
            (150, 450, 5),
            (600, 450, 2),
            (300, 350, 4),
            (700, 300, 3),
            (200, 200, 6),
            (500, 150, 4)  # Salida de la caverna
        ]
        
        for x, y, width in cave_platforms:
            for i in range(width):
                tile_x = x + (i * self.tile_size)
                variant = random.choice([7, 8, 9])  # Variantes de roca
                
                tile = TerrainTile(tile_x, y, 'terrain', variant=variant, tile_size=self.tile_size)
                self.tiles.append(tile)
                self.platform_tiles.append(tile)
                
                if y == 150 and i == width // 2:
                    self.final_platform = tile
        
        # Estalactitas (decoración colgante)
        for _ in range(10):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(50, 300)
            tile = TerrainTile(x, y, 'blue', variant=4, tile_size=self.tile_size)
            tile.collidable = False
            self.tiles.append(tile)
    
    def create_storm_level(self):
        """Crea nivel de tormenta"""
        print("[TerrainManager] Creando nivel de tormenta...")
        
        # Plataformas flotantes
        floating_platforms = [
            (150, 650, 2),
            (400, 580, 3),
            (100, 500, 2),
            (600, 450, 4),
            (250, 380, 3),
            (700, 320, 2),
            (350, 250, 5),
            (550, 180, 3),
            (200, 100, 4)  # Cima
        ]
        
        for x, y, width in floating_platforms:
            for i in range(width):
                tile_x = x + (i * self.tile_size)
                
                # Plataformas eléctricas (azules)
                variant = random.choice([5, 6, 7])
                tile = TerrainTile(tile_x, y, 'blue', variant=variant, tile_size=self.tile_size)
                
                # Efecto de brillo para plataformas eléctricas
                if random.random() > 0.7:
                    self.add_glow_effect(tile_x, y)
                
                self.tiles.append(tile)
                self.platform_tiles.append(tile)
                
                if y == 100 and i == width // 2:
                    self.final_platform = tile
        
        # Nubes decorativas (no colisionables)
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH - self.tile_size)
            y = random.randint(50, SCREEN_HEIGHT - 200)
            
            if random.random() > 0.3:  # 70% de probabilidad
                variant = random.choice([8, 9, 10])
                tile = TerrainTile(x, y, 'blue', variant=variant, tile_size=self.tile_size)
                tile.collidable = False
                self.tiles.append(tile)
    
    def create_default_level(self):
        """Crea nivel por defecto"""
        print("[TerrainManager] Creando nivel por defecto...")
        
        # Suelo simple
        for x in range(0, SCREEN_WIDTH + self.tile_size, self.tile_size):
            y = SCREEN_HEIGHT - self.tile_size
            tile = TerrainTile(x, y, 'terrain', variant=0, tile_size=self.tile_size)
            self.tiles.append(tile)
            self.platform_tiles.append(tile)
        
        # Algunas plataformas básicas
        for i in range(5):
            x = 200 + (i * 150)
            y = 500 - (i * 80)
            width = 3
            
            for j in range(width):
                tile_x = x + (j * self.tile_size)
                variant = j if j < 2 else 2
                tile = TerrainTile(tile_x, y, 'blue', variant=variant, tile_size=self.tile_size)
                self.tiles.append(tile)
                self.platform_tiles.append(tile)
                
                if i == 4 and j == 1:
                    self.final_platform = tile
    
    def add_glow_effect(self, x, y):
        """Añade efecto de brillo a una plataforma"""
        # Esta función la puedes expandir para efectos visuales
        pass
    
    def check_collision_at(self, x, y):
        """Verifica si hay colisión en una posición"""
        test_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
        
        for tile in self.tiles:
            if tile.collidable and tile.get_rect().colliderect(test_rect):
                return True
        return False
    
    def get_platforms(self):
        """Retorna lista de tiles que funcionan como plataformas"""
        return self.platform_tiles
    
    def get_final_platform(self):
        """Retorna la plataforma final del nivel"""
        return self.final_platform
    
    def draw(self, surface, camera_y=0):
        """Dibuja todos los tiles del terreno"""
        for tile in self.tiles:
            tile.draw(surface, camera_y)
    
    def draw_background(self, surface, camera_y=0):
        """Dibuja fondo según el nivel"""
        # Gradiente de fondo según nivel
        for y in range(SCREEN_HEIGHT):
            screen_y = y
            
            if self.level_number == 1:  # Bosque
                # Gradiente verde
                r = int(lerp(100, 34, y/SCREEN_HEIGHT))
                g = int(lerp(180, 139, y/SCREEN_HEIGHT))
                b = int(lerp(100, 34, y/SCREEN_HEIGHT))
            elif self.level_number == 2:  # Caverna
                # Gradiente gris oscuro
                r = int(lerp(30, 10, y/SCREEN_HEIGHT))
                g = int(lerp(30, 10, y/SCREEN_HEIGHT))
                b = int(lerp(40, 20, y/SCREEN_HEIGHT))
            else:  # Tormenta
                # Gradiente azul tormentoso
                r = int(lerp(80, 40, y/SCREEN_HEIGHT))
                g = int(lerp(100, 60, y/SCREEN_HEIGHT))
                b = int(lerp(150, 100, y/SCREEN_HEIGHT))
            
            pygame.draw.line(surface, (r, g, b), (0, screen_y), (SCREEN_WIDTH, screen_y))
        
        # Estrellas/nubes de fondo
        if self.level_number == 3:
            self.draw_stars(surface, camera_y)
    
    def draw_stars(self, surface, camera_y):
        """Dibuja estrellas/nubes de fondo para nivel de tormenta"""
        # Crear algunas estrellas fijas
        stars = [
            (100, 50), (300, 80), (500, 120), (700, 90), (900, 60),
            (150, 200), (400, 180), (650, 220), (850, 190), (250, 150)
        ]
        
        for x, y in stars:
            screen_y = y - camera_y * 0.3  # Paralaje lento
            
            if 0 < screen_y < SCREEN_HEIGHT:
                # Brillo pulsante
                pulse = (pygame.time.get_ticks() % 2000) / 2000
                alpha = int(100 + 50 * abs(pygame.math.Vector2(pulse - 0.5).length()))
                
                star_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
                pygame.draw.circle(star_surf, (255, 255, 255, alpha), (2, 2), 2)
                surface.blit(star_surf, (x, screen_y))