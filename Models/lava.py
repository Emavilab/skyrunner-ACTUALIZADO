"""
lava.py - Sistema de Lava Dinámica

Este módulo implementa un sistema de lava ascendente con física realista,
efectos visuales dinámicos y mecánicas de presión progresiva.

Características principales:
- Lava ascendente que persigue al jugador
- Sistema de ondas procedurales con múltiples capas
- Partículas de lava, burbujas y humo
- Aceleración progresiva basada en altura ganada
- Sistema de "presión de escape" por inactividad
- Efectos visuales con pulsación de color y brillo
- Niveles de peligro dinámicos

Clases:
    Lava: Sistema principal de lava con física y renderizado

Autor: Proyecto SkyRunner
Fecha: 2025
"""

import pygame
import math
import random
from objects.constants import *
from objects.utils import lerp, clamp, sine_wave

class Lava:
    """
    Sistema de lava ascendente con física dinámica y efectos visuales.
    
    La lava persigue al jugador ascendiendo constantemente, acelerándose
    progresivamente según la altura ganada y aplicando presión cuando el
    jugador permanece estático. Incluye ondas procedurales, partículas,
    burbujas y efectos de humo.
    
    Attributes:
        difficulty (str): Nivel de dificultad ('easy', 'normal', 'hard')
        settings (dict): Configuración de dificultad desde constants
        y (float): Posición Y actual de la lava
        target_y (float): Posición Y objetivo (para interpolación suave)
        base_speed (float): Velocidad base de ascenso
        current_speed (float): Velocidad actual (con multiplicadores)
        acceleration (float): Aceleración por tiempo
        wave_time (float): Tiempo acumulado para animación de ondas
        wave_amplitude (float): Amplitud de las ondas superficiales
        escape_timer (float): Temporizador de presión por inactividad
        progress_multiplier (float): Multiplicador de velocidad por progreso
        particles (list): Lista de partículas de lava activas
        bubbles (list): Lista de burbujas en la superficie
        smoke_particles (list): Lista de partículas de humo
        is_paused (bool): Estado de pausa del sistema
        color_pulse (float): Factor de pulsación de color (0-1)
        glow_intensity (float): Intensidad del brillo (0-1)
        
    Methods:
        initialize(player_y): Inicializa la lava en posición relativa al jugador
        update(dt, player_y, player_rect, game_state): Actualiza física y partículas
        draw(surface, camera_offset): Renderiza la lava y sus efectos
        draw_hud(surface, player_y, player_rect): Dibuja HUD de información
        get_surface_y(x): Calcula altura de la superficie con ondas en X
        reset(player_y): Reinicia el sistema a valores iniciales
        pause(): Pausa el sistema
        resume(): Reanuda el sistema
    """
    def __init__(self, difficulty="normal"):
        """
        Inicializa el sistema de lava con la dificultad especificada.
        
        Configura todos los parámetros de física, velocidad, efectos visuales
        y sistemas de partículas según la dificultad seleccionada.
        
        Args:
            difficulty (str): Nivel de dificultad ('easy', 'normal', 'hard').
                             Afecta velocidad, aceleración y densidad de partículas.
        """
        # Configuración de dificultad
        self.difficulty = difficulty
        self.settings = DIFFICULTY_SETTINGS[difficulty]
        
        # Posición y movimiento
        self.y = SCREEN_HEIGHT  # Posición Y actual
        self.target_y = SCREEN_HEIGHT  # Posición objetivo (interpolación)
        self.base_speed = self.settings["lava_speed"]  # Velocidad base
        self.current_speed = self.base_speed  # Velocidad actual con multiplicadores
        self.acceleration = self.settings["lava_acceleration"]  # Aceleración por tiempo
        
        # Sistema de ondas superficiales
        self.wave_time = 0  # Tiempo para animación de ondas
        self.wave_amplitude = LAVA_CONFIG["wave_amplitude"]  # Altura de ondas
        self.wave_frequency = 0.5  # Frecuencia de ondas
        
        # Sistema de presión de escape (penaliza inactividad)
        self.escape_timer = 0  # Contador de tiempo estático
        self.escape_threshold = 5.0  # Segundos antes de activar presión
        self.escape_multiplier = 1.2  # Multiplicador cuando se activa
        
        # Sistema de aceleración progresiva
        self.progress_multiplier = 1.0  # Multiplicador por altura ganada
        self.last_player_y = SCREEN_HEIGHT  # Última posición del jugador
        
        # Sistemas de partículas
        self.particles = []  # Partículas de lava volando
        self.bubbles = []  # Burbujas en la superficie
        self.smoke_particles = []  # Humo cuando el jugador está cerca
        self.particle_timer = 0  # Temporizador de generación
        
        # Estados del sistema
        self.is_paused = False  # Pausa el sistema
        self.initialized = False  # Indica si se inicializó la posición
        
        # Efectos visuales
        self.color_pulse = 0  # Pulsación de color (0-1)
        self.glow_intensity = 0  # Intensidad del brillo (0-1)
        
        # Información de depuración
        self.debug_info = {
            "speed": 0,
            "acceleration": 0,
            "distance_to_player": 0,
            "danger_level": 0
        }
    
    def initialize(self, player_y):
        """
        Inicializa la posición de la lava relativa al jugador.
        
        Coloca la lava 500 píxeles debajo del jugador al inicio del nivel
        y marca el sistema como inicializado.
        
        Args:
            player_y (float): Posición Y actual del jugador.
        """
        self.y = player_y + 500
        self.target_y = self.y
        self.last_player_y = player_y
        self.initialized = True
    
    def update(self, dt, player_y, player_rect, game_state):
        """
        Actualiza la física, movimiento y efectos de la lava.
        
        Este método maneja:
        - Animación de ondas superficiales
        - Aceleración progresiva por altura ganada
        - Sistema de presión de escape por inactividad
        - Generación y actualización de partículas/burbujas
        - Detección de colisiones con el jugador
        
        Args:
            dt (float): Delta time en segundos desde el último frame.
            player_y (float): Posición Y actual del jugador.
            player_rect (pygame.Rect): Rectángulo de colisión del jugador.
            game_state (str): Estado actual del juego (playing, paused, etc.).
            
        Returns:
            bool: True si la lava tocó al jugador, False en caso contrario.
        """
        if not self.initialized or self.is_paused:
            return False
        
        # Actualizar animación de ondas y pulsación de color
        self.wave_time += dt
        self.color_pulse = (math.sin(self.wave_time * 3) + 1) / 2
        
        self._update_progress_acceleration(player_y)
        self._update_escape_pressure(player_y, dt)
        
        self.current_speed = self.base_speed * self.progress_multiplier
        
        if self.difficulty == "hard":
            self.current_speed += self.acceleration * self.wave_time
        
        if self.escape_timer > self.escape_threshold:
            self.current_speed *= self.escape_multiplier
        
        target_movement = self.current_speed * dt * 60
        self.target_y -= target_movement
        
        self.y = lerp(self.y, self.target_y, 0.1)
        self.y = min(self.y, self.target_y)
        
        self._generate_particles(dt, player_y)
        self._update_particles(dt)
        self._update_bubbles(dt)
        
        distance = player_y - self.get_surface_y(player_rect.centerx)
        if 0 < distance < 200:
            self._generate_smoke(player_rect.centerx, player_y, dt)
        
        self._update_debug_info(player_y, distance)
        
        return self._check_collision(player_rect, distance)
    
    def _update_progress_acceleration(self, player_y):
        """
        Actualiza el multiplicador de velocidad basado en la altura ganada.
        
        Aumenta progresivamente la velocidad de la lava a medida que el
        jugador asciende, incentivando mantener un ritmo constante.
        El multiplicador está limitado entre 1.0x y 2.0x.
        
        Args:
            player_y (float): Posición Y actual del jugador.
        """
        height_gained = max(0, self.last_player_y - player_y)
        
        if height_gained > 0:
            self.progress_multiplier += height_gained * 0.0001
            self.progress_multiplier = clamp(self.progress_multiplier, 1.0, 2.0)
        
        self.last_player_y = player_y
    
    def _update_escape_pressure(self, player_y, dt):
        """
        Actualiza el sistema de presión de escape por inactividad.
        
        Si el jugador se mueve menos de 10 píxeles, incrementa un temporizador.
        Cuando el temporizador supera el umbral, la lava acelera para forzar
        movimiento. Se resetea cuando el jugador se mueve activamente.
        
        Args:
            player_y (float): Posición Y actual del jugador.
            dt (float): Delta time en segundos.
        """
        distance_moved = abs(player_y - self.last_player_y)
        
        if distance_moved < 10:
            self.escape_timer += dt
        else:
            self.escape_timer = max(0, self.escape_timer - dt * 2)
    
    def _update_debug_info(self, player_y, distance):
        self.debug_info = {
            "speed": round(self.current_speed, 2),
            "acceleration": round(self.acceleration, 4),
            "distance_to_player": int(distance) if distance > 0 else 0,
            "danger_level": self._calculate_danger_level(distance),
            "escape_timer": round(self.escape_timer, 1)
        }
    
    def _calculate_danger_level(self, distance):
        if distance <= 0:
            return 100
        elif distance < 100:
            return 90 - (distance / 100) * 40
        elif distance < 300:
            return 50 - ((distance - 100) / 200) * 40
        else:
            return max(10, 100 - (distance / 10))
    
    def _generate_particles(self, dt, player_y):
        self.particle_timer += dt
        
        density = LAVA_CONFIG["particle_density"] * (2 if self.difficulty == "hard" else 1)
        
        if self.particle_timer > 1.0 / density:
            for _ in range(random.randint(1, 3)):
                x = random.randint(50, SCREEN_WIDTH - 50)
                surface_y = self.get_surface_y(x)
                
                if abs(surface_y - player_y) < 500:
                    self.particles.append({
                        'x': x,
                        'y': surface_y,
                        'vx': random.uniform(-0.5, 0.5),
                        'vy': random.uniform(-3, -1),
                        'life': random.uniform(0.5, 1.5),
                        'size': random.randint(2, 5),
                        'color': random.choice([
                            LAVA_CONFIG["colors"]["surface"],
                            LAVA_CONFIG["colors"]["glow"],
                            (255, 200, 50)
                        ])
                    })
            
            self.particle_timer = 0
            
            if random.random() < 0.3:
                self._generate_bubble()
    
    def _generate_bubble(self):
        x = random.randint(100, SCREEN_WIDTH - 100)
        surface_y = self.get_surface_y(x)
        
        self.bubbles.append({
            'x': x,
            'y': surface_y,
            'radius': random.uniform(3, 8),
            'growth_speed': random.uniform(0.5, 1.5),
            'max_radius': random.uniform(10, 20),
            'life': random.uniform(1.0, 2.0),
            'color': (255, 255, 255, 100)
        })
    
    def _generate_smoke(self, x, player_y, dt):
        if random.random() < 0.1:
            smoke_y = self.get_surface_y(x) - 10
            
            self.smoke_particles.append({
                'x': x + random.randint(-20, 20),
                'y': smoke_y,
                'vx': random.uniform(-0.2, 0.2),
                'vy': random.uniform(-1.5, -0.5),
                'life': random.uniform(1.0, 2.0),
                'size': random.randint(3, 8),
                'color': (100, 100, 100, 150)
            })
    
    def _update_particles(self, dt):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= dt
            p['vy'] -= 0.1
            
            if p['life'] <= 0 or p['y'] < -50:
                self.particles.remove(p)
        
        for s in self.smoke_particles[:]:
            s['x'] += s['vx']
            s['y'] += s['vy']
            s['life'] -= dt
            s['size'] += 0.5
            
            if s['life'] <= 0 or s['y'] < -50:
                self.smoke_particles.remove(s)
    
    def _update_bubbles(self, dt):
        for b in self.bubbles[:]:
            b['radius'] += b['growth_speed'] * dt
            b['life'] -= dt
            b['y'] -= 0.5
            
            if b['life'] <= 0 or b['radius'] >= b['max_radius']:
                self._explode_bubble(b)
                self.bubbles.remove(b)
    
    def _explode_bubble(self, bubble):
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            
            self.particles.append({
                'x': bubble['x'],
                'y': bubble['y'],
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.3, 0.8),
                'size': random.randint(1, 3),
                'color': LAVA_CONFIG["colors"]["glow"]
            })
    
    def get_surface_y(self, x):
        """
        Calcula la altura de la superficie de lava en una posición X específica.
        
        Combina tres ondas sinusoidales con diferentes frecuencias y amplitudes
        para crear un efecto de oleaje realista y dinámico.
        
        Ondas:
        - wave1: Onda principal (frecuencia media, amplitud completa)
        - wave2: Onda secundaria (frecuencia alta, 50% amplitud)
        - wave3: Onda de fondo (frecuencia baja, 30% amplitud)
        
        Args:
            x (float): Posición horizontal donde calcular la altura.
            
        Returns:
            float: Altura Y de la superficie en la posición X dada.
        """
        wave1 = math.sin(x * 0.02 + self.wave_time * 2) * self.wave_amplitude
        wave2 = math.sin(x * 0.05 + self.wave_time * 1.5) * (self.wave_amplitude * 0.5)
        wave3 = math.sin(x * 0.01 + self.wave_time * 0.8) * (self.wave_amplitude * 0.3)
        
        return self.y + wave1 + wave2 + wave3
    
    def _check_collision(self, player_rect, distance):
        if distance <= 0:
            player_bottom = player_rect.bottom
            lava_surface = self.get_surface_y(player_rect.centerx)
            
            if player_bottom >= lava_surface - 5:
                return True
        
        return False
    
    def accelerate(self, multiplier=1.1):
        self.current_speed *= multiplier
        self.glow_intensity = min(1.0, self.glow_intensity + 0.3)
    
    def reset(self, player_y):
        """
        Reinicia el sistema de lava a su estado inicial.
        
        Restablece posición, velocidad, multiplicadores, temporizadores
        y limpia todas las partículas activas. Usado al reiniciar nivel
        o cuando el jugador pierde una vida.
        
        Args:
            player_y (float): Nueva posición Y del jugador para reposicionar lava.
        """
        self.y = player_y + 500
        self.target_y = self.y
        self.current_speed = self.base_speed
        self.progress_multiplier = 1.0
        self.escape_timer = 0
        self.wave_time = 0
        self.particles.clear()
        self.bubbles.clear()
        self.smoke_particles.clear()
    
    def pause(self):
        self.is_paused = True
    
    def resume(self):
        self.is_paused = False
    
    def draw(self, surface, camera_offset):
        """
        Renderiza la lava y todos sus efectos visuales.
        
        Dibuja múltiples capas:
        1. Capa profunda (lava oscura del fondo)
        2. Capa media (transición de color)
        3. Superficie con ondas procedurales
        4. Línea de brillo en las crestas
        5. Burbujas con transparencia
        6. Partículas de lava volando
        7. Partículas de humo
        
        Aplica pulsación de color y efectos de brillo dinámicos.
        
        Args:
            surface (pygame.Surface): Superficie donde dibujar.
            camera_offset (float): Offset Y de la cámara para scroll.
        """
        screen_y = self.y - camera_offset
        
        # Culling: no dibujar si está completamente fuera de pantalla
        if screen_y > SCREEN_HEIGHT + 100:
            return
        
        pulse_factor = 0.8 + self.color_pulse * 0.2
        glow_factor = 0.5 + self.glow_intensity * 0.5
        
        base_surface = tuple(int(c * pulse_factor) for c in LAVA_CONFIG["colors"]["surface"])
        base_middle = tuple(int(c * pulse_factor) for c in LAVA_CONFIG["colors"]["middle"])
        base_deep = tuple(int(c * pulse_factor) for c in LAVA_CONFIG["colors"]["deep"])
        glow_color = tuple(int(c * glow_factor) for c in LAVA_CONFIG["colors"]["glow"])
        
        deep_height = LAVA_CONFIG["height"] - 20
        if screen_y + deep_height > 0:
            deep_rect = pygame.Rect(0, screen_y + 20, SCREEN_WIDTH, deep_height)
            pygame.draw.rect(surface, base_deep, deep_rect)
        
        if screen_y + 10 > 0:
            mid_rect = pygame.Rect(0, screen_y + 10, SCREEN_WIDTH, 10)
            pygame.draw.rect(surface, base_middle, mid_rect)
        
        surface_points = []
        step = 20
        
        for x in range(0, SCREEN_WIDTH + step, step):
            wave_y = self.get_surface_y(x) - camera_offset
            surface_points.append((x, wave_y))
        
        surface_points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface_points.append((0, SCREEN_HEIGHT))
        
        pygame.draw.polygon(surface, base_surface, surface_points)
        
        if len(surface_points) > 2:
            crest_points = [(x, y - 2) for x, y in surface_points[:-2]]
            pygame.draw.lines(surface, glow_color, False, crest_points, 2)
        
        for bubble in self.bubbles:
            bubble_y = bubble['y'] - camera_offset
            if 0 < bubble_y < SCREEN_HEIGHT:
                alpha = int(255 * (bubble['life'] / 2.0))
                color = (*bubble['color'][:3], alpha)
                
                bubble_surf = pygame.Surface((int(bubble['radius']*2), int(bubble['radius']*2)), 
                                            pygame.SRCALPHA)
                pygame.draw.circle(bubble_surf, color,
                                 (int(bubble['radius']), int(bubble['radius'])), 
                                 int(bubble['radius']))
                surface.blit(bubble_surf, 
                           (int(bubble['x'] - bubble['radius']), 
                            int(bubble_y - bubble['radius'])))
        
        for p in self.particles:
            particle_y = p['y'] - camera_offset
            if 0 < particle_y < SCREEN_HEIGHT:
                alpha = int(255 * (p['life'] / 1.5))
                color = (*p['color'][:3], alpha)
                
                particle_surf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surf, color,
                                 (p['size'], p['size']), p['size'])
                surface.blit(particle_surf, 
                           (int(p['x'] - p['size']), int(particle_y - p['size'])))
        
        for s in self.smoke_particles:
            smoke_y = s['y'] - camera_offset
            if 0 < smoke_y < SCREEN_HEIGHT:
                alpha = int(150 * (s['life'] / 2.0))
                color = (*s['color'][:3], alpha)
                
                smoke_surf = pygame.Surface((s['size']*2, s['size']*2), pygame.SRCALPHA)
                pygame.draw.circle(smoke_surf, color,
                                 (s['size'], s['size']), s['size'])
                surface.blit(smoke_surf, 
                           (int(s['x'] - s['size']), int(smoke_y - s['size'])))
        
        if self.glow_intensity > 0:
            self.glow_intensity = max(0, self.glow_intensity - 0.02)
    
    def draw_hud(self, surface, player_y, player_rect):
        font = pygame.font.Font(None, FONT_SIZE_SMALL)
        small_font = pygame.font.Font(None, 18)
        
        distance = max(0, player_y - self.get_surface_y(player_rect.centerx))
        
        danger_color = GREEN
        if distance < 300:
            danger_color = YELLOW
        if distance < 100:
            danger_color = RED
        
        panel_x = SCREEN_WIDTH - 180
        panel_y = 100
        panel_width = 170
        panel_height = 120
        
        pygame.draw.rect(surface, (0, 0, 0, 180),
                        (panel_x, panel_y, panel_width, panel_height), border_radius=5)
        pygame.draw.rect(surface, WHITE,
                        (panel_x, panel_y, panel_width, panel_height), 2, border_radius=5)
        
        title = font.render("🌋 SISTEMA DE LAVA", True, YELLOW)
        surface.blit(title, (panel_x + 10, panel_y + 10))
        
        dist_text = small_font.render(f"Distancia: {int(distance)}px", True, WHITE)
        surface.blit(dist_text, (panel_x + 10, panel_y + 40))
        
        danger_level = self._calculate_danger_level(distance)
        danger_text = small_font.render(f"Peligro: {int(danger_level)}%", True, danger_color)
        surface.blit(danger_text, (panel_x + 10, panel_y + 60))
        
        speed_text = small_font.render(f"Velocidad: {self.current_speed:.1f}x", True, WHITE)
        surface.blit(speed_text, (panel_x + 10, panel_y + 80))
        
        if self.escape_timer > self.escape_threshold:
            escape_text = small_font.render("¡PRESIÓN DE ESCAPE!", True, RED)
            surface.blit(escape_text, (panel_x + 10, panel_y + 100))
        
        bar_width = 150
        bar_height = 8
        bar_x = panel_x + 10
        bar_y = panel_y + 125
        
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        danger_width = int((danger_level / 100) * bar_width)
        pygame.draw.rect(surface, danger_color, (bar_x, bar_y, danger_width, bar_height))
        
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)