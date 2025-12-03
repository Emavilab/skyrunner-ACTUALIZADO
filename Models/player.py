"""
player.py - Clase Player COMPLETAMENTE FUNCIONAL
"""

import pygame
import math
from objects.constants import *
from objects.utils import lerp, clamp

# Constants
JUMP_FORCE = -15  # Fuerza de salto (valor negativo para moverse hacia arriba)
GRAVITY = 0.5  # Aceleración de la gravedad (ajusta según sea necesario)
# player.py - cerca de las otras importaciones
# Añade después de los imports:
PLAYER_LIVES = 3  # Vidas por defecto

# Clase SpriteSheet simple
class SpriteSheet:
    def __init__(self, image_path, sprite_width=32, sprite_height=32):
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
    
    def get_frame(self, frame_x, frame_y=0, width=None, height=None):
        """Extrae un frame del spritesheet"""
        width = width or self.sprite_width
        height = height or self.sprite_height
        rect = pygame.Rect(frame_x * self.sprite_width, frame_y * self.sprite_height, width, height)
        frame = self.sprite_sheet.subsurface(rect).copy()
        return frame

class Player:
    def __init__(self, x, y, difficulty_settings):
        # Posición y tamaño
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        
        # Física
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.jump_count = 0
        self.max_jumps = difficulty_settings.get("player_jumps", 1)
        self.coyote_time = difficulty_settings.get("coyote_time", 0.1)
        self.coyote_timer = 0
        
        # Atributos básicos
        self.health = PLAYER_MAX_HEALTH
        self.score = 0
        self.lives = difficulty_settings.get("player_lives", PLAYER_LIVES)
        self.alive = True
        
        # Animación
        self.state = "IDLE_RIGHT"
        self.pastState = "RUN_RIGHT"
        self.animation_speed = 0.1  # Segundos entre frames
        self.frame_timer = 0
        
        # Estados de animación
        self.idle_frame = 0
        self.run_frame = 0
        self.idle_length = 11
        self.run_length = 12
        
        # Cargar sprites
        self.load_frog_animations()
        
        # Power-ups
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost = False
        self.speed_timer = 0
        self.speed_multiplier = 1.5
        self.zoom_active = False
        self.zoom_timer = 0
        self.zoom_scale = 1.0
        
        # Combo
        self.combo = 0
        self.combo_timer = 0
        self.max_combo = 0
        self.combo_multiplier = 1.0
        
        # Estadísticas
        self.stats = {
            'platforms_touched': 0,
            'enemies_killed': 0,
            'powerups_collected': 0,
            'max_height': self.y,
            'total_jumps': 0,
            'air_time': 0
        }
        
        # Tiempo y efectos
        self.animation_time = 0
        self.game_time = 0
        
        # Invulnerabilidad
        self.invulnerable = False
        self.invuln_timer = 0
        
        # Controles
        self.jump_pressed = False
        self.last_keys = None

    def load_frog_animations(self):
        """Carga sprites de la ranita"""
        try:
            # IDLE - 11 frames
            self.idle_length = 11
            idle_sheet = SpriteSheet("./Assets/Player/player_idle.png")
            self.idle = [idle_sheet.get_frame(x) for x in range(self.idle_length)]
            
            # Escalar al tamaño del jugador
            for x in range(len(self.idle)):
                self.idle[x] = pygame.transform.scale(self.idle[x], (self.width, self.height))

            # RUN - 12 frames
            self.run_length = 12
            run_sheet = SpriteSheet("./Assets/Player/player_run.png")
            self.run = [run_sheet.get_frame(x) for x in range(self.run_length)]
            
            # Escalar al tamaño del jugador
            for x in range(len(self.run)):
                self.run[x] = pygame.transform.scale(self.run[x], (self.width, self.height))

            # JUMP / FALL
            self.player_jump = pygame.transform.scale(
                pygame.image.load("./Assets/Player/player_jump.png").convert_alpha(), 
                (self.width, self.height)
            )
            self.player_fall = pygame.transform.scale(
                pygame.image.load("./Assets/Player/player_fall.png").convert_alpha(), 
                (self.width, self.height)
            )

        except Exception as e:
            print(f"[Player] Error cargando sprites: {e}")
            self.create_default_sprites()

    def create_default_sprites(self):
        """Crea sprites simples si falla la carga"""
        # IDLE frames
        self.idle = []
        self.idle_length = 4
        for i in range(self.idle_length):
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            color = (0, 200 + i*10, 0)
            pygame.draw.circle(surf, color, (self.width//2, self.height//2), self.width//2 - 5)
            self.idle.append(surf)
        
        # RUN frames
        self.run = []
        self.run_length = 6
        for i in range(self.run_length):
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            offset = (i % 2) * 5
            pygame.draw.ellipse(surf, (0, 180, 0), 
                               (5 + offset, 5, self.width - 10, self.height - 10))
            self.run.append(surf)
        
        # JUMP/FALL frames
        self.player_jump = self.create_frog_sprite()
        self.player_fall = self.create_frog_sprite()
    
    def create_frog_sprite(self):
        """Crea sprite de ranita simple"""
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (0, 200, 0), (5, 5, self.width - 10, self.height - 10))
        pygame.draw.circle(surf, (255, 255, 255), (self.width//3, self.height//3), 4)
        pygame.draw.circle(surf, (255, 255, 255), (2*self.width//3, self.height//3), 4)
        pygame.draw.circle(surf, (0, 0, 0), (self.width//3, self.height//3), 2)
        pygame.draw.circle(surf, (0, 0, 0), (2*self.width//3, self.height//3), 2)
        return surf

    def get_rect(self):
        """Retorna rectángulo de colisión"""
        # Hitbox más pequeña que el sprite visual
        w = int(self.width * 0.7 * self.zoom_scale)
        h = int(self.height * 0.8 * self.zoom_scale)
        return pygame.Rect(self.x - w//2, self.y - h//2 + 5, w, h)
    
    def handle_input(self, keys):
        """Maneja entrada del jugador"""
        # Velocidad base - VALOR FIJO y manejable
        base_speed = 7  # Píxeles por frame (ajusta este valor según necesites)
        
        if self.speed_boost:
            base_speed *= self.speed_multiplier
        
        # Movimiento horizontal
        moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        
        if moving_left and not moving_right:
            self.vel_x = -base_speed
            self.state = "RUN_LEFT"
            self.pastState = "RUN_LEFT"
        elif moving_right and not moving_left:
            self.vel_x = base_speed
            self.state = "RUN_RIGHT"
            self.pastState = "RUN_RIGHT"
        else:
            # Frenado
            self.vel_x = lerp(self.vel_x, 0, 0.15)  # Reducido de 0.3 a 0.15 para frenado más suave
            if abs(self.vel_x) < 0.5:
                if self.pastState == "RUN_RIGHT":
                    self.state = "IDLE_RIGHT"
                elif self.pastState == "RUN_LEFT":
                    self.state = "IDLE_LEFT"
        
        # Saltos - solo en presión, no en hold
        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        
        # Solo salta cuando se PRESIONA la tecla
        if jump_pressed and not self.jump_pressed:
            can_jump = (self.on_ground or self.coyote_timer > 0 or self.jump_count < self.max_jumps)
            
            if can_jump:
                self.vel_y = JUMP_FORCE  # Valor negativo en tus constantes
                self.on_ground = False
                self.coyote_timer = 0
                self.jump_count += 1
                self.stats['total_jumps'] += 1
        
        # Guardar estado de salto
        self.jump_pressed = jump_pressed

    def update(self, dt, platforms):
        """Actualiza estado del jugador - CORREGIDO PARA NO TRASPASAR PLATAFORMAS"""
        self.game_time += dt
        self.animation_time += dt
        self.frame_timer += dt
        
        # Animaciones
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            if self.state in ["IDLE_RIGHT", "IDLE_LEFT"]:
                self.idle_frame = (self.idle_frame + 1) % self.idle_length
            elif self.state in ["RUN_RIGHT", "RUN_LEFT"]:
                speed_mod = 1.5 if self.speed_boost else 1.0
                self.run_frame = (self.run_frame + int(speed_mod)) % self.run_length
        
        # Coyote time
        if self.on_ground:
            self.coyote_timer = self.coyote_time
            self.jump_count = 0
        else:
            self.coyote_timer -= dt
        
        # Gravedad
        self.vel_y += GRAVITY
        
        # Limitar velocidad vertical
        if self.vel_y > TERMINAL_VELOCITY:
            self.vel_y = TERMINAL_VELOCITY
        
        # Movimiento horizontal con fricción en el aire (suavizado)
        air_friction = 0.95 if not self.on_ground else 1.0
        self.vel_x *= air_friction

        # Actualizar posición primero en X
        self.x += self.vel_x
        
        # Límites horizontales
        half_width = self.width // 2
        self.x = clamp(self.x, half_width, SCREEN_WIDTH - half_width)
        
        # Actualizar posición en Y
        self.y += self.vel_y
        
        # CORRECCIÓN IMPORTANTE: Colisiones con plataformas - SISTEMA MEJORADO
        self.on_ground = False
        player_rect = self.get_rect()
        
        for platform in platforms:
            plat_rect = platform.get_rect()
            
            if player_rect.colliderect(plat_rect):
                # Calcular diferencia en Y entre el jugador y la plataforma
                diff_y = player_rect.bottom - plat_rect.top
                diff_x_right = plat_rect.right - player_rect.left
                diff_x_left = player_rect.right - plat_rect.left
                
                # Si viene desde arriba y está cerca del borde superior
                if self.vel_y >= 0 and diff_y >= 0 and diff_y <= 25:  # Aumentado el rango
                    # Colisión desde arriba - parar en la plataforma
                    self.y = plat_rect.top - (player_rect.height // 2) + 5  # Ajuste fino
                    self.vel_y = 0
                    self.on_ground = True
                    self.jump_count = 0
                    
                    # Puntos por primera vez
                    if not hasattr(platform, 'touched') or not platform.touched:
                        platform.touched = True
                        self.add_points_from_platform()
                
                # Colisiones laterales - solo si no estamos sobre la plataforma
                elif not self.on_ground:
                    # Movimiento hacia la derecha
                    if self.vel_x > 0 and diff_x_right > 0 and diff_x_right < 20:
                        # Verificar si podemos pasar por encima
                        if plat_rect.top > player_rect.bottom - 10:
                            self.x = plat_rect.left - (player_rect.width // 2)
                            self.vel_x = 0
                    
                    # Movimiento hacia la izquierda
                    elif self.vel_x < 0 and diff_x_left > 0 and diff_x_left < 20:
                        if plat_rect.top > player_rect.bottom - 10:
                            self.x = plat_rect.right + (player_rect.width // 2)
                            self.vel_x = 0
        
        # Power-ups - ACTUALIZACIÓN CON TODOS LOS EFECTOS
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False
                print("[Player] Escudo desactivado")
        
        if self.speed_boost:
            self.speed_timer -= dt
            if self.speed_timer <= 0:
                self.speed_boost = False
                print("[Player] Velocidad desactivada")
        
        if self.zoom_active:
            self.zoom_timer -= dt
            if self.zoom_timer <= 0:
                self.zoom_active = False
                self.zoom_scale = lerp(self.zoom_scale, 1.0, 0.1)
                print("[Player] Zoom desactivado")
            else:
                # Efecto de pulso para el zoom
                pulse = 0.03 * math.sin(self.game_time * 10)
                self.zoom_scale = lerp(self.zoom_scale, 1.3 + pulse, 0.2)
        else:
            self.zoom_scale = lerp(self.zoom_scale, 1.0, 0.1)
        
        # Combo
        if self.combo > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo = 0
        
        # Invulnerabilidad
        if self.invulnerable:
            self.invuln_timer -= dt
            if self.invuln_timer <= 0:
                self.invulnerable = False
        
        # Estadísticas
        if self.y < self.stats['max_height']:
            self.stats['max_height'] = self.y
        
        if not self.on_ground:
            self.stats['air_time'] += dt
        
        # Muerte por caída - usar sistema de vidas
        if self.y > SCREEN_HEIGHT + 200:
            if self.alive:  # Solo si está vivo
                # Desactivar escudo si lo tiene para asegurar que muera
                if self.shield_active:
                    self.shield_active = False
                    print("[Player] Escudo desactivado por caída")
                
                # Aplicar daño fatal
                damage_to_apply = max(self.health, 1000)  # Asegurar muerte
                self.take_damage(damage_to_apply)
                print("[Player] Muerte por caída")
    
    def draw(self, surface, camera_offset=0):
        """Dibuja la ranita - CON EFECTOS COMPLETOS DE POWER-UPS"""
        screen_x = int(self.x)
        screen_y = int(self.y - camera_offset)
        
        current_width = int(self.width * self.zoom_scale)
        current_height = int(self.height * self.zoom_scale)
        draw_x = screen_x - current_width // 2
        draw_y = screen_y - current_height // 2

        sprite = None
        
        # Seleccionar sprite
        if not self.on_ground:
            if self.vel_y < 0:  # Saltando
                if self.pastState == "RUN_RIGHT":
                    sprite = self.player_jump
                else:
                    sprite = pygame.transform.flip(self.player_jump, True, False)
            else:  # Cayendo
                if self.pastState == "RUN_RIGHT":
                    sprite = self.player_fall
                else:
                    sprite = pygame.transform.flip(self.player_fall, True, False)
        elif self.state == "IDLE_RIGHT":
            sprite = self.idle[self.idle_frame % self.idle_length]
        elif self.state == "IDLE_LEFT":
            sprite = pygame.transform.flip(self.idle[self.idle_frame % self.idle_length], True, False)
        elif self.state == "RUN_RIGHT":
            sprite = self.run[self.run_frame % self.run_length]
        elif self.state == "RUN_LEFT":
            sprite = pygame.transform.flip(self.run[self.run_frame % self.run_length], True, False)
        
        # Aplicar efectos de power-ups al sprite
        if sprite:
            # Escalar según zoom
            if self.zoom_scale != 1.0:
                sprite = pygame.transform.scale(sprite, (current_width, current_height))
            
            # Efecto de velocidad (rotación y translación)
            if self.speed_boost:
                # Crear sprite con efecto de movimiento
                angle = math.sin(self.game_time * 20) * 5  # Oscilación suave
                rotated_sprite = pygame.transform.rotate(sprite, angle)
                
                # Ajustar posición después de rotación
                rot_rect = rotated_sprite.get_rect(center=(draw_x + current_width//2, draw_y + current_height//2))
                final_sprite = rotated_sprite
                final_draw_x = rot_rect.x
                final_draw_y = rot_rect.y
            else:
                final_sprite = sprite
                final_draw_x = draw_x
                final_draw_y = draw_y
            
            # Dibujar sprite
            if self.invulnerable and int(self.animation_time * 10) % 2 == 0:
                # Parpadeo cuando invulnerable
                alpha_sprite = final_sprite.copy()
                alpha_sprite.set_alpha(128)
                surface.blit(alpha_sprite, (final_draw_x, final_draw_y))
            else:
                surface.blit(final_sprite, (final_draw_x, final_draw_y))
        else:
            final_draw_x = draw_x
            final_draw_y = draw_y
        
        # Escudo - EFECTO MEJORADO
        if self.shield_active:
            shield_radius = int(max(current_width, current_height) * 0.9)
            
            # Efecto de pulso y rotación
            pulse = 1.0 + 0.15 * math.sin(self.animation_time * 12)
            shield_radius_pulsed = int(shield_radius * pulse)
            
            # Dibujar círculo exterior animado
            for i in range(3):
                offset = i * 2
                alpha = 200 - i * 50
                color = (SHIELD_COLOR[0], SHIELD_COLOR[1], SHIELD_COLOR[2], alpha)
                
                # Crear superficie para el escudo con transparencia
                shield_surf = pygame.Surface((shield_radius_pulsed*2 + 10, shield_radius_pulsed*2 + 10), pygame.SRCALPHA)
                
                # Dibujar anillos concéntricos
                pygame.draw.circle(shield_surf, color, 
                                 (shield_radius_pulsed + 5, shield_radius_pulsed + 5), 
                                 shield_radius_pulsed - offset, 3)
                
                # Rotar el escudo
                angle = self.animation_time * 100 + i * 30  # Rotación diferente para cada anillo
                rotated_shield = pygame.transform.rotate(shield_surf, angle)
                rot_rect = rotated_shield.get_rect(center=(screen_x, screen_y))
                
                surface.blit(rotated_shield, rot_rect)
            
            # Efecto interior brillante
            inner_surf = pygame.Surface((shield_radius_pulsed, shield_radius_pulsed), pygame.SRCALPHA)
            inner_color = (255, 255, 200, 30)
            pygame.draw.circle(inner_surf, inner_color, 
                             (shield_radius_pulsed//2, shield_radius_pulsed//2), 
                             shield_radius_pulsed//2 - 5)
            surface.blit(inner_surf, (screen_x - shield_radius_pulsed//2, screen_y - shield_radius_pulsed//2))
        
        # Rastro de velocidad - EFECTO MEJORADO
        if self.speed_boost and abs(self.vel_x) > 0 and sprite:
            trail_length = 5
            for i in range(trail_length):
                alpha = 150 - i * 30
                size_factor = 1.0 - i * 0.1
                
                # Posición del rastro
                trail_x = screen_x - (self.vel_x * 0.15) * (i + 1) * 2
                trail_y = screen_y
                
                # Crear sprite del rastro
                trail_width = int(current_width * size_factor)
                trail_height = int(current_height * size_factor)
                
                if self.pastState == "RUN_RIGHT":
                    trail_sprite = pygame.transform.scale(sprite, (trail_width, trail_height))
                else:
                    trail_sprite = pygame.transform.scale(pygame.transform.flip(sprite, True, False), 
                                                         (trail_width, trail_height))
                
                # Aplicar transparencia y color
                trail_sprite = trail_sprite.copy()
                color_overlay = pygame.Surface((trail_width, trail_height), pygame.SRCALPHA)
                color_overlay.fill((255, 200, 0, alpha//2))
                trail_sprite.blit(color_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                
                # Dibujar rastro
                surface.blit(trail_sprite, (trail_x - trail_width//2, trail_y - trail_height//2))
        
        # Efecto de combo - EFECTO MEJORADO
        if self.combo >= 5:
            combo_size = 30 + min(self.combo, 20) * 2
            
            # Color según nivel de combo
            if self.combo >= 15:
                combo_color = (255, 50, 255)  # Violeta brillante
                pulse_speed = 20
            elif self.combo >= 10:
                combo_color = (255, 255, 50)  # Amarillo brillante
                pulse_speed = 15
            else:
                combo_color = (50, 255, 255)  # Cyan
                pulse_speed = 10
            
            # Efecto de pulso y rotación
            pulse = 1.0 + 0.3 * math.sin(self.animation_time * pulse_speed)
            current_combo_size = int(combo_size * pulse)
            
            # Dibujar múltiples anillos
            for i in range(3):
                ring_size = current_combo_size - i * 8
                if ring_size > 0:
                    alpha = 200 - i * 60
                    ring_color = (combo_color[0], combo_color[1], combo_color[2], alpha)
                    
                    # Crear superficie para el anillo
                    ring_surf = pygame.Surface((ring_size*2, ring_size*2), pygame.SRCALPHA)
                    pygame.draw.circle(ring_surf, ring_color, 
                                     (ring_size, ring_size), ring_size, 3)
                    
                    # Rotar anillo
                    angle = self.animation_time * 50 + i * 45
                    rotated_ring = pygame.transform.rotate(ring_surf, angle)
                    rot_rect = rotated_ring.get_rect(center=(screen_x, screen_y))
                    
                    surface.blit(rotated_ring, rot_rect)
            
            # Texto de combo con efecto
            if self.combo >= 10:
                font = pygame.font.Font(None, 36)
                combo_text = f"x{self.combo}"
                if self.combo_multiplier > 1.0:
                    combo_text += f" (x{self.combo_multiplier:.1f})"
                
                # Sombra del texto
                shadow_surf = font.render(combo_text, True, (0, 0, 0))
                shadow_rect = shadow_surf.get_rect(center=(screen_x + 2, screen_y - 50 + 2))
                surface.blit(shadow_surf, shadow_rect)
                
                # Texto principal con efecto de brillo
                text_alpha = 200 + int(55 * math.sin(self.animation_time * 15))
                text_surf = font.render(combo_text, True, combo_color)
                text_surf.set_alpha(text_alpha)
                text_rect = text_surf.get_rect(center=(screen_x, screen_y - 50))
                surface.blit(text_surf, text_rect)
                
                # Efecto de partículas alrededor del texto
                if self.combo >= 15:
                    for i in range(8):
                        angle = i * 45 + self.animation_time * 100
                        radius = 40 + 10 * math.sin(self.animation_time * 8 + i)
                        particle_x = screen_x + radius * math.cos(math.radians(angle))
                        particle_y = screen_y - 50 + radius * math.sin(math.radians(angle))
                        
                        particle_size = 3 + 2 * math.sin(self.animation_time * 10 + i)
                        pygame.draw.circle(surface, combo_color, 
                                         (int(particle_x), int(particle_y)), 
                                         int(particle_size))
    
    def add_combo(self, points=1):
        """Añade al combo"""
        self.combo += points
        self.combo_timer = 3.0
        self.max_combo = max(self.max_combo, self.combo)
        return self.combo
    
    def update_combo(self, dt):
        """Actualiza el temporizador de combo"""
        if self.combo > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo = 0
    
    def get_combo_bonus(self):
        """Calcula bonus de puntos por combo"""
        if self.combo <= 1:
            return 0
        bonus = 10 * (self.combo ** 2)
        bonus *= self.combo_multiplier
        return int(bonus)
    
    def add_points_from_platform(self):
        """Añade puntos por tocar plataforma"""
        base_points = POINTS_PLATFORM
        combo_bonus = self.get_combo_bonus()
        total_points = int((base_points + combo_bonus) * self.combo_multiplier)
        
        self.score += total_points
        self.stats['platforms_touched'] += 1
        self.add_combo()
    
    def take_damage(self, damage):
        """Aplica daño al jugador"""
        if self.invulnerable:
            return False
        
        if self.shield_active:
            self.shield_active = False
            print("[Player] Escudo destruido por daño")
            return False
        
        if self.combo > 0:
            self.combo = 0
            self.combo_timer = 0
            print("[Player] Combo perdido por daño")
        
        self.health -= damage
        print(f"[Player] Daño recibido: {damage}, Salud restante: {self.health}")
        
        if self.health <= 0:
            self.health = 0
            self.lives -= 1
            print(f"[Player] Vida perdida. Vidas restantes: {self.lives}")
            
            if self.lives > 0:
                self.health = PLAYER_MAX_HEALTH
                self.invulnerable = True
                self.invuln_timer = 2.0
                
                # Respawn en una posición segura
                self.y = SCREEN_HEIGHT - 200  # Posición segura desde abajo
                self.x = SCREEN_WIDTH // 2    # Centro horizontal
                self.velocity_y = 0           # Detener caída
                
                print("[Player] Reviviendo con invulnerabilidad")
                return True
            else:
                self.alive = False
                print("[Player] Jugador eliminado")
                return True
        else:
            self.invulnerable = True
            self.invuln_timer = 1.0
            print("[Player] Invulnerabilidad activada")
            return False
    
    def activate_powerup(self, powerup_type):
        """Activa un power-up con todos los efectos"""
        print(f"[Player] Activando power-up: {powerup_type}")
        
        if powerup_type == 'shield':
            self.shield_active = True
            self.shield_timer = POWERUP_DURATION * 2.0
            print(f"[Player] Escudo activado por {self.shield_timer:.1f}s")
            
        elif powerup_type == 'speed':
            self.speed_boost = True
            self.speed_timer = POWERUP_DURATION * 1.5
            print(f"[Player] Velocidad activada por {self.speed_timer:.1f}s")
            
        elif powerup_type == 'zoom':
            self.zoom_active = True
            self.zoom_timer = POWERUP_DURATION * 1.8
            print(f"[Player] Zoom activado por {self.zoom_timer:.1f}s")
        
        # Puntos por recoger power-up
        points = POINTS_POWERUP * self.combo_multiplier
        self.score += int(points)
        self.stats['powerups_collected'] += 1
        self.add_combo()
        
        print(f"[Player] +{int(points)} puntos por power-up")
        return True
    
    def draw_hud(self, surface):
        """Dibuja la interfaz de usuario"""
        # Barra de vida
        health_width = 200
        health_height = 20
        health_x = 20
        health_y = 20
        
        # Fondo con efecto de borde
        pygame.draw.rect(surface, (50, 50, 50), (health_x-2, health_y-2, health_width+4, health_height+4))
        pygame.draw.rect(surface, (100, 100, 100), (health_x, health_y, health_width, health_height))
        
        # Barra actual con gradiente
        health_percentage = self.health / PLAYER_MAX_HEALTH
        current_health_width = int(health_width * health_percentage)
        
        # Gradiente de color
        if health_percentage > 0.5:
            health_color = (0, 255, 0)  # Verde
        elif health_percentage > 0.25:
            health_color = (255, 255, 0)  # Amarillo
        else:
            health_color = (255, 0, 0)  # Rojo
        
        # Efecto de pulso si la salud es baja
        if health_percentage < 0.3:
            pulse = 0.5 + 0.5 * math.sin(self.game_time * 10)
            health_color = (int(255 * pulse), int(255 * pulse * 0.5), 0)
        
        pygame.draw.rect(surface, health_color, (health_x, health_y, current_health_width, health_height))
        
        # Borde interno
        pygame.draw.rect(surface, (255, 255, 255), (health_x, health_y, health_width, health_height), 1)
        
        # Texto
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"HP: {int(self.health)}/{PLAYER_MAX_HEALTH}", True, (255, 255, 255))
        surface.blit(health_text, (health_x + 5, health_y + 2))
        
        # Vidas
        lives_text = font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        surface.blit(lives_text, (health_x, health_y + 30))
        
        # Puntuación con efecto de brillo
        score_font = pygame.font.Font(None, 28)
        score_text = score_font.render(f"Puntos: {self.score}", True, (255, 255, 200))
        
        # Sombra del texto
        shadow_surf = score_font.render(f"Puntos: {self.score}", True, (0, 0, 0))
        surface.blit(shadow_surf, (SCREEN_WIDTH - 201, 21))
        
        surface.blit(score_text, (SCREEN_WIDTH - 200, 20))
        
        # Combo
        if self.combo > 0:
            combo_color = (255, 50, 255) if self.combo >= 15 else (255, 255, 50) if self.combo >= 10 else (50, 255, 255)
            combo_text = font.render(f"COMBO: x{self.combo}", True, combo_color)
            
            # Sombra del combo
            shadow_combo = font.render(f"COMBO: x{self.combo}", True, (0, 0, 0))
            surface.blit(shadow_combo, (SCREEN_WIDTH - 201, 51))
            
            surface.blit(combo_text, (SCREEN_WIDTH - 200, 50))
            
            # Barra de tiempo del combo con efecto de pulso
            combo_bar_width = 150
            combo_bar_height = 8
            combo_percentage = self.combo_timer / 3.0
            
            # Fondo de la barra
            pygame.draw.rect(surface, (50, 50, 50), (SCREEN_WIDTH - 200, 75, combo_bar_width, combo_bar_height))
            
            # Barra de progreso con gradiente
            if combo_percentage > 0.5:
                bar_color = combo_color
            elif combo_percentage > 0.25:
                bar_color = (combo_color[0]//2, combo_color[1]//2, combo_color[2]//2)
            else:
                bar_color = (combo_color[0]//4, combo_color[1]//4, combo_color[2]//4)
            
            current_bar_width = int(combo_bar_width * combo_percentage)
            pygame.draw.rect(surface, bar_color, (SCREEN_WIDTH - 200, 75, current_bar_width, combo_bar_height))
            
            # Borde de la barra
            pygame.draw.rect(surface, (255, 255, 255), (SCREEN_WIDTH - 200, 75, combo_bar_width, combo_bar_height), 1)
        
        # Power-ups activos con iconos
        powerup_y = 100
        icon_size = 20
        
        if self.shield_active:
            # Icono de escudo
            shield_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
            pygame.draw.circle(shield_icon, SHIELD_COLOR, (icon_size//2, icon_size//2), icon_size//2 - 2, 2)
            pygame.draw.polygon(shield_icon, SHIELD_COLOR, 
                              [(icon_size//2, 4), (icon_size-4, icon_size//2), 
                               (icon_size//2, icon_size-4), (4, icon_size//2)])
            surface.blit(shield_icon, (20, powerup_y))
            
            shield_text = font.render(f"ESCUDO: {self.shield_timer:.1f}s", True, SHIELD_COLOR)
            surface.blit(shield_text, (50, powerup_y + 2))
            powerup_y += 30
        
        if self.speed_boost:
            # Icono de velocidad
            speed_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
            pygame.draw.circle(speed_icon, (255, 200, 0), (icon_size//2, icon_size//2), icon_size//2 - 2)
            for i in range(3):
                angle = i * 120 + self.game_time * 200
                x1 = icon_size//2 + (icon_size//3) * math.cos(math.radians(angle))
                y1 = icon_size//2 + (icon_size//3) * math.sin(math.radians(angle))
                x2 = icon_size//2 + (icon_size//2 - 1) * math.cos(math.radians(angle))
                y2 = icon_size//2 + (icon_size//2 - 1) * math.sin(math.radians(angle))
                pygame.draw.line(speed_icon, (255, 255, 200), (x1, y1), (x2, y2), 3)
            surface.blit(speed_icon, (20, powerup_y))
            
            speed_text = font.render(f"VELOCIDAD: {self.speed_timer:.1f}s", True, (255, 200, 0))
            surface.blit(speed_text, (50, powerup_y + 2))
            powerup_y += 30
        
        if self.zoom_active:
            # Icono de zoom
            zoom_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
            pygame.draw.circle(zoom_icon, (0, 255, 255), (icon_size//2, icon_size//2), icon_size//2 - 2, 2)
            pygame.draw.line(zoom_icon, (0, 255, 255), (icon_size-4, 4), (icon_size-8, 8), 2)
            pygame.draw.line(zoom_icon, (0, 255, 255), (icon_size-6, 4), (icon_size-4, 6), 2)
            surface.blit(zoom_icon, (20, powerup_y))
            
            zoom_text = font.render(f"ZOOM: {self.zoom_timer:.1f}s", True, (0, 255, 255))
            surface.blit(zoom_text, (50, powerup_y + 2))