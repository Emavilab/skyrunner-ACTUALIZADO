"""
game.py - Clase Principal del Juego COMPLETAMENTE CORREGIDA
"""

import pygame
import random
import math
import time
import json
import os
from datetime import datetime
from objects.constants import *
from Models.player import Player
from Levels.level import Level
from objects.powerup import PowerUp, CollectionEffect
from objects.utils import lerp, draw_text
from objects.audio import init_audio, play_sound, toggle_mute, is_muted
from Models.lava import Lava

class Game:
    def __init__(self, difficulty="normal", screen=None):
        # Pantalla - usar la pantalla existente o crear una nueva
        if screen is None:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.return_to_menu = False  # Nueva bandera para volver al menú
        
        # Dificultad
        self.difficulty = difficulty
        self.settings = DIFFICULTY_SETTINGS[difficulty]
        
        # Inicializar audio
        init_audio()
        
        # Estado del juego
        self.state = STATE_PLAYING
        self.current_level_number = 1
        
        # Instancias de juego
        self.player = None
        self.level = None
        self.lava = Lava(difficulty)
        
        # Cámara
        self.camera_y = 0
        self.target_camera_y = 0
        
        # Tiempo
        self.start_time = 0
        self.elapsed_time = 0
        self.game_time = 0
        
        # Efectos de pantalla
        self.screen_shake_magnitude = 0
        self.screen_shake_duration = 0
        
        # Fuentes
        self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
        self.font_subtitle = pygame.font.Font(None, FONT_SIZE_SUBTITLE)
        self.font_hud = pygame.font.Font(None, FONT_SIZE_HUD)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # High score
        self.player_name = ""
        self.entering_name = False
        self.is_new_high_score = False
        self.high_scores = self.load_high_scores()
        self.current_high_score = self.get_current_high_score()
        
        # Sistema de spawning de drones
        self.drone_spawn_timer = 0
        self.drone_spawn_interval = 8.0  # Segundos entre spawns
        self.last_drone_spawn_height = 0
        
        # Comenzar juego
        self.start_level(1)
    
    def load_high_scores(self):
        """Cargar puntuaciones altas desde archivo"""
        try:
            if os.path.exists("high_scores.json"):
                with open("high_scores.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return {
            "easy": [],
            "normal": [],
            "hard": []
        }
    
    def get_current_high_score(self):
        """Obtener el récord actual de la dificultad seleccionada"""
        scores = self.high_scores.get(self.difficulty, [])
        if scores:
            return max(score["score"] for score in scores)
        return 0
    
    def is_high_score(self, score):
        """Verificar si la puntuación es un nuevo récord"""
        scores = self.high_scores.get(self.difficulty, [])
        if len(scores) < 10:
            return True
        return score > min(score["score"] for score in scores)
    
    def save_high_score(self, name, score):
        """Guardar nueva puntuación alta"""
        try:
            self.high_scores[self.difficulty].append({
                "name": name[:3].upper(),
                "score": score,
                "date": datetime.now().strftime("%Y-%m-%d")
            })
            # Ordenar y mantener solo top 10
            self.high_scores[self.difficulty].sort(key=lambda x: x["score"], reverse=True)
            self.high_scores[self.difficulty] = self.high_scores[self.difficulty][:10]
            
            with open("high_scores.json", "w") as f:
                json.dump(self.high_scores, f, indent=2)
            
            # Actualizar récord actual
            self.current_high_score = self.get_current_high_score()
            return True
        except Exception as e:
            print(f"[HighScore] Error al guardar: {e}")
            return False
    
    def start_level(self, level_number):
        self.current_level_number = level_number
        
        # Resetear sistema de drones
        self.drone_spawn_timer = 0
        self.last_drone_spawn_height = 0
        
        # Ajustar intervalo de spawn según dificultad
        self.drone_spawn_interval = {
            "easy": 12.0,
            "normal": 8.0,
            "hard": 5.0
        }.get(self.difficulty, 8.0)
        
        # Ajustar configuración según dificultad
        level_config = LEVELS_CONFIG[level_number].copy()
        
        for enemy_type in ['bats', 'traps', 'rocks', 'lightning']:
            if enemy_type in level_config:
                level_config[enemy_type] = int(
                    level_config[enemy_type] * self.settings["enemy_rate"]
                )
        
        if 'powerups' in level_config:
            level_config['powerups'] = int(
                level_config['powerups'] * self.settings["powerup_rate"]
            )
        
        self.level = Level(level_number, level_config, difficulty=self.difficulty)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, self.settings)
        
        # Inicializar lava
        if self.player:
            self.lava.initialize(self.player.y)
        
        # Resetear cámara
        self.camera_y = 0
        self.target_camera_y = 0
        
        # Iniciar temporizador
        self.start_time = time.time()
        
        # Cambiar estado
        self.state = STATE_PLAYING
    
    def update_camera(self):
        if not self.player:
            return
        
        self.target_camera_y = self.player.y - CAMERA_OFFSET_Y
        self.camera_y = lerp(self.camera_y, self.target_camera_y, CAMERA_SMOOTHING)
    
    def spawn_drone(self):
        """Genera un nuevo drone en el trayecto de subida"""
        if not self.level or not self.player:
            return
        
        # Solo spawnear en niveles 2 y 3
        if self.current_level_number < 2:
            return
        
        try:
            from Models.enemies import SurveillanceDrone
            
            # Posicionar drone más arriba del jugador
            spawn_distance = 400  # Distancia por encima del jugador
            x = random.randint(150, SCREEN_WIDTH - 150)
            y = self.player.y - spawn_distance
            
            # Evitar spawn muy cerca de drones existentes
            too_close = False
            for enemy in self.level.enemies:
                if hasattr(enemy, '__class__') and enemy.__class__.__name__ == 'SurveillanceDrone':
                    distance = math.sqrt((enemy.x - x)**2 + (enemy.y - y)**2)
                    if distance < 200:
                        too_close = True
                        break
            
            if too_close:
                return
            
            # Crear drone con parámetros según nivel y dificultad
            patrol_range = 150
            detection_range = 200
            
            if self.current_level_number == 3:
                detection_range = 300
            
            # Ajustar según dificultad
            if self.difficulty == "hard":
                detection_range += 100
                patrol_range += 50
            elif self.difficulty == "easy":
                detection_range -= 50
            
            drone = SurveillanceDrone(x, y, patrol_range=patrol_range, detection_range=detection_range)
            
            # Mejorar según nivel
            if self.current_level_number == 3:
                drone.speed = 2.5
            
            self.level.enemies.append(drone)
            print(f"[Drone Spawn] Nuevo drone en ({x}, {y}) - Difficulty: {self.difficulty}")
            
        except Exception as e:
            print(f"[Drone Spawn] Error: {e}")
    
    def check_collisions(self):
        if not self.player or not self.level:
            return
        
        player_rect = self.player.get_rect()
        
        # Colisiones con enemigos
        for enemy in self.level.enemies:
            if not enemy.active:
                continue
            
            enemy_rect = enemy.get_rect()
            if player_rect.colliderect(enemy_rect):
                lost_life = self.player.take_damage(enemy.damage)
                enemy.active = False
                
                if lost_life:
                    play_sound('death')
                else:
                    play_sound('damage')
                
                self.screen_shake_magnitude = 5
                self.screen_shake_duration = 0.2
        
        # Colisiones con power-ups - VERSIÓN SIMPLE
        for powerup in self.level.powerups:
            if powerup.collected:
                continue
            
            powerup_rect = powerup.get_rect()
            if player_rect.colliderect(powerup_rect):
                if powerup.collect():
                    self.player.activate_powerup(powerup.type)
                    play_sound('powerup')
                    
                    # Efecto visual
                    color = powerup.colors.get(powerup.type, (255, 255, 0))
                    effect = CollectionEffect(powerup.x, powerup.y, color)
                    self.level.effects.append(effect)
    
    def check_level_complete(self):
        """Verifica si el jugador llegó a la bandera de victoria - VERSIÓN SIMPLE"""
        if not self.player or not self.level:
            return
        
        # Verificar colisión con bandera
        if self.level.check_flag_collision(self.player.get_rect()):
            print(f"[Game] ¡NIVEL {self.current_level_number} COMPLETADO!")
            
            # Calcular puntos - VERSIÓN SIMPLIFICADA
            time_taken = self.elapsed_time
            base_points = POINTS_LEVEL_COMPLETE
            time_bonus = max(0, 90 - time_taken) * 50
            
            # Bono por vidas restantes
            lives_bonus = self.player.lives * 1000
            
            # Multiplicador de dificultad
            diff_multiplier = {
                "easy": 1.0,
                "normal": 1.5,
                "hard": 2.0
            }.get(self.difficulty, 1.0)
            
            total_points = int((base_points + time_bonus + lives_bonus) * diff_multiplier)
            
            # Sumar puntos al jugador
            old_score = self.player.score
            self.player.score += total_points
            
            print(f"[Game] Puntos añadidos: {total_points} (Score: {old_score} -> {self.player.score})")
            
            # Cambiar estado
            self.state = STATE_LEVEL_COMPLETE
            self.level_complete_data = {
                'points': total_points,
                'time': time_taken,
                'level': self.current_level_number,
                'lives': self.player.lives,
                'multiplier': diff_multiplier
            }
            
            # Efectos
            try:
                play_sound('level_complete')
            except:
                print("[Audio] No se pudo reproducir sonido de victoria")
            
            self.screen_shake_magnitude = 12
            self.screen_shake_duration = 2.0

    def draw_altitude_hud(self):
        """Muestra altura restante hasta la cima"""
        if not self.level or not self.player or self.state != STATE_PLAYING:
            return
        
        # Verificar si hay plataforma final
        if not hasattr(self.level, 'final_platform') or not self.level.final_platform:
            return
        
        # Calcular progreso
        start_y = SCREEN_HEIGHT - 100
        target_y = self.level.final_platform.y
        current_y = max(self.player.y, target_y)
        
        # Progreso (0% a 100%)
        total_distance = abs(start_y - target_y)
        traveled_distance = abs(start_y - current_y)
        progress = min(100, max(0, (traveled_distance / total_distance) * 100))
        
        # Altura restante
        remaining_pixels = max(0, total_distance - traveled_distance)
        
        # --- BARRA DE PROGRESO INFERIOR ---
        bar_width = 300
        bar_height = 22
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = SCREEN_HEIGHT - 45
        
        # Fondo
        pygame.draw.rect(self.screen, (40, 40, 60, 200),
                        (bar_x, bar_y, bar_width, bar_height), border_radius=6)
        
        # Barra de progreso
        fill_width = int((progress / 100) * bar_width)
        
        if progress < 33:
            bar_color = (255, 100, 100)
        elif progress < 66:
            bar_color = (255, 200, 100)
        else:
            bar_color = (100, 255, 100)
        
        pygame.draw.rect(self.screen, bar_color,
                        (bar_x, bar_y, fill_width, bar_height), border_radius=6)
        
        # Borde
        pygame.draw.rect(self.screen, WHITE,
                        (bar_x, bar_y, bar_width, bar_height), 2, border_radius=6)
        
        # Texto de porcentaje
        percent_text = f"{int(progress)}%"
        percent_surf = self.font_small.render(percent_text, True, WHITE)
        self.screen.blit(percent_surf, (bar_x + bar_width + 10, bar_y - 2))

    def update(self, dt):
        self.game_time += dt
        
        if self.state == STATE_PLAYING:
            self.elapsed_time = time.time() - self.start_time
            
            if self.player and self.player.alive:
                keys = pygame.key.get_pressed()
                self.player.handle_input(keys)
                self.player.update(dt, self.level.platforms)
            
            self.level.update(dt, self.player.y if self.player else 0)
            
            # Actualizar lava
            if self.player and self.player.alive:
                player_died = self.lava.update(
                    dt, 
                    self.player.y,
                    self.player.get_rect(),
                    self.state
                )
                
                if player_died:
                    print("[Game] Jugador tocó la lava")
                    
                    # Desactivar escudo si lo tiene para asegurar que pierda vida
                    if self.player.shield_active:
                        self.player.shield_active = False
                        print("[Player] Escudo desactivado por lava")
                    
                    # Aplicar daño letal para activar el sistema de vidas
                    vidas_antes = self.player.lives
                    lost_life = self.player.take_damage(max(self.player.health, 500))  # Daño suficiente para matar
                    
                    if lost_life and self.player.lives > 0:
                        # Si perdió una vida pero le quedan vidas, reiniciar lava
                        print(f"[Game] Vida perdida por lava - Vidas restantes: {self.player.lives}")
                        print("[Game] Reiniciando lava para nueva vida")
                        self.lava.reset(self.player.y)
                        self.player_death("lava")  # Animación de muerte
                    else:
                        # Si no tiene vidas, muerte definitiva
                        print("[Game] Sin vidas - muerte definitiva por lava")
                        self.player_death("lava")
            
            self.update_camera()
            self.check_collisions()
            self.check_level_complete()
            
            # Sistema de spawning continuo de drones
            self.drone_spawn_timer += dt
            if self.drone_spawn_timer >= self.drone_spawn_interval:
                self.spawn_drone()
                self.drone_spawn_timer = 0
            
            # Verificar si el jugador murió completamente (sin vidas)
            if self.player and not self.player.alive and self.player.lives <= 0:
                print("[Game] Cambiando a STATE_GAME_OVER - jugador sin vidas")
                self.state = STATE_GAME_OVER
            
            if self.screen_shake_duration > 0:
                self.screen_shake_duration -= dt
                if self.screen_shake_duration <= 0:
                    self.screen_shake_magnitude = 0
        
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()
            if hasattr(self, 'death_animation'):
                self.update_death_animation(dt)
    
    def player_death(self, death_type="enemy"):
        """Maneja la muerte del jugador con animación"""
        if not self.player:
            return
        
        # Solo marcar como muerto si realmente no tiene vidas
        # El método take_damage ya maneja las vidas y alive status
        
        self.death_animation = {
            'type': death_type,
            'particles': [],
            'player_x': self.player.x,
            'player_y': self.player.y,
            'time': 1.5
        }
        
        color = RED if death_type == "lava" else ORANGE
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            life = random.uniform(0.5, 1.5)
            
            self.death_animation['particles'].append({
                'x': self.player.x, 'y': self.player.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': life,
                'max_life': life,
                'size': random.randint(3, 8),
                'color': color
            })
        
        self.screen_shake_magnitude = 10
        self.screen_shake_duration = 0.5
        play_sound('death')
        self.death_timer = 1.5
    
    def update_death_animation(self, dt):
        if not hasattr(self, 'death_animation') or not self.death_animation:
            return
        
        self.death_timer -= dt
        
        for p in self.death_animation['particles'][:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.5
            p['life'] -= dt
            
            if p['life'] <= 0:
                self.death_animation['particles'].remove(p)
        
        # Solo limpiar la animación cuando termine, NO reiniciar nivel automáticamente
        if self.death_timer <= 0 or not self.death_animation['particles']:
            self.death_animation = None
    
    def draw(self):
        shake_x = 0
        shake_y = 0
        if self.screen_shake_magnitude > 0:
            shake_x = random.randint(-self.screen_shake_magnitude, self.screen_shake_magnitude)
            shake_y = random.randint(-self.screen_shake_magnitude, self.screen_shake_magnitude)
        
        if self.state == STATE_PLAYING:
            self.level.draw_background(self.screen, self.camera_y)
            
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_surface.fill(self.level.theme['bg'])
            self.level.draw(temp_surface, self.camera_y)
            
            # Dibujar lava
            self.lava.draw(temp_surface, self.camera_y)
            
            if self.player and self.player.alive:
                self.player.draw(temp_surface, self.camera_y)
            
            if hasattr(self, 'death_animation') and self.death_animation:
                for p in self.death_animation['particles']:
                    screen_y = p['y'] - self.camera_y
                    alpha = int(255 * (p['life'] / p['max_life']))
                    color = (*p['color'][:3], alpha)
                    particle_surf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surf, color, (p['size'], p['size']), p['size'])
                    temp_surface.blit(particle_surf, 
                                   (int(p['x'] - p['size'] + shake_x),
                                    int(screen_y - p['size'] + shake_y)))
            
            self.screen.blit(temp_surface, (shake_x, shake_y))
            
            # Dibujar HUD del jugador y la información del nivel
            if self.player:
                self.player.draw_hud(self.screen)
                self.draw_level_info_hud()
        
        elif self.state == STATE_PAUSED:
            self.level.draw_background(self.screen, self.camera_y)
            self.level.draw(self.screen, self.camera_y)
            self.lava.draw(self.screen, self.camera_y)
            if self.player:
                self.player.draw(self.screen, self.camera_y)
            
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            self.draw_pause_menu()
        
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()
        
        elif self.state == STATE_LEVEL_COMPLETE:
            self.draw_level_complete()
        
        elif self.state == STATE_VICTORY:
            self.draw_victory()
    
    def draw_level_info_hud(self):
        """Dibuja la información del nivel, tiempo y dificultad en la parte superior central"""
        # Calcular tiempo transcurrido
        elapsed_minutes = int(self.elapsed_time // 60)
        elapsed_seconds = int(self.elapsed_time % 60)
        time_str = f"{elapsed_minutes:02d}:{elapsed_seconds:02d}"
        
        # Obtener nombre del nivel
        level_names = {1: "Bosque Místico", 2: "Caverna Oscura", 3: "Tormenta Eléctrica"}
        level_name = level_names.get(self.current_level_number, f"Nivel {self.current_level_number}")
        
        # Configuración
        panel_width = 500
        panel_height = 70
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = 10
        
        # Dibujar panel semi-transparente
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (0, 0, 0, 180), (0, 0, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(panel_surf, self.settings["color"] + (255,), (0, 0, panel_width, panel_height), 3, border_radius=10)
        self.screen.blit(panel_surf, (panel_x, panel_y))
        
        # Dibujar nombre del nivel (arriba, centrado)
        level_text = self.font_subtitle.render(level_name, True, CYAN)
        level_text_rect = level_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 20))
        self.screen.blit(level_text, level_text_rect)
        
        # Dibujar tiempo y dificultad (abajo, en línea)
        info_y = panel_y + 45
        
        # Tiempo (izquierda)
        time_label = self.font_small.render("Tiempo:", True, WHITE)
        time_value = self.font_subtitle.render(time_str, True, YELLOW)
        self.screen.blit(time_label, (panel_x + 20, info_y - 2))
        self.screen.blit(time_value, (panel_x + 85, info_y - 2))
        
        # Dificultad (derecha)
        diff_label = self.font_small.render("Dificultad:", True, WHITE)
        diff_value = self.font_subtitle.render(self.settings['name'], True, self.settings['color'])
        self.screen.blit(diff_label, (panel_x + panel_width - 180, info_y - 2))
        self.screen.blit(diff_value, (panel_x + panel_width - 95, info_y - 2))
        
        # Mostrar récord actual (centro, debajo)
        if self.current_high_score > 0:
            record_text = f"Record: {self.current_high_score}"
            record_surface = self.font_small.render(record_text, True, (255, 215, 0))
            record_rect = record_surface.get_rect(center=(panel_x + panel_width // 2, panel_y + panel_height + 15))
            self.screen.blit(record_surface, record_rect)
        
        # Indicador de audio mute (esquina superior derecha)
        if is_muted():
            mute_text = "🔇 MUTE"
            mute_color = (255, 100, 100)
            mute_surface = self.font_small.render(mute_text, True, mute_color)
            self.screen.blit(mute_surface, (SCREEN_WIDTH - 100, 10))
    
    def draw_difficulty_hud(self):
        color = self.settings["color"]
        name = self.settings["name"]
        
        pygame.draw.rect(self.screen, color, 
                        (SCREEN_WIDTH - 150, 10, 140, 30), border_radius=5)
        pygame.draw.rect(self.screen, WHITE, 
                        (SCREEN_WIDTH - 150, 10, 140, 30), 2, border_radius=5)
        
        diff_text = self.font_hud.render(name, True, BLACK)
        self.screen.blit(diff_text, (SCREEN_WIDTH - 145, 15))
    
    def draw_pause_menu(self):
        draw_text(self.screen, "PAUSA", SCREEN_WIDTH // 2, 200,
                 self.font_title, YELLOW, center=True)
        
        draw_text(self.screen, f"Dificultad: {self.settings['name']}", 
                 SCREEN_WIDTH // 2, 280, self.font_subtitle, self.settings['color'], center=True)
        
        draw_text(self.screen, "ESC - Continuar", SCREEN_WIDTH // 2, 340,
                 self.font_subtitle, WHITE, center=True)
        
        draw_text(self.screen, "R - Reiniciar Nivel", SCREEN_WIDTH // 2, 390,
                 self.font_subtitle, WHITE, center=True)
        
        draw_text(self.screen, "Q - Volver al Menú Principal", SCREEN_WIDTH // 2, 440,
                 self.font_subtitle, WHITE, center=True)
        
        draw_text(self.screen, "M - Silenciar/Activar Audio", SCREEN_WIDTH // 2, 490,
                 self.font_small, (200, 200, 200), center=True)
        
        # Indicador de estado de audio
        mute_status = is_muted()
        mute_text = "🔇 SILENCIADO" if mute_status else "🔊 AUDIO ON"
        mute_color = (255, 100, 100) if mute_status else (100, 255, 100)
        draw_text(self.screen, mute_text, SCREEN_WIDTH // 2, 520,
                 self.font_small, mute_color, center=True)
    
    def draw_game_over(self):
        self.screen.fill(BLACK)
        
        draw_text(self.screen, "GAME OVER", SCREEN_WIDTH // 2, 150,
                 self.font_title, RED, center=True)
        
        if self.player:
            draw_text(self.screen, f"Puntuación: {self.player.score}",
                     SCREEN_WIDTH // 2, 250, self.font_subtitle, YELLOW, center=True)
            
            draw_text(self.screen, f"Nivel alcanzado: {self.current_level_number}",
                     SCREEN_WIDTH // 2, 300, self.font_small, WHITE, center=True)
            
            draw_text(self.screen, f"Dificultad: {self.settings['name']}",
                     SCREEN_WIDTH // 2, 330, self.font_small, self.settings['color'], center=True)
            
            draw_text(self.screen, "R - Reintentar", SCREEN_WIDTH // 2, 400,
                     self.font_subtitle, GREEN, center=True)
            
            draw_text(self.screen, "Q - Volver al Menú", SCREEN_WIDTH // 2, 450,
                     self.font_subtitle, WHITE, center=True)

    def draw_level_complete(self):
        """Pantalla de nivel completado - VERSIÓN SIMPLE"""
        import math
        import random
        
        # Fondo
        for y in range(SCREEN_HEIGHT):
            alpha = y / SCREEN_HEIGHT
            r = int(lerp(0, 50, alpha))
            g = int(lerp(50, 150, alpha))
            b = int(lerp(0, 50, alpha))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Título
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.002)) * 0.3 + 0.7
        title_color = (0, int(255 * pulse), 0)
        
        title = self.font_title.render("¡NIVEL COMPLETADO!", True, title_color)
        title_x = SCREEN_WIDTH // 2
        title_y = 100
        self.screen.blit(title, (title_x - title.get_width()//2, title_y))
        
        # Panel
        panel_width = 500
        panel_height = 300
        panel_x = SCREEN_WIDTH // 2 - panel_width // 2
        panel_y = 180
        
        pygame.draw.rect(self.screen, (0, 0, 0, 200),
                        (panel_x, panel_y, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(self.screen, WHITE,
                        (panel_x, panel_y, panel_width, panel_height), 3, border_radius=15)
        
        # Información
        info_y = panel_y + 40
        
        # Nivel
        level_text = f"NIVEL {self.current_level_number} COMPLETADO"
        level_surf = self.font_subtitle.render(level_text, True, YELLOW)
        self.screen.blit(level_surf, (title_x - level_surf.get_width()//2, info_y))
        
        # Dificultad
        diff_text = f"Dificultad: {self.settings['name']}"
        diff_surf = self.font_small.render(diff_text, True, self.settings['color'])
        self.screen.blit(diff_surf, (title_x - diff_surf.get_width()//2, info_y + 40))
        
        # Puntos
        if hasattr(self, 'level_complete_data'):
            data = self.level_complete_data
            points_y = info_y + 100
            
            # Puntos ganados
            points_text = f"Puntos ganados: +{data['points']}"
            points_surf = self.font_subtitle.render(points_text, True, GREEN)
            self.screen.blit(points_surf, (title_x - points_surf.get_width()//2, points_y))
            
            # Puntuación total
            if self.player:
                total_y = points_y + 50
                total_text = f"PUNTUACIÓN TOTAL: {self.player.score}"
                total_surf = self.font_subtitle.render(total_text, True, (255, 215, 0))
                self.screen.blit(total_surf, (title_x - total_surf.get_width()//2, total_y))
        
        # Controles
        controls_y = SCREEN_HEIGHT - 100
        
        if self.current_level_number < 3:
            next_text = "ENTER - SIGUIENTE NIVEL"
        else:
            next_text = "ENTER - ¡VICTORIA FINAL!"
        
        next_surf = self.font_hud.render(next_text, True, GREEN)
        self.screen.blit(next_surf, (title_x - next_surf.get_width()//2, controls_y))
    
    def draw_victory(self):
        for y in range(SCREEN_HEIGHT):
            color_factor = y / SCREEN_HEIGHT
            r = int(lerp(0, 50, color_factor))
            g = int(lerp(50, 150, color_factor))
            b = int(lerp(0, 50, color_factor))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        draw_text(self.screen, "¡VICTORIA!", SCREEN_WIDTH // 2, 100,
                 self.font_title, YELLOW, center=True)
        
        draw_text(self.screen, "Has completado todos los niveles",
                 SCREEN_WIDTH // 2, 180, self.font_subtitle, WHITE, center=True)
        
        if self.player:
            draw_text(self.screen, f"Puntuación Final: {self.player.score}",
                     SCREEN_WIDTH // 2, 260, self.font_subtitle, YELLOW, center=True)
        
        draw_text(self.screen, f"Dificultad: {self.settings['name']}",
                 SCREEN_WIDTH // 2, 320, self.font_subtitle, self.settings['color'], center=True)
        
        # Verificar si es nuevo récord
        if self.player and not self.is_new_high_score:
            self.is_new_high_score = self.is_high_score(self.player.score)
            if self.is_new_high_score:
                self.entering_name = True
        
        # Si está ingresando nombre
        if self.entering_name:
            draw_text(self.screen, "¡NUEVO RÉCORD!", SCREEN_WIDTH // 2, 370,
                     self.font_subtitle, (255, 215, 0), center=True)
            
            draw_text(self.screen, "Ingresa tus iniciales (3 letras):", SCREEN_WIDTH // 2, 420,
                     self.font_hud, WHITE, center=True)
            
            # Mostrar nombre actual con cursor parpadeante
            cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            name_display = self.player_name + cursor if len(self.player_name) < 3 else self.player_name
            draw_text(self.screen, name_display, SCREEN_WIDTH // 2, 470,
                     self.font_title, YELLOW, center=True)
            
            draw_text(self.screen, "ENTER - Guardar", SCREEN_WIDTH // 2, 540,
                     self.font_hud, GREEN, center=True)
        else:
            draw_text(self.screen, "ENTER - Jugar de Nuevo", SCREEN_WIDTH // 2, 400,
                     self.font_subtitle, GREEN, center=True)
            
            draw_text(self.screen, "Q - Volver al Menú", SCREEN_WIDTH // 2, 450,
                     self.font_subtitle, WHITE, center=True)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # F1 para salir del fullscreen
                if event.key == pygame.K_F1:
                    pygame.display.toggle_fullscreen()
                
                # M para silenciar/activar audio (funciona en cualquier estado)
                if event.key == pygame.K_m:
                    muted = toggle_mute()
                    print(f"[AUDIO] {'Silenciado' if muted else 'Activado'}")
                
                if self.state == STATE_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSED
                        self.lava.pause()
                    elif event.key == pygame.K_r:
                        self.start_level(self.current_level_number)
                
                elif self.state == STATE_PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_PLAYING
                        self.lava.resume()
                    elif event.key == pygame.K_r:
                        self.start_level(self.current_level_number)
                    elif event.key == pygame.K_q:
                        # Volver al menú principal
                        print("[DEBUG] Q presionada en PAUSED - volviendo al menú")
                        self.return_to_menu = True
                        self.running = False
                
                elif self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()  # Reiniciar completamente el juego
                    elif event.key == pygame.K_q:
                        # Volver al menú principal
                        print("[DEBUG] Q presionada en GAME_OVER - volviendo al menú")
                        self.return_to_menu = True
                        self.running = False
                
                elif self.state == STATE_LEVEL_COMPLETE:
                    if event.key == pygame.K_RETURN:
                        if self.current_level_number < 3:
                            self.start_level(self.current_level_number + 1)
                        else:
                            self.state = STATE_VICTORY
                
                elif self.state == STATE_VICTORY:
                    # Si está ingresando nombre para high score
                    if self.entering_name:
                        if event.key == pygame.K_RETURN and len(self.player_name) >= 1:
                            # Guardar puntuación
                            name = self.player_name if len(self.player_name) == 3 else self.player_name + "___"[:3-len(self.player_name)]
                            if self.player:
                                self.save_high_score(name, self.player.score)
                                print(f"[HighScore] Guardado: {name} - {self.player.score}")
                            self.entering_name = False
                            self.player_name = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif event.unicode.isalpha() and len(self.player_name) < 3:
                            self.player_name += event.unicode.upper()
                    else:
                        if event.key == pygame.K_RETURN:
                            self.reset_game()
                        elif event.key == pygame.K_q:
                            # Volver al menú principal
                            print("[DEBUG] Q presionada en VICTORY - volviendo al menú")
                            self.return_to_menu = True
                            self.running = False
    
    def reset_game(self):
        """Reinicia completamente el juego desde el nivel 1"""
        self.current_level_number = 1
        self.state = STATE_PLAYING
        
        # Resetear variables de high score
        self.player_name = ""
        self.entering_name = False
        self.is_new_high_score = False
        
        # Reiniciar tiempo
        self.start_time = time.time()
        self.elapsed_time = 0
        self.game_time = 0
        
        # Reiniciar lava
        self.lava = Lava(self.difficulty)
        
        # Comenzar nivel 1
        self.start_level(1)
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            
            # Si running se volvió False, salir del loop
            if not self.running:
                break
                
            self.update(dt)
            self.draw()
            
            pygame.display.flip()