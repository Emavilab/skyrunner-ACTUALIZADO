"""
flags.py - Sistema de banderas de victoria
"""

import pygame
from objects.constants import *

class VictoryFlag:
    """Bandera de victoria estilo Mario"""
    
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.base_y = y  # Guardar posición original
        self.level = level
        self.height = 150  # Altura del asta
        self.width = 10    # Ancho del asta
        self.flag_raised = False
        self.flag_y = y    # Posición actual de la bandera
        self.raising_speed = 200  # píxeles por segundo
        self.animation_progress = 0  # 0 a 1
        
        # Efectos visuales
        self.particles = []
        self.sparkle_timer = 0
    
    def raise_flag(self):
        """Inicia la animación de izar la bandera"""
        if not self.flag_raised:
            self.flag_raised = True
            self.animation_progress = 0
            return True
        return False
    
    def update(self, dt):
        """Actualiza la animación de la bandera"""
        if self.flag_raised and self.animation_progress < 1.0:
            self.animation_progress += dt * (self.raising_speed / self.height)
            self.animation_progress = min(self.animation_progress, 1.0)
            
            # Calcular nueva posición Y
            target_y = self.base_y - self.height + 30
            self.flag_y = self.base_y - (self.base_y - target_y) * self.animation_progress
            
            # Partículas al izar
            if random.random() < 0.3:
                self.create_sparkle()
        
        # Actualizar partículas
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt * 60
            p['y'] += p['vy'] * dt * 60
            p['life'] -= dt
            
            if p['life'] <= 0:
                self.particles.remove(p)
        
        # Temporizador de brillo
        self.sparkle_timer += dt
    
    def create_sparkle(self):
        """Crea partículas de brillo"""
        for _ in range(3):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(20, 50)
            
            self.particles.append({
                'x': self.x + self.width + 25,
                'y': self.flag_y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.5, 1.0),
                'size': random.randint(2, 5),
                'color': YELLOW
            })
    
    def draw(self, surface, camera_offset):
        """Dibuja la bandera completa"""
        screen_x = self.x
        screen_base_y = self.base_y - camera_offset
        screen_flag_y = self.flag_y - camera_offset
        
        # --- ASTA DE LA BANDERA ---
        # Sombra
        pygame.draw.rect(surface, (50, 50, 50),
                        (screen_x + 2, screen_base_y - self.height + 2,
                         self.width, self.height))
        
        # Asta principal (mástil)
        pole_rect = pygame.Rect(
            screen_x,
            screen_base_y - self.height,
            self.width,
            self.height
        )
        pygame.draw.rect(surface, (100, 100, 100), pole_rect)
        
        # Detalles del mástil
        for i in range(3):
            ring_y = screen_base_y - self.height + (i * 40) + 20
            pygame.draw.rect(surface, (150, 150, 150),
                           (screen_x - 3, ring_y, self.width + 6, 5))
        
        # --- BANDERA ---
        # Color según nivel
        flag_colors = {
            1: (0, 180, 0),    # Verde bosque
            2: (180, 0, 180),  # Púrpura caverna
            3: (0, 180, 180)   # Cian tormenta
        }
        
        flag_color = flag_colors.get(self.level, YELLOW)
        
        # Bandera ondeante (triángulo)
        flag_points = [
            (screen_x + self.width, screen_flag_y),  # Punta del asta
            (screen_x + self.width + 60, screen_flag_y + 20),  # Punta exterior
            (screen_x + self.width, screen_flag_y + 40)  # Base
        ]
        
        # Dibujar bandera
        pygame.draw.polygon(surface, flag_color, flag_points)
        
        # Contorno de bandera
        pygame.draw.polygon(surface, BLACK, flag_points, 2)
        
        # Patrón en bandera (rayas o símbolo)
        if self.level == 1:
            # Rayas horizontales para bosque
            for i in range(3):
                stripe_y = screen_flag_y + 5 + (i * 10)
                pygame.draw.line(surface, (255, 255, 0),
                               (screen_x + self.width + 5, stripe_y),
                               (screen_x + self.width + 55, stripe_y), 2)
        elif self.level == 2:
            # Círculo para caverna
            pygame.draw.circle(surface, (255, 255, 0),
                             (screen_x + self.width + 30, screen_flag_y + 20),
                             15, 3)
        else:
            # Rayo para tormenta
            lightning_points = [
                (screen_x + self.width + 20, screen_flag_y + 5),
                (screen_x + self.width + 30, screen_flag_y + 15),
                (screen_x + self.width + 20, screen_flag_y + 25),
                (screen_x + self.width + 40, screen_flag_y + 35)
            ]
            pygame.draw.lines(surface, (255, 255, 0), False, lightning_points, 3)
        
        # --- PARTÍCULAS DE BRILLO ---
        for p in self.particles:
            alpha = int(255 * (p['life'] * 2))
            if alpha > 0:
                particle_surf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surf, (*p['color'], alpha),
                                 (p['size'], p['size']), p['size'])
                
                particle_x = p['x'] - camera_offset - p['size']
                particle_y = p['y'] - camera_offset - p['size']
                surface.blit(particle_surf, (int(particle_x), int(particle_y)))
        
        # --- EFECTO DE BRILLO EN BANDERA ---
        if self.sparkle_timer % 0.5 < 0.25:
            # Destello suave
            highlight_points = [
                (screen_x + self.width + 10, screen_flag_y + 5),
                (screen_x + self.width + 50, screen_flag_y + 15),
                (screen_x + self.width + 30, screen_flag_y + 35)
            ]
            
            highlight_surf = pygame.Surface((60, 40), pygame.SRCALPHA)
            pygame.draw.polygon(highlight_surf, (255, 255, 255, 100), 
                              [(p[0] - screen_x - self.width - 10, 
                                p[1] - screen_flag_y) for p in highlight_points])
            surface.blit(highlight_surf, (screen_x + self.width + 10, screen_flag_y))
    
    def get_rect(self):
        """Retorna rectángulo de colisión"""
        return pygame.Rect(
            self.x - 30,
            self.base_y - self.height - 20,
            100,  # Ancho amplio para facilitar
            self.height + 40
        )
    
    def is_fully_raised(self):
        """Verifica si la bandera está completamente izada"""
        return self.flag_raised and self.animation_progress >= 1.0


# Añadir al principio del archivo si no están
import random
import math