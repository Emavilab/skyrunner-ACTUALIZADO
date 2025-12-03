"""
enemies.py - Clases de Enemigos COMPLETAS
"""

import pygame
import math
import random
from objects.constants import *
from objects.utils import sine_wave



class Enemy:
    """Clase base para todos los enemigos"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True
        self.damage = 20  # Daño base para todos los enemigos
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        raise NotImplementedError("Subclases deben implementar get_rect()")
    
    def update(self, dt):
        """Actualiza el enemigo"""
        raise NotImplementedError("Subclases deben implementar update()")
    
    def draw(self, surface, camera_offset):
        """Dibuja el enemigo"""
        raise NotImplementedError("Subclases deben implementar draw()")


class Bat(Enemy):
    """
    Murciélago que patrulla en trayectoria sinusoidal.
    Implementa movimiento sinusoidal y rotación.
    """
    
    def __init__(self, x, y, patrol_range=150):
        super().__init__(x, y)
        self.start_x = x
        self.start_y = y
        self.patrol_range = patrol_range
        self.speed = BAT_SPEED
        self.time = random.uniform(0, 2 * math.pi)
        self.direction = random.choice([-1, 1])
        
        # Dimensiones
        self.width = BAT_WIDTH
        self.height = BAT_HEIGHT
        
        # Rotación (transformación)
        self.angle = 0
        self.rotation_speed = 2

        self.damage = 15  # Daño específico para murciélago
    
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2,
                          self.width, self.height)
    
    def update(self, dt):
        """
        Actualiza posición del murciélago.
        Movimiento sinusoidal: y = A * sin(ωt + φ)
        """
        self.time += dt
        
        # Movimiento horizontal
        self.x += self.speed * self.direction * dt * 60  # Multiplicar por dt*60
        
        # Cambiar dirección al llegar al límite
        if abs(self.x - self.start_x) > self.patrol_range:
            self.direction *= -1
        
        # Movimiento vertical sinusoidal
        self.y = self.start_y + sine_wave(self.time, BAT_AMPLITUDE, 2)
        
        # Actualizar rotación
        self.angle += self.rotation_speed * dt * 60
        if self.angle >= 360:
            self.angle -= 360
    
    def draw(self, surface, camera_offset):
        """Dibuja el murciélago con rotación"""
        screen_y = self.y - camera_offset
        
        # Si está fuera de pantalla, no dibujar
        if screen_y < -50 or screen_y > SCREEN_HEIGHT + 50:
            return
        
        # Color del murciélago
        color = (100, 50, 150)  # Púrpura oscuro
        
        # Crear superficie para rotar
        bat_surface = pygame.Surface((self.width, self.height), 
                                     pygame.SRCALPHA)
        
        # Dibujar cuerpo del murciélago
        # Cuerpo central
        pygame.draw.ellipse(bat_surface, color,
                           (5, 10, self.width-10, self.height-10))
        
        # Alas (triángulos)
        # Ala izquierda
        pygame.draw.polygon(bat_surface, color,
                           [(5, 15), (0, 25), (10, 20)])
        # Ala derecha
        pygame.draw.polygon(bat_surface, color,
                           [(self.width-5, 15), (self.width, 25), 
                            (self.width-10, 20)])
        
        # Aplicar transformación de rotación
        rotated_surface = pygame.transform.rotate(bat_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x, screen_y))
        
        surface.blit(rotated_surface, rotated_rect)


class RotatingTrap(Enemy):
    """
    Trampa rotante que gira constantemente.
    Implementa transformación de rotación continua.
    """
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = TRAP_SIZE
        self.angle = 0
        self.rotation_speed = TRAP_ROTATION_SPEED
        self.damage = 25  # Daño específico para trampa
    
    def get_rect(self):
        # Usar un área circular para colisión más precisa
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2,
                          self.size, self.size)
    
    def update(self, dt):
        """Actualiza la rotación de la trampa"""
        # Aplicar rotación constante
        self.angle += self.rotation_speed * dt * 60  # Multiplicar por dt*60
        if self.angle >= 360:
            self.angle -= 360
    
    def draw(self, surface, camera_offset):
        """Dibuja la trampa con rotación"""
        screen_y = self.y - camera_offset
        
        if screen_y < -50 or screen_y > SCREEN_HEIGHT + 50:
            return
        
        # Crear superficie para la trampa
        trap_surface = pygame.Surface((self.size * 2, self.size * 2), 
                                      pygame.SRCALPHA)
        center = self.size
        
        # Dibujar estrella de púas
        num_spikes = 8
        outer_radius = self.size
        inner_radius = self.size // 2
        
        points = []
        for i in range(num_spikes * 2):
            angle = math.radians(i * 180 / num_spikes)
            if i % 2 == 0:
                # Punta externa
                px = center + outer_radius * math.cos(angle)
                py = center + outer_radius * math.sin(angle)
            else:
                # Punta interna
                px = center + inner_radius * math.cos(angle)
                py = center + inner_radius * math.sin(angle)
            points.append((px, py))
        
        pygame.draw.polygon(trap_surface, RED, points)
        pygame.draw.polygon(trap_surface, (150, 0, 0), points, 3)
        
        # Aplicar transformación de rotación
        rotated_surface = pygame.transform.rotate(trap_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x, screen_y))
        
        surface.blit(rotated_surface, rotated_rect)


class FallingRock(Enemy):
    """
    Roca que cae aplicando física de gravedad.
    Implementa traslación vertical con aceleración.
    """
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = ROCK_SIZE
        self.vel_y = 0
        self.gravity = 2.0  # GRAVEDAD REDUCIDA para caída más lenta
        self.rotation_angle = random.uniform(0, 360)
        self.rotation_vel = random.uniform(-3, 3)  # REDUCIDO para rotación más lenta
        self.damage = 30  # Daño específico para roca
        self.active = True
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2,
                          self.size, self.size)
    
    def update(self, dt):
        """Actualiza la caída de la roca con física REDUCIDA"""
        # Aplicar gravedad REDUCIDA
        self.vel_y += self.gravity * dt * 60  # Multiplicar por dt*60 para suavizar
        
        # Limitar velocidad máxima
        max_speed = 15.0
        if self.vel_y > max_speed:
            self.vel_y = max_speed
        
        # Aplicar traslación vertical
        self.y += self.vel_y * dt * 60
        
        # Rotación mientras cae (más lenta)
        self.rotation_angle += self.rotation_vel * dt * 60
        
        # Desactivar si cae fuera de la pantalla
        if self.y > SCREEN_HEIGHT + 200:  # Más margen
            self.active = False
    
    def draw(self, surface, camera_offset):
        """Dibuja la roca"""
        screen_y = self.y - camera_offset
        
        if screen_y < -50 or screen_y > SCREEN_HEIGHT + 50:
            return
        
        # Crear superficie para la roca
        rock_surface = pygame.Surface((self.size, self.size), 
                                      pygame.SRCALPHA)
        
        # Dibujar roca irregular (polígono)
        points = [
            (self.size * 0.5, self.size * 0.1),
            (self.size * 0.9, self.size * 0.3),
            (self.size * 0.8, self.size * 0.7),
            (self.size * 0.5, self.size * 0.9),
            (self.size * 0.2, self.size * 0.7),
            (self.size * 0.1, self.size * 0.3)
        ]
        
        pygame.draw.polygon(rock_surface, GRAY, points)
        pygame.draw.polygon(rock_surface, (80, 80, 80), points, 2)
        
        # Aplicar rotación
        rotated_surface = pygame.transform.rotate(rock_surface, 
                                                  self.rotation_angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x, screen_y))
        
        surface.blit(rotated_surface, rotated_rect)


class Lightning(Enemy):
    """
    Rayo eléctrico que aparece aleatoriamente.
    Exclusivo del nivel 3 (Tormenta).
    """
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = LIGHTNING_WIDTH
        self.height = LIGHTNING_HEIGHT
        self.lifetime = 0.5  # Segundos que permanece visible
        self.time = 0
        self.warning_time = 0.3  # Tiempo de advertencia antes de aparecer
        self.warned = False
        self.damage = 35  # Daño específico para rayo
        
        # Animación
        self.flicker_time = 0
        self.visible = True
    
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y,
                          self.width, self.height)
    
    def update(self, dt):
        """Actualiza el rayo"""
        self.time += dt
        self.flicker_time += dt
        
        # Advertencia (mostrar indicador)
        if self.time < self.warning_time:
            self.warned = True
        else:
            self.warned = False
        
        # Parpadeo del rayo
        if self.flicker_time > 0.05:
            self.visible = not self.visible
            self.flicker_time = 0
        
        # Desactivar después de lifetime
        if self.time > self.lifetime + self.warning_time:
            self.active = False
    
    def draw(self, surface, camera_offset):
        """Dibuja el rayo eléctrico"""
        screen_y = self.y - camera_offset
        
        if screen_y < -100 or screen_y > SCREEN_HEIGHT + 100:
            return
        
        # Mostrar advertencia
        if self.warned:
            # Línea roja parpadeante de advertencia
            if int(self.time * 20) % 2 == 0:
                pygame.draw.line(surface, RED,
                               (self.x, screen_y),
                               (self.x, screen_y + self.height), 2)
        else:
            # Dibujar rayo si está visible
            if self.visible:
                # Rayo en zigzag
                points = [(self.x, screen_y)]
                segments = 10
                for i in range(1, segments):
                    offset = random.randint(-self.width//2, self.width//2)
                    y = screen_y + (self.height / segments) * i
                    points.append((self.x + offset, y))
                points.append((self.x, screen_y + self.height))
                
                # Dibujar rayo
                pygame.draw.lines(surface, YELLOW, False, points, 4)
                pygame.draw.lines(surface, WHITE, False, points, 2)


class SurveillanceDrone(Enemy):
    """
    Dron de vigilancia que patrulla un área.
    Detecta al jugador y lo persigue.
    """
    
    def __init__(self, x, y, patrol_range=150, detection_range=200):
        super().__init__(x, y)
        self.start_x = x
        self.start_y = y
        self.patrol_range = patrol_range
        self.detection_range = detection_range
        self.speed = 1.5
        self.direction = 1
        self.width = 40
        self.height = 30
        self.damage = 20  # Daño específico para dron
        
        # Estados
        self.patrolling = True
        self.chasing = False
        self.target_x = None
        self.target_y = None
        
        # Animación
        self.frame = 0
        self.animation_speed = 0.1
        self.frame_timer = 0
        self.propeller_angle = 0
        
        # Cargar sprite o crear uno simple
        try:
            self.sprite = pygame.image.load("./Assets/Enemies/drone.png").convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
        except:
            self.create_simple_sprite()
    
    def create_simple_sprite(self):
        """Crea un sprite simple si no hay imagen"""
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Cuerpo del dron
        pygame.draw.ellipse(surf, (80, 80, 100), 
                           (0, 0, self.width, self.height))
        # Ojos/sensor
        pygame.draw.circle(surf, (255, 0, 0), 
                          (self.width//2, self.height//2), 6)
        # Detalles
        pygame.draw.ellipse(surf, (60, 60, 80), 
                           (5, 5, self.width-10, self.height-10), 2)
        self.sprite = surf
    
    def update(self, dt, player_pos=None):
        """Actualiza el dron con detección del jugador"""
        self.frame_timer += dt
        
        # Animación de hélices
        self.propeller_angle = (self.propeller_angle + 10 * dt * 60) % 360
        
        # Detectar jugador
        if player_pos and self._detect_player(player_pos):
            self.chasing = True
            self.patrolling = False
            self.target_x, self.target_y = player_pos
        else:
            self.chasing = False
            self.patrolling = True
        
        # Movimiento según estado
        if self.chasing and self.target_x:
            # Perseguir al jugador
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Moverse hacia el objetivo
                self.x += (dx / distance) * self.speed * 1.5 * dt * 60
                self.y += (dy / distance) * self.speed * 1.5 * dt * 60
        else:
            # Patrullar
            self.x += self.speed * self.direction * dt * 60
            
            # Cambiar dirección al llegar al límite
            if abs(self.x - self.start_x) > self.patrol_range:
                self.direction *= -1
        
        # Actualizar frame de animación
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.frame = (self.frame + 1) % 4
    
    def _detect_player(self, player_pos):
        """Verifica si el jugador está en rango de detección"""
        px, py = player_pos
        distance = math.sqrt((px - self.x)**2 + (py - self.y)**2)
        return distance < self.detection_range
    
    def get_rect(self):
        """Retorna rectángulo de colisión"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2,
                          self.width, self.height)
    
    def draw(self, surface, camera_offset):
        """Dibuja el dron con efectos"""
        screen_y = self.y - camera_offset
        screen_x = self.x
        
        # Solo dibujar si está en pantalla
        if screen_y < -50 or screen_y > SCREEN_HEIGHT + 50:
            return
        
        # Dibujar sprite base
        draw_x = screen_x - self.width//2
        draw_y = screen_y - self.height//2
        surface.blit(self.sprite, (draw_x, draw_y))
        
        # Dibujar hélices rotantes
        prop_color = (150, 150, 150)
        prop_length = 15
        
        # Hélices en ángulo
        for angle_offset in [0, 90]:
            angle = self.propeller_angle + angle_offset
            radians = math.radians(angle)
            
            x1 = screen_x + math.cos(radians) * prop_length
            y1 = screen_y + math.sin(radians) * prop_length
            x2 = screen_x - math.cos(radians) * prop_length
            y2 = screen_y - math.sin(radians) * prop_length
            
            pygame.draw.line(surface, prop_color, 
                           (x1, y1), (x2, y2), 3)
        
        # Luz de vigilancia si está en modo alerta
        if self.chasing:
            light_color = (255, 50, 50, 100)
            light_surf = pygame.Surface((self.detection_range*2, 40), pygame.SRCALPHA)
            pygame.draw.ellipse(light_surf, light_color, 
                               (0, 0, self.detection_range*2, 40))
            light_x = self.x - self.detection_range
            surface.blit(light_surf, (light_x, screen_y))


# ============================================
# 🎮 FACTORY PARA CREAR ENEMIGOS
# ============================================

def create_enemy(enemy_type, x, y, **kwargs):
    """
    Factory para crear enemigos dinámicamente.
    
    Args:
        enemy_type: Tipo de enemigo ('bat', 'trap', 'rock', 'lightning', 'drone')
        x, y: Posición inicial
        **kwargs: Parámetros específicos para cada tipo
    """
    enemies = {
        'bat': Bat,
        'trap': RotatingTrap,
        'rock': FallingRock,
        'lightning': Lightning,
        'drone': SurveillanceDrone
    }
    
    if enemy_type in enemies:
        return enemies[enemy_type](x, y, **kwargs)
    else:
        raise ValueError(f"Tipo de enemigo desconocido: {enemy_type}")


# ============================================
# 🧪 EJEMPLO DE USO (para pruebas)
# ============================================

def test_enemies():
    """Función para probar todos los enemigos"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Crear un ejemplo de cada enemigo
    enemies = [
        Bat(200, 300),
        RotatingTrap(400, 300),
        FallingRock(600, 100),
        Lightning(300, 200),
        SurveillanceDrone(500, 400, patrol_range=100)
    ]
    
    running = True
    camera_offset = 0
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Actualizar enemigos
        for enemy in enemies:
            if hasattr(enemy, 'update'):
                enemy.update(dt)
        
        # Dibujar
        screen.fill((50, 50, 50))
        for enemy in enemies:
            if hasattr(enemy, 'draw'):
                enemy.draw(screen, camera_offset)
        
        pygame.display.flip()
    
    pygame.quit()

# Para probar: python -m enemies
if __name__ == "__main__":
    test_enemies()