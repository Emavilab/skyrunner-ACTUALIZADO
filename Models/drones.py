"""
drones.py - Drones inteligentes con visión computacional
VERSIÓN CORREGIDA Y FUNCIONAL
"""

import pygame
import math
import random
from objects.constants import *

class SurveillanceDrone:
    """Dron que detecta al jugador y cambia su patrón"""
    
    def __init__(self, x, y, detection_range=300):
        self.x = x
        self.y = y
        self.width = 60  # Aumentado para mejor visibilidad
        self.height = 40  # Aumentado para mejor visibilidad
        self.speed = 2.0
        self.angle = 0
        self.active = True
        self.damage = 25  # Daño del dron
        
        # CARGAR IMAGEN DEL DRON
        self.image = self.load_drone_image()
        self.original_image = self.image.copy() if self.image else None
        
        # Visión computacional simulada
        self.detection_range = detection_range
        self.player_detected = False
        self.detection_timer = 0
        self.detection_cooldown = 1.0
        
        # Patrones de movimiento
        self.pattern = "hover"  # hover, patrol, chase, evade
        self.patrol_points = []
        self.current_patrol_index = 0
        self.generate_patrol_points()
        
        # Efectos visuales
        self.scan_angle = 0
        self.laser_active = False
        self.laser_target = (x, y)
        self.particles = []
        
        # Para seguir al jugador
        self.player_positions = []
        self.predicted_position = (x, y)
        
        print(f"[Drone] Creado en ({x}, {y}) con imagen: {'Sí' if self.image else 'No'}")
    
    def load_drone_image(self):
        """Carga la imagen del dron o crea una por defecto"""
        try:
            # Intenta cargar la imagen
            image_path = "./Assets/Enemies/drone.png"
            print(f"[Drone] Intentando cargar: {image_path}")
            
            image = pygame.image.load(image_path).convert_alpha()
            print(f"[Drone] Imagen cargada: {image.get_width()}x{image.get_height()}")
            
            # Escalar al tamaño correcto
            scaled_image = pygame.transform.scale(image, (self.width, self.height))
            print(f"[Drone] Imagen escalada a: {self.width}x{self.height}")
            return scaled_image
            
        except Exception as e:
            print(f"[Drone] No se pudo cargar drone.png: {e}")
            print(f"[Drone] Creando imagen por defecto...")
            
            # Crear imagen por defecto
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # Cuerpo del dron (elipse)
            pygame.draw.ellipse(surf, (50, 150, 255), 
                              (0, 0, self.width, self.height))
            
            # Detalles del dron
            pygame.draw.ellipse(surf, (30, 100, 200), 
                              (5, 5, self.width-10, self.height-10), 2)
            
            # "Ojos" del dron
            pygame.draw.circle(surf, (255, 0, 0), 
                             (self.width//3, self.height//2), 4)
            pygame.draw.circle(surf, (255, 0, 0), 
                             (2*self.width//3, self.height//2), 4)
            
            # Línea central
            pygame.draw.line(surf, (255, 255, 255), 
                           (self.width//2, 5), 
                           (self.width//2, self.height-5), 1)
            
            return surf
    
    def generate_patrol_points(self):
        """Genera puntos de patrulla aleatorios"""
        for _ in range(4):
            px = self.x + random.randint(-200, 200)
            py = self.y + random.randint(-100, 100)
            self.patrol_points.append((px, py))
        print(f"[Drone] Puntos de patrulla: {self.patrol_points}")
    
    def update(self, dt, player_pos=None):
        """Actualiza dron con IA"""
        self.angle += dt * 2  # Rotación constante
        
        # Actualizar temporizador de detección
        if self.detection_timer > 0:
            self.detection_timer -= dt
        
        # "Detectar" jugador
        if player_pos and self.detection_timer <= 0:
            px, py = player_pos
            distance = math.sqrt((self.x - px)**2 + (self.y - py)**2)
            
            if distance < self.detection_range:
                self.player_detected = True
                self.detection_timer = self.detection_cooldown
                
                # Guardar posición del jugador
                self.player_positions.append(player_pos)
                if len(self.player_positions) > 10:
                    self.player_positions.pop(0)
                
                # Predecir posición futura
                if len(self.player_positions) >= 2:
                    last_pos = self.player_positions[-1]
                    second_last = self.player_positions[-2]
                    dx = last_pos[0] - second_last[0]
                    dy = last_pos[1] - second_last[1]
                    self.predicted_position = (last_pos[0] + dx*2, last_pos[1] + dy*2)
                
                # Cambiar patrón según distancia
                if distance < 150:
                    self.pattern = "evade"
                    self.speed = 3.0
                else:
                    self.pattern = "chase"
                    self.speed = 2.5
            else:
                self.player_detected = False
                self.pattern = "patrol" if len(self.patrol_points) > 0 else "hover"
                self.speed = 2.0
        
        # Ejecutar patrón actual
        if self.pattern == "hover":
            # Movimiento flotante suave
            self.y += math.sin(pygame.time.get_ticks() * 0.001) * 0.5
            
        elif self.pattern == "patrol" and self.patrol_points:
            # Patrullar entre puntos
            target = self.patrol_points[self.current_patrol_index]
            dx = target[0] - self.x
            dy = target[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < 10:
                self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
            else:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                
        elif self.pattern == "chase" and self.player_detected:
            # Perseguir al jugador
            target = self.predicted_position
            dx = target[0] - self.x
            dy = target[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                
                # Activar láser al estar cerca
                if distance < 100:
                    self.laser_active = True
                    self.laser_target = (target[0] + random.randint(-20, 20),
                                       target[1] + random.randint(-20, 20))
                    
                    # Crear partículas de láser
                    if random.random() < 0.3:
                        self.create_laser_particle()
                else:
                    self.laser_active = False
                    
        elif self.pattern == "evade" and self.player_detected:
            # Evadir al jugador
            dx = self.x - self.predicted_position[0]
            dy = self.y - self.predicted_position[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        
        # Actualizar efectos
        self.scan_angle += dt * 3
        self.update_particles(dt)
        
        # Mantener dentro de límites
        self.x = max(self.width//2, min(SCREEN_WIDTH - self.width//2, self.x))
        self.y = max(50, min(SCREEN_HEIGHT - 100, self.y))
    
    def create_laser_particle(self):
        """Crea partículas de efecto láser"""
        for _ in range(3):
            angle = random.uniform(0, math.pi*2)
            dist = random.uniform(0, 50)
            px = self.x + math.cos(angle) * dist
            py = self.y + math.sin(angle) * dist
            
            self.particles.append({
                'x': px, 'y': py,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'life': random.uniform(0.3, 0.8),
                'color': (255, 50, 50),
                'size': random.uniform(2, 4)
            })
    
    def update_particles(self, dt):
        """Actualiza partículas"""
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= dt
            
            if p['life'] <= 0:
                self.particles.remove(p)
    
    def draw(self, surface, camera_offset):
        """Dibuja dron con todos los efectos"""
        screen_y = self.y - camera_offset
        screen_x = self.x
        
        # Solo dibujar si está en pantalla (con margen)
        if screen_y < -150 or screen_y > SCREEN_HEIGHT + 150:
            return
        
        # ============================================
        # 🛸 DIBUJAR IMAGEN DEL DRON (PRIMERO)
        # ============================================
        if self.image:
            try:
                # Rotar la imagen según el ángulo
                rotated_image = pygame.transform.rotate(self.original_image, self.angle)
                # Centrar la imagen rotada
                rect = rotated_image.get_rect(center=(screen_x, screen_y))
                surface.blit(rotated_image, rect.topleft)
                
                # Si el dron detectó al jugador, añadir brillo rojo
                if self.player_detected:
                    # Crear superficie para efecto de brillo
                    glow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    glow.fill((255, 50, 50, 50))  # Rojo semi-transparente
                    surface.blit(glow, rect.topleft, special_flags=pygame.BLEND_ADD)
                    
            except Exception as e:
                print(f"[Drone] Error dibujando imagen: {e}")
                # Fallback: dibujar formas
                self.draw_fallback(surface, screen_x, screen_y)
        else:
            # Si no hay imagen, dibujar formas
            self.draw_fallback(surface, screen_x, screen_y)
        
        # ============================================
        # 🔄 HÉLICES ROTATORIAS (encima de la imagen)
        # ============================================
        prop_color = (200, 200, 200) if not self.player_detected else (255, 100, 100)
        prop_length = 25
        
        for i in range(4):
            angle = self.angle + (i * math.pi/2) + pygame.time.get_ticks() * 0.01
            blade_x = screen_x + math.cos(angle) * prop_length
            blade_y = screen_y + math.sin(angle) * prop_length
            
            pygame.draw.line(surface, prop_color,
                           (screen_x, screen_y),
                           (blade_x, blade_y), 3)
            
            # Puntas de las hélices
            pygame.draw.circle(surface, (255, 255, 255),
                             (int(blade_x), int(blade_y)), 3)
        
        # Centro de las hélices
        pygame.draw.circle(surface, (100, 100, 100),
                         (int(screen_x), int(screen_y)), 10)
        
        # ============================================
        # 👁️ "OJOS" DE VISIÓN
        # ============================================
        eye_color = (255, 0, 0) if self.player_detected else (0, 255, 0)
        for offset in [-15, 15]:
            eye_x = screen_x + offset
            eye_y = screen_y - 5
            
            # Ojo exterior
            pygame.draw.circle(surface, (30, 30, 30),
                             (int(eye_x), int(eye_y)), 8)
            
            # Pupila que se mueve
            pupil_angle = self.scan_angle
            pupil_x = eye_x + math.cos(pupil_angle) * 4
            pupil_y = eye_y + math.sin(pupil_angle) * 4
            
            pygame.draw.circle(surface, eye_color,
                             (int(pupil_x), int(pupil_y)), 4)
        
        # ============================================
        # 🔦 LÁSER DE SEGUIMIENTO
        # ============================================
        if self.laser_active:
            target_screen_y = self.laser_target[1] - camera_offset
            
            # Línea láser con efecto de parpadeo
            if int(pygame.time.get_ticks() / 100) % 2 == 0:
                # Línea principal
                pygame.draw.line(surface, (255, 0, 0),
                               (screen_x, screen_y),
                               (self.laser_target[0], target_screen_y), 3)
                
                # Efecto de brillo
                pygame.draw.line(surface, (255, 100, 100),
                               (screen_x, screen_y),
                               (self.laser_target[0], target_screen_y), 1)
                
                # Punto de impacto
                pygame.draw.circle(surface, (255, 50, 50),
                                 (int(self.laser_target[0]), int(target_screen_y)), 10)
                pygame.draw.circle(surface, (255, 0, 0),
                                 (int(self.laser_target[0]), int(target_screen_y)), 5)
        
        # ============================================
        # ✨ PARTÍCULAS DE PROPULSIÓN
        # ============================================
        for p in self.particles:
            particle_alpha = int(255 * (p['life'] * 1.5))
            if particle_alpha > 0:
                # Partícula con brillo
                size = int(p['size'])
                glow_size = size * 2
                
                particle_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.circle(particle_surf, (*p['color'], particle_alpha//2),
                                 (glow_size//2, glow_size//2), glow_size//2)
                pygame.draw.circle(particle_surf, (255, 200, 200, particle_alpha),
                                 (glow_size//2, glow_size//2), size)
                
                particle_x = p['x'] - camera_offset
                surface.blit(particle_surf, 
                           (int(p['x'] - glow_size//2), 
                            int(particle_x - glow_size//2)))
        
        # ============================================
        # 📡 EFECTO DE ESCANEO (solo si detecta jugador)
        # ============================================
        if self.player_detected:
            # Cono de visión semi-transparente
            scan_surf = pygame.Surface((self.detection_range, self.detection_range), 
                                      pygame.SRCALPHA)
            
            # Dibujar arco de escaneo
            for a in range(-30, 31, 2):
                angle = math.radians(a) + self.scan_angle
                alpha = 50 + int(100 * abs(math.sin(self.scan_angle * 2 + a/10)))
                
                for r in range(10, self.detection_range, 20):
                    x1 = self.detection_range//2 + math.cos(angle) * r
                    y1 = self.detection_range//2 + math.sin(angle) * r
                    x2 = self.detection_range//2 + math.cos(angle) * (r + 15)
                    y2 = self.detection_range//2 + math.sin(angle) * (r + 15)
                    
                    pygame.draw.line(scan_surf, (255, 0, 0, alpha),
                                   (x1, y1), (x2, y2), 2)
            
            surface.blit(scan_surf, 
                        (screen_x - self.detection_range//2, 
                         screen_y - self.detection_range//2))
        
        # ============================================
        # 🎯 INDICADOR DE ESTADO (solo debug)
        # ============================================
        if self.player_detected:
            font = pygame.font.Font(None, 18)
            status = "¡ALERTA!"
            status_color = (255, 50, 50)
            
            status_surf = font.render(status, True, status_color)
            surface.blit(status_surf, 
                        (screen_x - status_surf.get_width()//2, 
                         screen_y - self.height//2 - 25))
    
    def draw_fallback(self, surface, screen_x, screen_y):
        """Dibuja dron con formas cuando no hay imagen"""
        # Cuerpo principal
        body_rect = pygame.Rect(
            screen_x - self.width//2,
            screen_y - self.height//2,
            self.width,
            self.height
        )
        
        # Color según estado
        if self.player_detected:
            body_color = (255, 50, 50)
            border_color = (255, 150, 150)
        else:
            body_color = (50, 150, 255)
            border_color = (100, 200, 255)
        
        # Cuerpo con bordes redondeados
        pygame.draw.rect(surface, body_color, body_rect, border_radius=10)
        pygame.draw.rect(surface, border_color, body_rect, 3, border_radius=10)
        
        # Detalles
        pygame.draw.line(surface, (255, 255, 255),
                       (screen_x, screen_y - self.height//4),
                       (screen_x, screen_y + self.height//4), 2)
    
    def get_rect(self):
        """Retorna rectángulo de colisión"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2,
                          self.width, self.height)
    
    def get_damage(self):
        """Daño que causa el dron"""
        return self.damage


# ============================================
# 🧪 FUNCIÓN PARA PROBAR EL DRON
# ============================================

def test_drone():
    """Prueba el dron por separado"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    print("\n=== PRUEBA DEL DRON ===")
    drone = SurveillanceDrone(400, 300)
    print(f"Drone creado en: ({drone.x}, {drone.y})")
    print(f"Tamaño: {drone.width}x{drone.height}")
    print(f"Tiene imagen: {'Sí' if drone.image else 'No'}")
    
    running = True
    camera_offset = 0
    player_pos = (400, 400)
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # El mouse simula la posición del jugador
                player_pos = event.pos
        
        # Actualizar dron
        drone.update(dt, player_pos)
        
        # Dibujar
        screen.fill((30, 30, 50))
        drone.draw(screen, camera_offset)
        
        # Dibujar posición del "jugador" (mouse)
        pygame.draw.circle(screen, (0, 255, 0), 
                         (int(player_pos[0]), int(player_pos[1])), 10)
        
        # Información
        font = pygame.font.Font(None, 24)
        info = f"Patrón: {drone.pattern} | Detectado: {drone.player_detected}"
        text = font.render(info, True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()

# Para probar: python drones.py
if __name__ == "__main__":
    test_drone()