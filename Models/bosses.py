# Crea archivo: bosses.py

"""
bosses.py - Jefes épicos para SkyRunner
"""

import pygame
import math
import random
import time
from objects.constants import *

class CompilerDemon:
    """Boss épico que lanza errores de código y excepciones"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 150
        self.health = 1000
        self.max_health = 1000
        self.active = True
        self.phase = 1  # 1, 2, 3
        
        # Estados de ataque
        self.attack_timer = 0
        self.attack_cooldown = 2.0
        self.current_attack = None
        
        # Movimiento
        self.speed = 1.5
        self.target_x = x
        self.target_y = y
        self.wave_timer = 0
        
        # Efectos visuales
        self.eye_glow = 0
        self.code_lines = []
        self.generate_code_lines()
        self.error_particles = []
        self.exception_crystals = []
        
        # Ataques
        self.syntax_errors = []
        self.runtime_errors = []
        self.exception_freezes = []
        
        # Música/audio
        self.boss_music_started = False
    
    def generate_code_lines(self):
        """Genera líneas de código flotantes"""
        code_snippets = [
            "if (player.alive) { attack(); }",
            "while (true) { spawn_enemy(); }",
            "catch (Player player) { damage(50); }",
            "throw new Exception('YOU DIED');",
            "public void bossAttack() {",
            "// TODO: Implement player destruction",
            "console.error('PLAYER FOUND');",
            "git commit -m 'Add boss mechanics'",
            "npm install demon-package",
            "while (!player.dead) { chase(); }"
        ]
        
        for _ in range(15):
            self.code_lines.append({
                'text': random.choice(code_snippets),
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2.0),
                'alpha': random.randint(100, 200),
                'size': random.randint(12, 20)
            })
    
    def update(self, dt, player_pos=None):
        """Actualiza el boss y sus ataques"""
        self.wave_timer += dt
        self.eye_glow = abs(math.sin(self.wave_timer * 2)) * 255
        
        # Movimiento en onda
        self.y += math.sin(self.wave_timer) * 0.5
        
        # Seguir al jugador suavemente
        if player_pos:
            dx = player_pos[0] - self.x
            dy = (player_pos[1] - 200) - self.y  # Mantenerse arriba del jugador
            
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                self.x += (dx / dist) * self.speed * 0.3
                self.y += (dy / dist) * self.speed * 0.3
        
        # Limitar movimiento
        self.x = max(self.width//2, min(SCREEN_WIDTH - self.width//2, self.x))
        self.y = max(100, min(300, self.y))
        
        # Actualizar temporizador de ataque
        self.attack_timer += dt
        
        # Cambiar fase según salud
        if self.health < self.max_health * 0.66 and self.phase == 1:
            self.phase = 2
            self.speed *= 1.5
            self.attack_cooldown *= 0.7
            print("[BOSS] ¡FASE 2 ACTIVADA! Velocidad aumentada")
            
        if self.health < self.max_health * 0.33 and self.phase == 2:
            self.phase = 3
            self.speed *= 1.3
            self.attack_cooldown *= 0.5
            print("[BOSS] ¡FASE 3 ACTIVADA! MODO OVERCLOCK")
        
        # Elegir ataque
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer = 0
            
            if self.phase == 1:
                self.attack_syntax_error()
            elif self.phase == 2:
                if random.random() < 0.5:
                    self.attack_runtime_error()
                else:
                    self.attack_syntax_error()
            else:  # Fase 3
                attacks = [self.attack_syntax_error, 
                          self.attack_runtime_error, 
                          self.attack_exception_freeze]
                random.choice(attacks)()
        
        # Actualizar ataques activos
        self.update_attacks(dt)
        self.update_code_lines(dt)
        self.update_particles(dt)
    
    def attack_syntax_error(self):
        """Lanza errores de sintaxis que persiguen al jugador"""
        print("[BOSS] ¡Error de sintaxis lanzado!")
        
        for _ in range(3 if self.phase == 1 else 5 if self.phase == 2 else 8):
            error = {
                'x': self.x + random.randint(-50, 50),
                'y': self.y + random.randint(-30, 30),
                'speed': 3.0 + self.phase * 0.5,
                'target_x': None,
                'target_y': None,
                'life': 5.0,
                'text': random.choice(['SyntaxError', 'TypeError', 'ReferenceError']),
                'color': (255, 50, 50)
            }
            self.syntax_errors.append(error)
            
            # Efecto de partículas
            for _ in range(10):
                self.error_particles.append({
                    'x': error['x'],
                    'y': error['y'],
                    'vx': random.uniform(-3, 3),
                    'vy': random.uniform(-3, 3),
                    'life': random.uniform(0.5, 1.0),
                    'color': (255, 100, 100)
                })
    
    def attack_runtime_error(self):
        """Lanza errores de tiempo de ejecución que explotan"""
        print("[BOSS] ¡Error de tiempo de ejecución!")
        
        for _ in range(2 if self.phase == 1 else 3 if self.phase == 2 else 5):
            error = {
                'x': self.x + random.randint(-100, 100),
                'y': self.y + random.randint(-50, 50),
                'speed': 2.0,
                'angle': random.uniform(0, math.pi*2),
                'life': 3.0,
                'explosion_timer': 2.0,
                'text': random.choice(['RuntimeError', 'RangeError', 'EvalError']),
                'color': (255, 150, 50)
            }
            self.runtime_errors.append(error)
    
    def attack_exception_freeze(self):
        """Lanza cristales de excepción que congelan"""
        print("[BOSS] ¡Excepción congelante!")
        
        for _ in range(1 if self.phase < 3 else 3):
            crystal = {
                'x': self.x,
                'y': self.y,
                'angle': random.uniform(0, math.pi*2),
                'rotation': 0,
                'rotation_speed': random.uniform(1, 3),
                'life': 4.0,
                'freeze_radius': 100,
                'active': False,
                'activation_timer': 1.0
            }
            self.exception_crystals.append(crystal)
    
    def update_attacks(self, dt):
        """Actualiza todos los ataques activos"""
        # Errores de sintaxis (persiguen)
        for error in self.syntax_errors[:]:
            error['life'] -= dt
            
            if error['life'] <= 0:
                self.syntax_errors.remove(error)
                continue
            
            # Movimiento hacia abajo con oscilación
            error['x'] += math.sin(self.wave_timer * 5 + error['x'] * 0.01) * 2
            error['y'] += error['speed']
            
            # Crear estela
            if random.random() < 0.3:
                self.error_particles.append({
                    'x': error['x'],
                    'y': error['y'],
                    'vx': random.uniform(-1, 1),
                    'vy': random.uniform(-1, 1),
                    'life': random.uniform(0.3, 0.7),
                    'color': error['color']
                })
        
        # Errores de runtime (vuelan y explotan)
        for error in self.runtime_errors[:]:
            error['life'] -= dt
            error['explosion_timer'] -= dt
            
            if error['life'] <= 0:
                # Explotar
                self.create_explosion(error['x'], error['y'], error['color'])
                self.runtime_errors.remove(error)
                continue
            
            # Movimiento en línea recta
            error['x'] += math.cos(error['angle']) * error['speed']
            error['y'] += math.sin(error['angle']) * error['speed']
            
            # Temblar antes de explotar
            if error['explosion_timer'] < 0.5:
                error['x'] += random.uniform(-2, 2)
                error['y'] += random.uniform(-2, 2)
        
        # Cristales de excepción
        for crystal in self.exception_crystals[:]:
            crystal['life'] -= dt
            crystal['rotation'] += crystal['rotation_speed'] * dt
            crystal['activation_timer'] -= dt
            
            if crystal['life'] <= 0:
                self.exception_crystals.remove(crystal)
                continue
            
            # Movimiento en espiral
            crystal['angle'] += 0.05
            radius = 50 + (3.0 - crystal['life']) * 20
            crystal['x'] = self.x + math.cos(crystal['angle']) * radius
            crystal['y'] = self.y + math.sin(crystal['angle']) * radius
            
            # Activar después del tiempo
            if crystal['activation_timer'] <= 0 and not crystal['active']:
                crystal['active'] = True
                print("[BOSS] ¡Cristal de excepción activado!")
    
    def update_code_lines(self, dt):
        """Actualiza líneas de código flotantes"""
        for line in self.code_lines:
            line['y'] += line['speed']
            line['alpha'] = 150 + int(math.sin(self.wave_timer * 2 + line['x'] * 0.01) * 50)
            
            # Reiniciar cuando salga de pantalla
            if line['y'] > SCREEN_HEIGHT + 50:
                line['y'] = -50
                line['x'] = random.randint(0, SCREEN_WIDTH)
    
    def update_particles(self, dt):
        """Actualiza partículas"""
        for p in self.error_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vx'] *= 0.95
            p['vy'] *= 0.95
            p['life'] -= dt
            
            if p['life'] <= 0:
                self.error_particles.remove(p)
    
    def create_explosion(self, x, y, color):
        """Crea explosión de partículas"""
        for _ in range(30):
            angle = random.uniform(0, math.pi*2)
            speed = random.uniform(2, 8)
            
            self.error_particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.5, 1.5),
                'color': color
            })
    
    def take_damage(self, damage):
        """Recibe daño y retorna si murió"""
        self.health -= damage
        
        # Efecto visual de daño
        for _ in range(10):
            self.error_particles.append({
                'x': self.x + random.randint(-self.width//2, self.width//2),
                'y': self.y + random.randint(-self.height//2, self.height//2),
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-5, 5),
                'life': random.uniform(0.3, 0.8),
                'color': (255, 255, 255)
            })
        
        print(f"[BOSS] Salud: {self.health}/{self.max_health}")
        
        if self.health <= 0:
            self.active = False
            # Gran explosión final
            for _ in range(100):
                self.create_explosion(self.x, self.y, (255, 50, 50))
            print("[BOSS] ¡COMPILER DEMON DERROTADO!")
            return True
        
        return False
    
    def draw(self, surface, camera_offset):
        """Dibuja el boss con todos sus efectos"""
        screen_x = self.x
        screen_y = self.y - camera_offset
        
        # ============================================
        # 👹 CUERPO DEL DEMONIO COMPILADOR
        # ============================================
        # Sombra
        shadow_rect = pygame.Rect(
            screen_x - self.width//2 + 5,
            screen_y - self.height//2 + 5,
            self.width,
            self.height
        )
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=15)
        
        # Cuerpo principal
        body_rect = pygame.Rect(
            screen_x - self.width//2,
            screen_y - self.height//2,
            self.width,
            self.height
        )
        
        # Color que cambia con la fase
        if self.phase == 1:
            body_color = (100, 0, 100)  # Púrpura
        elif self.phase == 2:
            body_color = (150, 0, 0)    # Rojo oscuro
        else:
            # Efecto de parpadeo en fase 3
            if int(pygame.time.get_ticks() / 100) % 2 == 0:
                body_color = (255, 50, 50)  # Rojo brillante
            else:
                body_color = (255, 150, 50) # Naranja
        
        pygame.draw.rect(surface, body_color, body_rect, border_radius=15)
        
        # Detalles del cuerpo
        detail_color = (200, 200, 255)
        for i in range(3):
            detail_y = screen_y - self.height//4 + i * (self.height//3)
            detail_width = self.width - 40
            pygame.draw.rect(surface, detail_color,
                           (screen_x - detail_width//2, detail_y, detail_width, 10),
                           border_radius=5)
        
        # ============================================
        # 👁️ OJOS DEL DEMONIO
        # ============================================
        eye_radius = 20
        for i, offset in enumerate([-40, 40]):
            eye_x = screen_x + offset
            eye_y = screen_y - 10
            
            # Ojo exterior
            pygame.draw.circle(surface, (30, 30, 30), (int(eye_x), int(eye_y)), eye_radius)
            
            # Brillo del ojo
            glow_color = (255, int(self.eye_glow * 0.7), 0, int(self.eye_glow))
            glow_surf = pygame.Surface((eye_radius*2, eye_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, glow_color,
                             (eye_radius, eye_radius), eye_radius)
            surface.blit(glow_surf, (int(eye_x - eye_radius), int(eye_y - eye_radius)))
            
            # Pupila
            pupil_radius = 8
            pupil_color = (255, 255, 0) if self.phase < 3 else (255, 0, 0)
            pygame.draw.circle(surface, pupil_color,
                             (int(eye_x), int(eye_y)), pupil_radius)
            
            # Reflejo en la pupila
            pygame.draw.circle(surface, WHITE,
                             (int(eye_x - 3), int(eye_y - 3)), 3)
        
        # ============================================
        # 👄 BOCA/CONSOLA DEL DEMONIO
        # ============================================
        mouth_width = 80
        mouth_height = 30
        mouth_rect = pygame.Rect(
            screen_x - mouth_width//2,
            screen_y + 20,
            mouth_width,
            mouth_height
        )
        
        # Boca negra
        pygame.draw.rect(surface, (20, 20, 20), mouth_rect, border_radius=5)
        
        # Texto de consola que cambia
        font = pygame.font.Font(None, 16)
        console_texts = [
            "> compiling attack...",
            "> error: player not found",
            "> launching syntax error",
            "> status: ANGRY",
            f"> health: {self.health}/{self.max_health}"
        ]
        
        current_text = console_texts[int(self.wave_timer * 0.5) % len(console_texts)]
        text_surf = font.render(current_text, True, (0, 255, 0))
        text_rect = text_surf.get_rect(center=(screen_x, screen_y + 35))
        surface.blit(text_surf, text_rect)
        
        # ============================================
        # 📊 BARRA DE SALUD ÉPICA
        # ============================================
        health_bar_width = 300
        health_bar_height = 25
        health_bar_x = SCREEN_WIDTH // 2 - health_bar_width // 2
        health_bar_y = 50
        
        # Fondo
        pygame.draw.rect(surface, (50, 50, 50),
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height),
                        border_radius=5)
        
        # Salud actual
        health_percent = self.health / self.max_health
        health_width = int(health_bar_width * health_percent)
        
        # Color que cambia según salud
        if health_percent > 0.66:
            health_color = (0, 255, 100)  # Verde
        elif health_percent > 0.33:
            health_color = (255, 200, 50)  # Naranja
        else:
            # Parpadeo rojo en poca salud
            if int(pygame.time.get_ticks() / 200) % 2 == 0:
                health_color = (255, 50, 50)  # Rojo
            else:
                health_color = (255, 100, 100)  # Rojo claro
        
        pygame.draw.rect(surface, health_color,
                        (health_bar_x, health_bar_y, health_width, health_bar_height),
                        border_radius=5)
        
        # Borde
        pygame.draw.rect(surface, WHITE,
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height),
                        3, border_radius=5)
        
        # Texto del nombre del boss
        boss_font = pygame.font.Font(None, 32)
        boss_name = "COMPILER DEMON"
        if self.phase == 2:
            boss_name += " [TURBO MODE]"
        elif self.phase == 3:
            boss_name += " [OVERCLOCK]"
        
        name_surf = boss_font.render(boss_name, True, (255, 100, 100))
        surface.blit(name_surf, (SCREEN_WIDTH//2 - name_surf.get_width()//2, 20))
        
        # Texto de fase
        phase_font = pygame.font.Font(None, 24)
        phase_text = f"Fase {self.phase}/3"
        phase_surf = phase_font.render(phase_text, True, (255, 255, 100))
        surface.blit(phase_surf, (SCREEN_WIDTH//2 - phase_surf.get_width()//2, 80))
        
        # ============================================
        # 📝 LÍNEAS DE CÓDIGO FLOTANTES
        # ============================================
        for line in self.code_lines:
            line_screen_y = line['y'] - camera_offset
            
            if -50 < line_screen_y < SCREEN_HEIGHT + 50:
                font = pygame.font.Font(None, line['size'])
                text_surf = font.render(line['text'], True, 
                                      (0, 255, 0, line['alpha']))
                
                # Crear superficie con alpha
                text_with_alpha = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
                text_with_alpha.blit(text_surf, (0, 0))
                text_with_alpha.set_alpha(line['alpha'])
                
                surface.blit(text_with_alpha, (line['x'], line_screen_y))
        
        # ============================================
        # ⚡ ATAQUES ACTIVOS
        # ============================================
        # Errores de sintaxis
        for error in self.syntax_errors:
            error_screen_y = error['y'] - camera_offset
            
            if -50 < error_screen_y < SCREEN_HEIGHT + 50:
                # Círculo del error
                pygame.draw.circle(surface, error['color'],
                                 (int(error['x']), int(error_screen_y)), 15)
                
                # Texto del error
                error_font = pygame.font.Font(None, 14)
                text_surf = error_font.render(error['text'], True, WHITE)
                text_rect = text_surf.get_rect(center=(int(error['x']), int(error_screen_y)))
                surface.blit(text_surf, text_rect)
                
                # Anillo exterior
                ring_radius = 15 + math.sin(self.wave_timer * 10) * 3
                pygame.draw.circle(surface, (255, 255, 255),
                                 (int(error['x']), int(error_screen_y)),
                                 int(ring_radius), 2)
        
        # Errores de runtime
        for error in self.runtime_errors:
            error_screen_y = error['y'] - camera_offset
            
            if -50 < error_screen_y < SCREEN_HEIGHT + 50:
                # Triángulo del error
                points = [
                    (error['x'], error_screen_y - 15),
                    (error['x'] - 13, error_screen_y + 10),
                    (error['x'] + 13, error_screen_y + 10)
                ]
                pygame.draw.polygon(surface, error['color'], points)
                
                # Signo de exclamación
                exclamation_font = pygame.font.Font(None, 20)
                exclamation = exclamation_font.render("!", True, WHITE)
                exclamation_rect = exclamation.get_rect(center=(int(error['x']), 
                                                              int(error_screen_y)))
                surface.blit(exclamation, exclamation_rect)
                
                # Temblar si está por explotar
                if error['explosion_timer'] < 0.5:
                    shake = math.sin(self.wave_timer * 20) * 3
                    pygame.draw.circle(surface, (255, 255, 255, 100),
                                     (int(error['x'] + shake), int(error_screen_y + shake)),
                                     25, 2)
        
        # Cristales de excepción
        for crystal in self.exception_crystals:
            crystal_screen_y = crystal['y'] - camera_offset
            
            if -50 < crystal_screen_y < SCREEN_HEIGHT + 50:
                # Cristal hexagonal
                crystal_color = (100, 200, 255) if crystal['active'] else (200, 200, 255)
                
                points = []
                for i in range(6):
                    angle = crystal['rotation'] + (i * math.pi / 3)
                    radius = 20
                    x = crystal['x'] + math.cos(angle) * radius
                    y = crystal_screen_y + math.sin(angle) * radius
                    points.append((x, y))
                
                pygame.draw.polygon(surface, crystal_color, points)
                pygame.draw.polygon(surface, WHITE, points, 2)
                
                # Centro del cristal
                pygame.draw.circle(surface, (255, 255, 255),
                                 (int(crystal['x']), int(crystal_screen_y)), 5)
                
                # Aura de congelación si está activo
                if crystal['active']:
                    freeze_radius = crystal['freeze_radius']
                    pygame.draw.circle(surface, (100, 200, 255, 50),
                                     (int(crystal['x']), int(crystal_screen_y)),
                                     int(freeze_radius), 2)
                    
                    # Partículas de hielo
                    for _ in range(2):
                        angle = random.uniform(0, math.pi*2)
                        dist = random.uniform(0, freeze_radius)
                        px = crystal['x'] + math.cos(angle) * dist
                        py = crystal_screen_y + math.sin(angle) * dist
                        
                        pygame.draw.circle(surface, (200, 230, 255),
                                         (int(px), int(py)), 2)
        
        # ============================================
        # ✨ PARTÍCULAS DE ERROR
        # ============================================
        for p in self.error_particles:
            particle_screen_y = p['y'] - camera_offset
            
            if -50 < particle_screen_y < SCREEN_HEIGHT + 50:
                alpha = int(255 * p['life'] * 2)
                if alpha > 0:
                    particle_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surf, (*p['color'], alpha),
                                     (3, 3), 3)
                    surface.blit(particle_surf,
                               (int(p['x'] - 3), int(particle_screen_y - 3)))
        
        # ============================================
        # 🔥 EFECTO DE FASE 3 (OVERCLOCK)
        # ============================================
        if self.phase == 3:
            # Distorsión de pantalla
            if int(pygame.time.get_ticks() / 50) % 2 == 0:
                # Líneas de distorsión
                for i in range(SCREEN_HEIGHT // 20):
                    y = i * 20 + (self.wave_timer * 50) % 20
                    pygame.draw.line(surface, (255, 255, 255, 50),
                                   (0, y), (SCREEN_WIDTH, y), 1)
            
            # Texto "OVERCLOCK" parpadeante
            if int(pygame.time.get_ticks() / 100) % 2 == 0:
                overclock_font = pygame.font.Font(None, 48)
                overclock_text = overclock_font.render("OVERCLOCK", True, (255, 50, 50))
                overclock_rect = overclock_text.get_rect(center=(SCREEN_WIDTH//2, 120))
                
                # Sombra
                shadow = overclock_font.render("OVERCLOCK", True, BLACK)
                surface.blit(shadow, (overclock_rect.x + 2, overclock_rect.y + 2))
                surface.blit(overclock_text, overclock_rect)
    
    def get_rect(self):
        """Retorna rectángulo de colisión"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2,
                          self.width, self.height)
    
    def check_collision_with_player(self, player_rect):
        """Verifica colisiones con ataques del boss"""
        damage_taken = 0
        
        # Colisión con errores de sintaxis
        for error in self.syntax_errors[:]:
            error_rect = pygame.Rect(error['x'] - 15, error['y'] - 15, 30, 30)
            if player_rect.colliderect(error_rect):
                damage_taken += 20
                self.syntax_errors.remove(error)
                print("[BOSS] ¡Error de sintaxis golpeó al jugador!")
        
        # Colisión con errores de runtime
        for error in self.runtime_errors[:]:
            error_rect = pygame.Rect(error['x'] - 15, error['y'] - 15, 30, 30)
            if player_rect.colliderect(error_rect):
                damage_taken += 30
                self.runtime_errors.remove(error)
                self.create_explosion(error['x'], error['y'], (255, 150, 50))
                print("[BOSS] ¡Error de runtime explotó en el jugador!")
        
        # Colisión con cristales de excepción (congela)
        for crystal in self.exception_crystals:
            if crystal['active']:
                crystal_rect = pygame.Rect(crystal['x'] - crystal['freeze_radius'],
                                         crystal['y'] - crystal['freeze_radius'],
                                         crystal['freeze_radius'] * 2,
                                         crystal['freeze_radius'] * 2)
                if player_rect.colliderect(crystal_rect):
                    damage_taken += 10
                    print("[BOSS] ¡Jugador congelado por excepción!")
                    # Aquí podrías añadir efecto de congelación al jugador
        
        return damage_taken