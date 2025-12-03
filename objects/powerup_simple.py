"""
powerup_simple.py - Power-ups CON SPRITES DE KIWI
Versión simplificada pero funcional con todos los efectos
"""

import pygame
import math
import random
import os
from objects.constants import *

# ============================================
# SPRITE SHEET SIMPLIFICADO
# ============================================
class SpriteSheet:
    def __init__(self, image_path, sprite_width=32, sprite_height=32):
        """Clase simple para manejar sprite sheets"""
        self.sprite_sheet = None
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        
        # Intentar cargar la imagen
        try:
            # Rutas posibles
            paths_to_try = [
                image_path,
                f"../{image_path}",
                f"./{image_path}",
                f"Assets/Collectables/{os.path.basename(image_path)}",
                f"../Assets/Collectables/{os.path.basename(image_path)}"
            ]
            
            for path in paths_to_try:
                try:
                    if os.path.exists(path):
                        self.sprite_sheet = pygame.image.load(path).convert_alpha()
                        print(f"[SpriteSheet] Cargado: {path}")
                        break
                except:
                    continue
            
            # Si no se cargó, crear fallback
            if self.sprite_sheet is None:
                print(f"[SpriteSheet] No se pudo cargar: {image_path}")
                self.sprite_sheet = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                pygame.draw.circle(self.sprite_sheet, (0, 200, 0), 
                                 (sprite_width//2, sprite_height//2), 
                                 sprite_width//2 - 2)
        except Exception as e:
            print(f"[SpriteSheet] Error: {e}")
            # Crear superficie simple
            self.sprite_sheet = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            pygame.draw.circle(self.sprite_sheet, (0, 200, 0), 
                             (sprite_width//2, sprite_height//2), 
                             sprite_width//2 - 2)
    
    def get_frame(self, frame_index, frame_y=0, width=None, height=None):
        """Obtiene un frame específico"""
        width = width or self.sprite_width
        height = height or self.sprite_height
        frame_x = frame_index * self.sprite_width
        
        # Verificar límites
        if frame_x >= self.sprite_sheet.get_width():
            frame_x = 0
        
        try:
            rect = pygame.Rect(frame_x, frame_y, width, height)
            return self.sprite_sheet.subsurface(rect).copy()
        except:
            # Fallback
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.circle(surf, (0, 200, 0), 
                             (width//2, height//2), 
                             width//2 - 2)
            return surf

# ============================================
# POWER-UP CON KIWI COMPLETO
# ============================================
class PowerUp:
    """
    Clase que representa un power-up CON KIWI ANIMADO.
    Versión simplificada pero con todos los efectos.
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
        
        print(f"[PowerUp] Kiwi {powerup_type} creado en ({x}, {y})")
        
        # ============================================
        # 🎨 CARGAR/CREAR SPRITES DE KIWI
        # ============================================
        self.kiwi_frames = []
        self.collect_frames = []
        self._load_or_create_sprites()
        
        # Animación
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.animation_time = random.uniform(0, math.pi * 2)
        
        # ============================================
        # 🌊 ANIMACIÓN FLOTANTE
        # ============================================
        self.float_time = random.uniform(0, math.pi * 2)
        self.float_amplitude = 10
        self.float_speed = 1.2
        
        # Rotación
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(0.3, 0.8)
        
        # ============================================
        # 🎯 COLORES Y SÍMBOLOS
        # ============================================
        self.colors = {
            'shield': (34, 139, 34),      # Verde kiwi
            'speed': (255, 140, 0),       # Naranja
            'zoom': (152, 251, 152),      # Verde claro
            'combo': (255, 69, 0),        # Rojo naranja
            'time_slow': (138, 43, 226),  # Violeta
            'magnet': (255, 215, 0),      # Dorado
            'double_jump': (30, 144, 255) # Azul
        }
        
        self.symbols = {
            'shield': '🛡️',
            'speed': '⚡',
            'zoom': '🔍',
            'combo': '🎯',
            'time_slow': '⏳',
            'magnet': '🧲',
            'double_jump': '🪽'
        }
        
        # ============================================
        # ✨ EFECTOS VISUALES
        # ============================================
        self.glow_size = self.size * 1.5
        self.glow_alpha = 100
        self.sparkle_particles = []
        self.last_positions = []
        
        # Partículas iniciales
        for _ in range(6):
            self._create_sparkle()
    
    def _load_or_create_sprites(self):
        """Carga sprites o crea fallbacks"""
        # Intentar cargar kiwi.png
        try:
            kiwi_sheet = SpriteSheet("Assets/Collectables/kiwi.png", 32, 32)
            
            # Cargar frames de idle
            max_frames = min(6, kiwi_sheet.sprite_sheet.get_width() // 32)
            for i in range(max_frames):
                frame = kiwi_sheet.get_frame(i)
                scaled = pygame.transform.scale(frame, 
                    (int(self.size * 1.5), int(self.size * 1.5)))
                self.kiwi_frames.append(scaled)
            
            print(f"[PowerUp] {len(self.kiwi_frames)} frames de kiwi cargados")
            
            # Intentar cargar animación de colección
            try:
                collect_sheet = SpriteSheet("Assets/Collectables/collected.png", 32, 32)
                max_collect = min(4, collect_sheet.sprite_sheet.get_width() // 32)
                for i in range(max_collect):
                    frame = collect_sheet.get_frame(i)
                    scaled = pygame.transform.scale(frame,
                        (int(self.size * 1.5), int(self.size * 1.5)))
                    self.collect_frames.append(scaled)
                print(f"[PowerUp] {len(self.collect_frames)} frames de colección cargados")
            except:
                print(f"[PowerUp] No se pudieron cargar frames de colección")
                self._create_collect_fallback()
                
        except Exception as e:
            print(f"[PowerUp] Error cargando sprites: {e}")
            self._create_kiwi_fallback()
            self._create_collect_fallback()
        
        # Asegurar que tenemos al menos 1 frame
        if not self.kiwi_frames:
            self._create_kiwi_fallback()
        if not self.collect_frames:
            self._create_collect_fallback()
        
        self.collect_frame_index = 0
        self.collect_animation_speed = 12
    
    def _create_kiwi_fallback(self):
        """Crea kiwi simple animado"""
        print("[PowerUp] Creando kiwi fallback")
        for i in range(4):
            surf = pygame.Surface((int(self.size * 1.5), int(self.size * 1.5)), pygame.SRCALPHA)
            color = self.colors.get(self.type, (34, 139, 34))
            
            # Cuerpo del kiwi
            offset = math.sin(i * 0.5) * 2
            pygame.draw.ellipse(surf, color, 
                               (self.size*0.1 + offset, self.size*0.1, 
                                self.size*1.3, self.size*1.3))
            
            # Centro marrón
            pygame.draw.ellipse(surf, (139, 69, 19), 
                               (self.size*0.4, self.size*0.4, 
                                self.size*0.7, self.size*0.7))
            
            # Semillas
            seed_color = (255, 255, 200)
            for seed in [(self.size*0.6, self.size*0.5), 
                        (self.size*0.7, self.size*0.7),
                        (self.size*0.5, self.size*0.8)]:
                pygame.draw.circle(surf, seed_color, 
                                 (int(seed[0]), int(seed[1])), 
                                 int(self.size * 0.08))
            
            self.kiwi_frames.append(surf)
    
    def _create_collect_fallback(self):
        """Crea animación de colección simple"""
        print("[PowerUp] Creando colección fallback")
        for i in range(4):
            surf = pygame.Surface((int(self.size * 1.5), int(self.size * 1.5)), pygame.SRCALPHA)
            color = self.colors.get(self.type, (34, 139, 34))
            
            # Kiwi que se desvanece
            alpha = 255 - (i * 60)
            pygame.draw.ellipse(surf, (*color[:3], alpha),
                               (self.size*0.1, self.size*0.1, 
                                self.size*1.3, self.size*1.3))
            
            # Centro
            pygame.draw.ellipse(surf, (139, 69, 19, alpha),
                               (self.size*0.4, self.size*0.4, 
                                self.size*0.7, self.size*0.7))
            
            self.collect_frames.append(surf)
    
    def _create_sparkle(self):
        """Crea partícula de chispa"""
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(self.size * 0.4, self.size * 1.0)
        color = self.colors.get(self.type, (34, 139, 34))
        
        self.sparkle_particles.append({
            'x': self.x + math.cos(angle) * distance,
            'y': self.y + math.sin(angle) * distance,
            'vx': math.cos(angle + math.pi) * random.uniform(0.2, 0.8),
            'vy': math.sin(angle + math.pi) * random.uniform(0.2, 0.8),
            'life': random.uniform(0.3, 0.8),
            'max_life': 0.8,
            'size': random.uniform(1, 2.5),
            'color': color
        })
    
    def update(self, dt):
        """Actualiza el power-up"""
        if self.collected:
            return
        
        # ============================================
        # ANIMACIÓN DEL KIWI
        # ============================================
        self.animation_time += dt * self.animation_speed
        self.animation_frame = int(self.animation_time * 8) % len(self.kiwi_frames)
        
        # ============================================
        # 🌊 MOVIMIENTO FLOTANTE
        # ============================================
        self.float_time += dt * self.float_speed
        self.y = self.start_y + math.sin(self.float_time) * self.float_amplitude
        self.x += math.sin(self.float_time * 0.7) * 0.5
        
        # ============================================
        # 🔄 ROTACIÓN
        # ============================================
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360
        
        # ============================================
        # ✨ GLOW PULSANTE
        # ============================================
        self.glow_size = self.size * (1.3 + 0.2 * math.sin(self.float_time * 2))
        self.glow_alpha = 80 + int(70 * abs(math.sin(self.float_time * 1.5)))
        
        # ============================================
        # 🎆 PARTÍCULAS
        # ============================================
        if random.random() < 0.2:
            self._create_sparkle()
        
        # Actualizar partículas
        for p in self.sparkle_particles[:]:
            p['life'] -= dt
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.05
            
            if p['life'] <= 0:
                self.sparkle_particles.remove(p)
        
        # ============================================
        # 💥 ANIMACIÓN DE RECOLECCIÓN
        # ============================================
        if self.collect_animation:
            self.collect_time += dt * self.collect_animation_speed
            self.collect_frame_index = min(int(self.collect_time), len(self.collect_frames) - 1)
            
            if self.collect_time >= len(self.collect_frames):
                self.collected = True
                # Crear explosión final
                self._create_explosion()
    
    def _create_explosion(self):
        """Crea explosión de partículas al recolectar"""
        color = self.colors.get(self.type, (34, 139, 34))
        for _ in range(15):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 5)
            
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
    
    def draw(self, surface, camera_offset):
        """Dibuja el power-up"""
        screen_y = self.y - camera_offset
        
        # No dibujar si está fuera de pantalla
        if screen_y < -100 or screen_y > SCREEN_HEIGHT + 100 or self.collected:
            return
        
        color = self.colors.get(self.type, (34, 139, 34))
        
        # ============================================
        # 🌟 GLOW EXTERIOR
        # ============================================
        if not self.collect_animation:
            glow_surf = pygame.Surface((int(self.glow_size*2), int(self.glow_size*2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*color[:3], self.glow_alpha//2),
                              (int(self.glow_size), int(self.glow_size)),
                              int(self.glow_size))
            surface.blit(glow_surf, 
                        (int(self.x - self.glow_size), int(screen_y - self.glow_size)))
        
        # ============================================
        # 🎆 PARTÍCULAS DE CHISPA
        # ============================================
        for p in self.sparkle_particles:
            particle_screen_y = p['y'] - camera_offset
            if -20 < particle_screen_y < SCREEN_HEIGHT + 20:
                alpha = int(255 * (p['life'] / p['max_life']))
                if alpha > 0:
                    pygame.draw.circle(surface, (*p['color'][:3], alpha),
                                     (int(p['x']), int(particle_screen_y)), 
                                     int(p['size']))
        
        # ============================================
        # DIBUJAR KIWI
        # ============================================
        if not self.collect_animation:
            # KIWI NORMAL
            if self.kiwi_frames and self.animation_frame < len(self.kiwi_frames):
                frame = self.kiwi_frames[self.animation_frame]
                
                # Rotación suave
                rotated_frame = pygame.transform.rotate(frame, self.rotation * 0.2)
                frame_rect = rotated_frame.get_rect(center=(self.x, screen_y))
                
                surface.blit(rotated_frame, frame_rect)
                
                # Símbolo
                symbol = self.symbols.get(self.type, '?')
                try:
                    font = pygame.font.Font(None, int(self.size * 0.8))
                    symbol_surf = font.render(symbol, True, WHITE)
                    symbol_rect = symbol_surf.get_rect(center=(self.x, screen_y))
                    surface.blit(symbol_surf, symbol_rect)
                except:
                    # Fallback para el símbolo
                    pygame.draw.circle(surface, WHITE, 
                                     (int(self.x), int(screen_y)), 
                                     self.size//4)
        else:
            # ANIMACIÓN DE RECOLECCIÓN
            if self.collect_frames and self.collect_frame_index < len(self.collect_frames):
                frame = self.collect_frames[self.collect_frame_index]
                frame_rect = frame.get_rect(center=(self.x, screen_y))
                surface.blit(frame, frame_rect)
        
        # ============================================
        # 💎 BORDE BRILLANTE
        # ============================================
        if not self.collect_animation:
            border_radius = int(self.size * 1.2)
            pygame.draw.circle(surface, (*color[:3], 180), 
                              (int(self.x), int(screen_y)), 
                              border_radius, 2)
            
            pygame.draw.circle(surface, WHITE, 
                              (int(self.x), int(screen_y)), 
                              border_radius + 2, 1)
        
        # ============================================
        # 📝 NOMBRE DEL TIPO (opcional)
        # ============================================
        if not self.collect_animation and 50 < screen_y < SCREEN_HEIGHT - 50:
            type_names = {
                'shield': 'KIWI ESCUDO',
                'speed': 'KIWI VELOCIDAD',
                'zoom': 'KIWI ZOOM',
                'combo': 'KIWI COMBO',
                'time_slow': 'KIWI TIEMPO',
                'magnet': 'KIWI IMÁN',
                'double_jump': 'KIWI SALTO'
            }
            
            type_name = type_names.get(self.type, f"KIWI {self.type.upper()}")
            font = pygame.font.Font(None, 16)
            text_surf = font.render(type_name, True, WHITE)
            text_rect = text_surf.get_rect(center=(self.x, screen_y + self.size + 12))
            
            # Fondo semitransparente
            bg = pygame.Surface((text_rect.width + 8, text_rect.height + 4), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 120))
            bg_rect = bg.get_rect(center=(self.x, screen_y + self.size + 12))
            surface.blit(bg, bg_rect)
            
            surface.blit(text_surf, text_rect)
    
    def get_rect(self):
        """Retorna rectángulo de colisión"""
        rect_size = int(self.size * 1.2)
        return pygame.Rect(self.x - rect_size//2, self.y - rect_size//2,
                          rect_size, rect_size)
    
    def collect(self):
        """Marca como recolectado"""
        if not self.collected and not self.collect_animation:
            self.collect_animation = True
            self.collect_time = 0
            self.collect_frame_index = 0
            print(f"[PowerUp] ¡KIWI {self.type.upper()} RECOGIDO!")
            return True
        return False
    
    def is_available(self):
        """Verifica si está disponible"""
        return not self.collected and not self.collect_animation

# ============================================
# 🎆 COLECTION EFFECT SIMPLIFICADO
# ============================================
class CollectionEffect:
    """Efecto de colección simplificado"""
    
    def __init__(self, x, y, color, powerup_type='shield'):
        self.x = x
        self.y = y
        self.color = color
        self.powerup_type = powerup_type
        self.lifetime = 0.8
        self.time = 0
        self.active = True
        self.particles = []
        
        # Crear partículas
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.4, self.lifetime),
                'max_life': self.lifetime,
                'size': random.uniform(2, 5),
                'color': color
            })
        
        print(f"[CollectionEffect] Efecto creado para {powerup_type}")
    
    def update(self, dt):
        """Actualiza el efecto"""
        self.time += dt
        
        # Actualizar partículas
        for p in self.particles:
            p['life'] -= dt
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.15
        
        # Desactivar
        if self.time > self.lifetime:
            self.active = False
    
    def draw(self, surface, camera_offset):
        """Dibuja el efecto"""
        if not self.active:
            return
        
        screen_y = self.y - camera_offset
        
        # Texto "¡KIWI!"
        if self.time < self.lifetime * 0.4:
            text_y = screen_y - 30 - (self.time * 80)
            text_alpha = int(255 * (1 - self.time / (self.lifetime * 0.4)))
            
            font = pygame.font.Font(None, 32)
            text_surf = font.render("¡KIWI!", True, (*self.color[:3], text_alpha))
            text_rect = text_surf.get_rect(center=(self.x, int(text_y)))
            surface.blit(text_surf, text_rect)
        
        # Partículas
        for p in self.particles:
            if p['life'] > 0:
                particle_screen_y = p['y'] - camera_offset
                if -30 < particle_screen_y < SCREEN_HEIGHT + 30:
                    alpha = int(255 * (p['life'] / p['max_life']))
                    if alpha > 0:
                        # Dibujar partícula como círculo o kiwi pequeño
                        size = max(1, int(p['size'] * (p['life'] / p['max_life'])))
                        
                        # 50% de chance de ser kiwi pequeño
                        if random.random() > 0.5:
                            pygame.draw.circle(surface, (*self.color[:3], alpha),
                                             (int(p['x']), int(particle_screen_y)), size)
                        else:
                            # Mini kiwi
                            pygame.draw.ellipse(surface, (*self.color[:3], alpha),
                                              (p['x'] - size, particle_screen_y - size//2,
                                               size*2, size))