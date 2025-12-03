"""
powerup_fixed.py - Power-ups VISIBLES con fallback robusto
"""

import pygame
import math
import random
import os
from objects.constants import *
from objects.utils import sine_wave

class PowerUp:
    """
    Clase que representa un power-up VISIBLE siempre.
    """
    
    def __init__(self, x, y, powerup_type='shield'):
        self.x = x
        self.y = y
        self.start_y = y
        self.type = powerup_type
        self.size = POWERUP_SIZE
        self.collected = False
        self.collect_animation = False
        self.collect_time = 0
        
        # ANIMACIÓN FLOTANTE
        self.float_time = random.uniform(0, math.pi * 2)
        self.float_amplitude = 12
        self.float_speed = 1.5
        
        # ROTACIÓN
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(0.5, 1.0)
        
        # COLORES POR TIPO
        self.colors = {
            'shield': (34, 139, 34),      # Verde bosque
            'speed': (255, 140, 0),       # Naranja
            'zoom': (152, 251, 152),      # Verde claro
            'combo': (255, 69, 0),        # Rojo naranja
            'time_slow': (138, 43, 226),  # Violeta
            'magnet': (255, 215, 0),      # Dorado
            'double_jump': (30, 144, 255) # Azul
        }
        
        # SÍMBOLOS
        self.symbols = {
            'shield': '🛡️',
            'speed': '⚡',
            'zoom': '🔍',
            'combo': '🎯',
            'time_slow': '⏳',
            'magnet': '🧲',
            'double_jump': '🪽'
        }
        
        # EFECTOS
        self.glow_size = 0
        self.glow_alpha = 150
        self.sparkle_particles = []
        
        # Crear partículas iniciales
        for _ in range(5):
            self.create_sparkle()
        
        print(f"[PowerUp] {powerup_type} creado en ({x}, {y})")

    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        rect_size = int(self.size * 1.2)
        return pygame.Rect(self.x - rect_size//2, self.y - rect_size//2,
                          rect_size, rect_size)
    
    def update(self, dt):
        """Actualiza la animación del power-up"""
        # Animación flotante
        self.float_time += dt * self.float_speed
        float_y = sine_wave(self.float_time, self.float_amplitude, 1)
        self.y = self.start_y + float_y
        
        # Rotación
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360
        
        # Glow pulsante
        self.glow_size = self.size * (0.7 + 0.3 * math.sin(self.float_time * 3))
        self.glow_alpha = 100 + int(100 * abs(math.sin(self.float_time * 2)))
        
        # Actualizar partículas
        for p in self.sparkle_particles[:]:
            p['life'] -= dt
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.1
            
            if p['life'] <= 0:
                self.sparkle_particles.remove(p)
        
        # Nueva partícula ocasional
        if not self.collected and random.random() < 0.2:
            self.create_sparkle()
        
        # Animación de colección
        if self.collect_animation:
            self.collect_time += dt * 15
            if self.collect_time >= 6:
                self.collected = True
    
    def draw(self, surface, camera_offset):
        """Dibuja el power-up siempre visible"""
        screen_y = self.y - camera_offset
        
        # No dibujar si está fuera de pantalla o recolectado
        if screen_y < -100 or screen_y > SCREEN_HEIGHT + 100 or self.collected:
            return
        
        color = self.colors.get(self.type, (34, 139, 34))
        
        # GLOW
        glow_surf = pygame.Surface((int(self.glow_size*2), int(self.glow_size*2)), 
                                  pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color[:3], self.glow_alpha),
                          (int(self.glow_size), int(self.glow_size)),
                          int(self.glow_size))
        surface.blit(glow_surf, 
                   (int(self.x - self.glow_size), int(screen_y - self.glow_size)))
        
        # CUERPO PRINCIPAL (SIEMPRE VISIBLE)
        if not self.collect_animation:
            # Dibujar círculo base
            pygame.draw.circle(surface, color, 
                             (int(self.x), int(screen_y)), 
                             int(self.size))
            
            # Borde blanco
            pygame.draw.circle(surface, WHITE, 
                             (int(self.x), int(screen_y)), 
                             int(self.size), 2)
            
            # Símbolo
            symbol = self.symbols.get(self.type, '?')
            font = pygame.font.Font(None, int(self.size))
            symbol_surf = font.render(symbol, True, WHITE)
            symbol_rect = symbol_surf.get_rect(center=(self.x, screen_y))
            surface.blit(symbol_surf, symbol_rect)
        else:
            # Animación de recolección (se desvanece y crece)
            alpha = max(0, 255 - int(self.collect_time * 40))
            size = self.size * (1 + self.collect_time * 0.2)
            
            fade_surf = pygame.Surface((int(size*2), int(size*2)), pygame.SRCALPHA)
            pygame.draw.circle(fade_surf, (*color[:3], alpha),
                             (int(size), int(size)), int(size))
            surface.blit(fade_surf, 
                       (int(self.x - size), int(screen_y - size)))
        
        # PARTÍCULAS
        for p in self.sparkle_particles:
            particle_screen_y = p['y'] - camera_offset
            
            if -20 < particle_screen_y < SCREEN_HEIGHT + 20:
                alpha = int(255 * (p['life'] / p['max_life']))
                if alpha > 0:
                    sparkle_surf = pygame.Surface((int(p['size']*2), int(p['size']*2)), 
                                                 pygame.SRCALPHA)
                    pygame.draw.circle(sparkle_surf, (*p['color'][:3], alpha),
                                     (int(p['size']), int(p['size'])), int(p['size']))
                    surface.blit(sparkle_surf, 
                               (int(p['x'] - p['size']), int(particle_screen_y - p['size'])))
        
        # TEXTO DEL TIPO
        if screen_y > 50 and screen_y < SCREEN_HEIGHT - 50 and not self.collect_animation:
            type_names = {
                'shield': 'ESCUDO',
                'speed': 'VELOCIDAD',
                'zoom': 'ZOOM',
                'combo': 'COMBO',
                'time_slow': 'TIEMPO',
                'magnet': 'IMÁN',
                'double_jump': 'SALTO X2'
            }
            
            type_name = type_names.get(self.type, self.type.upper())
            font = pygame.font.Font(None, 16)
            
            # Fondo
            text_bg = pygame.Surface((font.size(type_name)[0] + 8, 20), pygame.SRCALPHA)
            text_bg.fill((0, 0, 0, 150))
            text_bg_rect = text_bg.get_rect(center=(self.x, screen_y + self.size + 15))
            surface.blit(text_bg, text_bg_rect)
            
            # Texto
            text_surf = font.render(type_name, True, WHITE)
            text_rect = text_surf.get_rect(center=(self.x, screen_y + self.size + 15))
            surface.blit(text_surf, text_rect)
    
    def create_sparkle(self):
        """Crea partículas de chispa"""
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(self.size * 0.5, self.size * 1.2)
        
        self.sparkle_particles.append({
            'x': self.x + math.cos(angle) * distance,
            'y': self.y + math.sin(angle) * distance,
            'vx': math.cos(angle + math.pi) * random.uniform(0.3, 1.0),
            'vy': math.sin(angle + math.pi) * random.uniform(0.3, 1.0),
            'life': random.uniform(0.5, 1.0),
            'max_life': 1.0,
            'size': random.uniform(1, 2),
            'color': self.colors.get(self.type, (34, 139, 34))
        })
    
    def collect(self):
        """Marca el power-up como recolectado"""
        if not self.collected and not self.collect_animation:
            self.collect_animation = True
            self.collect_time = 0
            
            # Crear explosión de partículas
            color = self.colors.get(self.type, (34, 139, 34))
            for _ in range(15):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(2, 6)
                
                self.sparkle_particles.append({
                    'x': self.x,
                    'y': self.y,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'life': random.uniform(0.5, 1.0),
                    'max_life': 1.0,
                    'size': random.uniform(2, 4),
                    'color': color
                })
            
            print(f"[PowerUp] ¡{self.type.upper()} recogido!")
            return True
        return False


class CollectionEffect:
    """Efecto cuando se recoge un power-up"""
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = 0.8
        self.time = 0
        self.active = True
        self.particles = []
        
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.4, self.lifetime),
                'max_life': self.lifetime,
                'size': random.uniform(2, 4)
            })
    
    def update(self, dt):
        self.time += dt
        for p in self.particles:
            p['life'] -= dt
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.2
        
        if self.time > self.lifetime:
            self.active = False
    
    def draw(self, surface, camera_offset):
        screen_y = self.y - camera_offset
        
        for p in self.particles:
            if p['life'] > 0:
                particle_screen_y = p['y'] - camera_offset
                alpha = int(255 * (p['life'] / p['max_life']))
                
                if alpha > 0:
                    pygame.draw.circle(surface, (*self.color[:3], alpha),
                                     (int(p['x']), int(particle_screen_y)),
                                     int(p['size']))