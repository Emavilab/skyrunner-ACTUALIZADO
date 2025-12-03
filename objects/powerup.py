"""
powerup.py - Power-ups ÉPICOS CON SPRITES DE KIWI 🥝
Mantiene todos los efectos visuales épicos, pero con kiwis animados
"""

import pygame
import math
import random
import os
from objects.constants import *
from objects.utils import sine_wave

# Añade esta clase SpriteSheet al inicio del archivo
class SpriteSheet:
    def __init__(self, image_path, sprite_width=32, sprite_height=32):
        """Clase simple para manejar sprite sheets"""
        self.sprite_sheet = None
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        
        # Buscar el archivo en diferentes rutas
        possible_paths = [
            image_path,
            f"./{image_path}",
            f"../{image_path}",
            f"./Assets/Collectables/{os.path.basename(image_path)}",
            f"../Assets/Collectables/{os.path.basename(image_path)}",
            f"./Assets/{os.path.basename(image_path)}",
            f"../Assets/{os.path.basename(image_path)}"
        ]
        
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    self.sprite_sheet = pygame.image.load(path).convert_alpha()
                    print(f"[PowerUp] Sprite cargado desde: {path}")
                    break
            except Exception as e:
                print(f"[PowerUp] Error cargando sprite {path}: {e}")
                continue
        
        if self.sprite_sheet is None:
            print(f"[PowerUp] No se pudo cargar sprite: {image_path}")
            # Crear sprite simple como fallback
            self.sprite_sheet = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            pygame.draw.circle(self.sprite_sheet, (0, 200, 0), 
                             (sprite_width//2, sprite_height//2), 
                             sprite_width//2 - 2)
    
    def get_frame(self, frame_index, frame_y=0, width=None, height=None):
        """Obtiene un frame específico del sprite sheet"""
        width = width or self.sprite_width
        height = height or self.sprite_height
        frame_x = frame_index * self.sprite_width
        
        # Verificar límites
        if frame_x >= self.sprite_sheet.get_width():
            frame_x = 0
        
        rect = pygame.Rect(frame_x, frame_y, width, height)
        try:
            return self.sprite_sheet.subsurface(rect).copy()
        except:
            # Fallback si hay error con el subsurface
            return self.create_fallback_frame(width, height)

    def create_fallback_frame(self, width, height):
        """Crea un frame simple si falla la carga"""
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(surf, (0, 200, 0), 
                         (width//2, height//2), 
                         width//2 - 2)
        return surf

class PowerUp:
    """
    Clase que representa un power-up CON EFECTOS ÉPICOS Y KIWIS ANIMADOS.
    """
    
    def __init__(self, x, y, powerup_type='shield'):
        """
        Inicializa un power-up ÉPICO CON KIWI.
        
        Args:
            x, y: Posición
            powerup_type: Tipo ('shield', 'speed', 'zoom', 'combo', 'time_slow', 'magnet')
        """
        self.x = x
        self.y = y
        self.start_y = y
        self.type = powerup_type
        self.size = POWERUP_SIZE
        self.collected = False
        self.collect_animation = False
        self.collect_time = 0
        
        # ============================================
        # CARGAR SPRITES DE KIWI
        # ============================================
        self.kiwi_frames = []
        self.collect_frames = []
        self.load_kiwi_sprites()
        
        # Si no se cargaron sprites, crear fallback
        if not self.kiwi_frames:
            self.create_fallback_sprites()
        
        # Animación del kiwi
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_time = random.uniform(0, math.pi * 2)
        
        # ============================================
        # 🎨 ANIMACIÓN FLOTANTE ÉPICA
        # ============================================
        self.float_time = random.uniform(0, math.pi * 2)  # Fase aleatoria
        self.float_amplitude = 12  # Más movimiento
        self.float_speed = 1.5  # Más rápido
        
        # Rotación con variación (menos para kiwi)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(0.5, 1.0)  # Más lento para kiwi
        
        # ============================================
        # 🎯 COLORES Y SÍMBOLOS ÉPICOS
        # ============================================
        self.colors = {
            'shield': (34, 139, 34),      # Verde bosque (kiwi shield)
            'speed': (255, 140, 0),       # Naranja kiwi speed
            'zoom': (152, 251, 152),      # Verde claro kiwi zoom
            'combo': (255, 69, 0),        # Rojo naranja kiwi combo
            'time_slow': (138, 43, 226),  # Violeta kiwi time
            'magnet': (255, 215, 0),      # Dorado kiwi magnet
            'double_jump': (30, 144, 255) # Azul kiwi jump
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
        # ✨ EFECTOS VISUALES ÉPICOS
        # ============================================
        self.glow_size = 0
        self.glow_alpha = 150
        self.sparkle_particles = []
        self.trail_particles = []
        self.last_positions = []
        
        # Generar partículas iniciales
        for _ in range(8):
            self.create_sparkle()
        
        print(f"[PowerUp] Kiwi {powerup_type} creado en ({x}, {y})")

    def load_kiwi_sprites(self):
        """Carga los sprites de kiwi animados"""
        try:
            # Intentar cargar sprite sheet de kiwi idle
            kiwi_idle_sheet = SpriteSheet("Assets/Collectables/kiwi.png", 32, 32)
            
            # Verificar si se cargó correctamente
            if kiwi_idle_sheet.sprite_sheet.get_width() > 0:
                # Intentar cargar 17 frames de idle
                max_frames = min(17, kiwi_idle_sheet.sprite_sheet.get_width() // 32)
                self.kiwi_frames = []
                
                for i in range(max_frames):
                    frame = kiwi_idle_sheet.get_frame(i)
                    # Escalar al tamaño del power-up
                    scaled_frame = pygame.transform.scale(frame, 
                        (int(self.size * 1.5), int(self.size * 1.5)))
                    self.kiwi_frames.append(scaled_frame)
                
                print(f"[PowerUp] Kiwi idle sprites cargados: {len(self.kiwi_frames)} frames")
            
            # Intentar cargar animación de recolección
            try:
                kiwi_death_sheet = SpriteSheet("Assets/Collectables/collected.png", 32, 32)
                
                if kiwi_death_sheet.sprite_sheet.get_width() > 0:
                    max_death_frames = min(6, kiwi_death_sheet.sprite_sheet.get_width() // 32)
                    self.collect_frames = []
                    
                    for i in range(max_death_frames):
                        frame = kiwi_death_sheet.get_frame(i)
                        scaled_frame = pygame.transform.scale(frame,
                            (int(self.size * 1.5), int(self.size * 1.5)))
                        self.collect_frames.append(scaled_frame)
                    
                    print(f"[PowerUp] Kiwi collect sprites cargados: {len(self.collect_frames)} frames")
            
            except Exception as e:
                print(f"[PowerUp] No se pudieron cargar sprites de colección: {e}")
                self.collect_frames = []
            
            self.collect_frame_index = 0
            self.collect_animation_speed = 15  # Frames por segundo
            
        except Exception as e:
            print(f"[PowerUp ERROR] No se pudieron cargar sprites de kiwi: {e}")
            self.kiwi_frames = []
            self.collect_frames = []
    
    def create_fallback_sprites(self):
        """Crea sprites simples si falla la carga"""
        self.kiwi_frames = []
        self.collect_frames = []
        
        # Crear kiwi simple animado (6 frames)
        for i in range(6):
            surf = pygame.Surface((int(self.size * 1.5), int(self.size * 1.5)), pygame.SRCALPHA)
            
            # Color según tipo
            base_color = self.colors.get(self.type, (34, 139, 34))
            
            # Cuerpo del kiwi (óvalo)
            pygame.draw.ellipse(surf, base_color, 
                               (self.size*0.1, self.size*0.1, 
                                self.size*1.3, self.size*1.3))
            
            # Detalles del kiwi
            pygame.draw.ellipse(surf, (139, 69, 19),  # Marrón para el centro
                               (self.size*0.4, self.size*0.4, 
                                self.size*0.7, self.size*0.7))
            
            # Semillas
            seed_color = (255, 255, 200)
            for seed in [(self.size*0.6, self.size*0.5), 
                        (self.size*0.7, self.size*0.7),
                        (self.size*0.5, self.size*0.8)]:
                pygame.draw.circle(surf, seed_color, 
                                 (int(seed[0]), int(seed[1])), 
                                 int(self.size * 0.1))
            
            self.kiwi_frames.append(surf)
        
        # Frames de colección (simples)
        for i in range(6):
            surf = pygame.Surface((int(self.size * 1.5), int(self.size * 1.5)), pygame.SRCALPHA)
            alpha = 255 - (i * 40)  # Se desvanece
            
            # Kiwi que se desvanece
            pygame.draw.ellipse(surf, (*self.colors.get(self.type, (34, 139, 34))[:3], alpha),
                               (self.size*0.1, self.size*0.1, 
                                self.size*1.3, self.size*1.3))
            
            self.collect_frames.append(surf)
        
        self.collect_frame_index = 0
        self.collect_animation_speed = 15
    
    # ============================================
    # 🎮 MÉTODOS BÁSICOS
    # ============================================
    
    def get_rect(self):
        """
        Retorna el rectángulo de colisión (ajustado para kiwi).
        """
        # Hacer el rectángulo un poco más pequeño que el sprite
        rect_size = int(self.size * 1.2)
        return pygame.Rect(self.x - rect_size//2, self.y - rect_size//2,
                          rect_size, rect_size)
    
    def update(self, dt):
        """
        Actualiza la animación del power-up CON KIWI ANIMADO.
        """
        # Guardar posición para trail
        if len(self.last_positions) > 5:
            self.last_positions.pop(0)
        self.last_positions.append((self.x, self.y))
        
        # ============================================
        # ANIMACIÓN DEL KIWI
        # ============================================
        self.animation_time += dt * self.animation_speed
        self.animation_frame = int(self.animation_time * 10) % len(self.kiwi_frames)
        
        # ============================================
        # 🌊 MOVIMIENTO FLOTANTE SINUSOIDAL
        # ============================================
        self.float_time += dt * self.float_speed
        
        # Movimiento en X e Y con fases diferentes
        float_x = sine_wave(self.float_time * 0.7, 8, 0.8)
        float_y = sine_wave(self.float_time, self.float_amplitude, 1)
        
        self.y = self.start_y + float_y
        self.x += float_x * 0.1  # Movimiento horizontal suave
        
        # ============================================
        # 🔄 ROTACIÓN SUAVE
        # ============================================
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360
        
        # ============================================
        # ✨ ANIMACIÓN DE BRILLO PULSANTE
        # ============================================
        self.glow_size = self.size * (0.7 + 0.3 * math.sin(self.float_time * 3))
        self.glow_alpha = 100 + int(100 * abs(math.sin(self.float_time * 2)))
        
        # ============================================
        # 🎆 CREAR PARTÍCULAS DE CHISPA
        # ============================================
        if not self.collected and random.random() < 0.3:
            self.create_sparkle()
        
        # Crear partículas de estela
        if not self.collected and random.random() < 0.4 and len(self.last_positions) > 2:
            self.create_trail_particle()
        
        # ============================================
        # ⚡ ACTUALIZAR PARTÍCULAS
        # ============================================
        # Chispas
        for p in self.sparkle_particles[:]:
            p['life'] -= dt
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.1  # Gravedad leve
            
            if p['life'] <= 0:
                self.sparkle_particles.remove(p)
        
        # Estela
        for p in self.trail_particles[:]:
            p['life'] -= dt
            p['size'] = max(1, p['size'] - dt * 2)
            
            if p['life'] <= 0:
                self.trail_particles.remove(p)
        
        # ============================================
        # 💥 ANIMACIÓN DE RECOLECCIÓN DE KIWI
        # ============================================
        if self.collect_animation:
            self.collect_time += dt * self.collect_animation_speed
            self.collect_frame_index = min(int(self.collect_time), len(self.collect_frames) - 1)
            
            if self.collect_time >= len(self.collect_frames):
                self.collected = True
                # Crear explosión de partículas al recolectar
                self.create_collection_explosion()
    
    # ============================================
    # 🎨 MÉTODO DE DIBUJADO CON KIWI
    # ============================================
    
    def draw(self, surface, camera_offset):
        """
        Dibuja el power-up CON SPRITE DE KIWI ANIMADO.
        """
        screen_y = self.y - camera_offset
        
        # No dibujar si está fuera de pantalla o recolectado
        if screen_y < -100 or screen_y > SCREEN_HEIGHT + 100 or self.collected:
            return
        
        color = self.colors.get(self.type, (34, 139, 34))  # Verde kiwi por defecto
        
        # ============================================
        # ✨ DIBUJAR PARTÍCULAS DE ESTELA
        # ============================================
        for p in self.trail_particles:
            particle_screen_y = p['y'] - camera_offset
            
            if -20 < particle_screen_y < SCREEN_HEIGHT + 20:
                alpha = int(255 * (p['life'] / p['max_life']))
                if alpha > 0:
                    trail_surf = pygame.Surface((int(p['size']*2), int(p['size']*2)), 
                                               pygame.SRCALPHA)
                    pygame.draw.circle(trail_surf, (*p['color'][:3], alpha),
                                     (int(p['size']), int(p['size'])), int(p['size']))
                    surface.blit(trail_surf, 
                               (int(p['x'] - p['size']), int(particle_screen_y - p['size'])))
        
        # ============================================
        # 🌟 BRILLO EXTERIOR (GLOW) COLOR KIWI
        # ============================================
        glow_color = (*color[:3], self.glow_alpha)
        glow_surf = pygame.Surface((int(self.glow_size*2), int(self.glow_size*2)), 
                                  pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, glow_color,
                          (int(self.glow_size), int(self.glow_size)),
                          int(self.glow_size))
        surface.blit(glow_surf, 
                   (int(self.x - self.glow_size), int(screen_y - self.glow_size)))
        
        # ============================================
        # DIBUJAR SPRITE DE KIWI
        # ============================================
        if not self.collect_animation:
            # KIWI NORMAL ANIMADO
            if self.kiwi_frames and self.animation_frame < len(self.kiwi_frames):
                frame = self.kiwi_frames[self.animation_frame]
                
                # Aplicar rotación suave
                rotated_frame = pygame.transform.rotate(frame, self.rotation * 0.3)
                frame_rect = rotated_frame.get_rect(center=(self.x, screen_y))
                
                surface.blit(rotated_frame, frame_rect)
                
                # Símbolo del tipo sobre el kiwi
                symbol = self.symbols.get(self.type, '❓')
                font = pygame.font.Font(None, int(self.size * 0.7))
                symbol_surf = font.render(symbol, True, WHITE)
                symbol_rect = symbol_surf.get_rect(center=(self.x, screen_y))
                surface.blit(symbol_surf, symbol_rect)
        else:
            # ANIMACIÓN DE RECOLECCIÓN
            if self.collect_frames and self.collect_frame_index < len(self.collect_frames):
                frame = self.collect_frames[self.collect_frame_index]
                frame_rect = frame.get_rect(center=(self.x, screen_y))
                surface.blit(frame, frame_rect)
        
        # ============================================
        # 💎 BORDE BRILLANTE ALREDEDOR DEL KIWI
        # ============================================
        border_radius = int(self.size * 1.1)
        pygame.draw.circle(surface, (*color[:3], 200), 
                          (int(self.x), int(screen_y)), 
                          border_radius, 3)
        
        # Borde exterior blanco
        pygame.draw.circle(surface, WHITE, 
                          (int(self.x), int(screen_y)), 
                          border_radius + 2, 1)
        
        # ============================================
        # 🎆 DIBUJAR PARTÍCULAS DE CHISPA
        # ============================================
        for p in self.sparkle_particles:
            particle_screen_y = p['y'] - camera_offset
            
            if -20 < particle_screen_y < SCREEN_HEIGHT + 20:
                alpha = int(255 * (p['life'] / p['max_life']))
                if alpha > 0:
                    sparkle_surf = pygame.Surface((int(p['size']*2), int(p['size']*2)), 
                                                 pygame.SRCALPHA)
                    
                    # Chispa brillante
                    pygame.draw.circle(sparkle_surf, (*p['color'][:3], alpha),
                                     (int(p['size']), int(p['size'])), int(p['size']))
                    
                    # Glow exterior
                    pygame.draw.circle(sparkle_surf, (*p['color'][:3], alpha//2),
                                     (int(p['size']), int(p['size'])), int(p['size']*1.5))
                    
                    surface.blit(sparkle_surf, 
                               (int(p['x'] - p['size']), int(particle_screen_y - p['size'])))
        
        # ============================================
        # 📝 TEXTO DEL TIPO CON ESTILO KIWI
        # ============================================
        if screen_y > 50 and screen_y < SCREEN_HEIGHT - 50 and not self.collect_animation:
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
            font = pygame.font.Font(None, 18)
            
            # Fondo para el texto
            text_bg = pygame.Surface((font.size(type_name)[0] + 8, 22), pygame.SRCALPHA)
            text_bg.fill((0, 0, 0, 150))
            text_bg_rect = text_bg.get_rect(center=(self.x, screen_y + self.size + 15))
            surface.blit(text_bg, text_bg_rect)
            
            # Texto
            text_surf = font.render(type_name, True, color)
            text_rect = text_surf.get_rect(center=(self.x, screen_y + self.size + 15))
            surface.blit(text_surf, text_rect)
    
    # ============================================
    # 🎨 MÉTODOS DE CREACIÓN DE PARTÍCULAS
    # ============================================
    
    def create_sparkle(self):
        """Crea partículas de chispa alrededor del kiwi"""
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(self.size * 0.5, self.size * 1.2)
        
        self.sparkle_particles.append({
            'x': self.x + math.cos(angle) * distance,
            'y': self.y + math.sin(angle) * distance,
            'vx': math.cos(angle + math.pi) * random.uniform(0.5, 1.5),
            'vy': math.sin(angle + math.pi) * random.uniform(0.5, 1.5),
            'life': random.uniform(0.5, 1.2),
            'max_life': 1.2,
            'size': random.uniform(1.5, 3),
            'color': self.colors.get(self.type, (34, 139, 34))
        })
    
    def create_trail_particle(self):
        """Crea partículas de estela"""
        if len(self.last_positions) < 2:
            return
        
        last_pos = self.last_positions[-2]
        
        self.trail_particles.append({
            'x': last_pos[0],
            'y': last_pos[1],
            'life': random.uniform(0.3, 0.6),
            'max_life': 0.6,
            'size': random.uniform(2, 4),
            'color': (*self.colors.get(self.type, (34, 139, 34))[:3], 100)
        })
    
    def create_collection_explosion(self):
        """Crea explosión de partículas al recolectar kiwi"""
        color = self.colors.get(self.type, (34, 139, 34))
        
        for _ in range(20):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 8)
            
            self.sparkle_particles.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.8, 1.5),
                'max_life': 1.5,
                'size': random.uniform(2, 5),
                'color': color
            })
    
    # ============================================
    # 🎯 MÉTODOS DE INTERACCIÓN
    # ============================================
    
    def collect(self):
        """Marca el power-up como recolectado e inicia animación de kiwi"""
        if not self.collected and not self.collect_animation:
            self.collect_animation = True
            self.collect_time = 0
            self.collect_frame_index = 0
            print(f"[PowerUp] ¡KIWI {self.type.upper()} recogido!")
            return True
        return False
    
    def is_available(self):
        """Verifica si el kiwi está disponible para recolectar"""
        return not self.collected and not self.collect_animation


# ============================================
# CLASE CollectionEffect CON KIWI
# ============================================

class CollectionEffect:
    """
    Efecto visual épico cuando se recoge un kiwi.
    """
    
    def __init__(self, x, y, color, powerup_type='shield'):
        """
        Args:
            x, y: Posición del efecto
            color: Color del kiwi
            powerup_type: Tipo de power-up
        """
        self.x = x
        self.y = y
        self.color = color
        self.powerup_type = powerup_type
        self.lifetime = 1.0  # Efecto más largo para kiwi
        self.time = 0
        self.active = True
        
        # ============================================
        # 🎆 CREAR PARTÍCULAS ÉPICAS DE KIWI
        # ============================================
        self.particles = []
        particle_count = 20
        
        for i in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            
            # Forma de semilla de kiwi
            shape = 'seed' if random.random() > 0.5 else 'slice'
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.6, self.lifetime),
                'max_life': self.lifetime,
                'size': random.uniform(3, 6),
                'color': color,
                'shape': shape,  # 'seed' o 'slice'
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(2, 5)
            })
    
    def update(self, dt):
        """Actualiza el efecto de colección de kiwi"""
        self.time += dt
        
        # Actualizar partículas
        for p in self.particles:
            p['life'] -= dt
            p['rotation'] += p['rotation_speed']
            
            # Movimiento
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.2  # Gravedad
            
            # Reducir velocidad
            p['vx'] *= 0.98
            p['vy'] *= 0.98
        
        # Desactivar cuando termine
        if self.time > self.lifetime:
            self.active = False
    
    def draw(self, surface, camera_offset):
        """Dibuja el efecto de colección de kiwi"""
        screen_y = self.y - camera_offset
        
        # Dibujar partículas
        for p in self.particles:
            if p['life'] > 0:
                particle_screen_y = p['y'] - camera_offset
                
                if -50 < particle_screen_y < SCREEN_HEIGHT + 50:
                    alpha = int(255 * (p['life'] / p['max_life']))
                    
                    if alpha > 0:
                        if p['shape'] == 'seed':
                            # Semilla de kiwi (elipse marrón)
                            seed_surf = pygame.Surface((int(p['size']*2), int(p['size'])), 
                                                      pygame.SRCALPHA)
                            pygame.draw.ellipse(seed_surf, (139, 69, 19, alpha),
                                              (0, 0, p['size']*2, p['size']))
                            
                            # Rotar
                            rotated_seed = pygame.transform.rotate(seed_surf, p['rotation'])
                            seed_rect = rotated_seed.get_rect(center=(p['x'], particle_screen_y))
                            surface.blit(rotated_seed, seed_rect)
                        
                        else:  # slice
                            # Rodaja de kiwi (semicírculo verde)
                            slice_surf = pygame.Surface((int(p['size']*2), int(p['size'])), 
                                                       pygame.SRCALPHA)
                            pygame.draw.ellipse(slice_surf, (*self.color[:3], alpha),
                                              (0, 0, p['size']*2, p['size']))
                            
                            # Centro marrón
                            pygame.draw.ellipse(slice_surf, (139, 69, 19, alpha),
                                              (p['size']*0.3, p['size']*0.3,
                                               p['size']*1.4, p['size']*0.4))
                            
                            rotated_slice = pygame.transform.rotate(slice_surf, p['rotation'])
                            slice_rect = rotated_slice.get_rect(center=(p['x'], particle_screen_y))
                            surface.blit(rotated_slice, slice_rect)
        
        # Texto "¡KIWI!" que sube
        if self.time < self.lifetime * 0.5:
            text_y = screen_y - 50 - (self.time * 100)
            text_alpha = int(255 * (1 - self.time / (self.lifetime * 0.5)))
            
            font = pygame.font.Font(None, 36)
            text_surf = font.render("¡KIWI!", True, (*self.color[:3], text_alpha))
            text_rect = text_surf.get_rect(center=(self.x, int(text_y)))
            surface.blit(text_surf, text_rect)