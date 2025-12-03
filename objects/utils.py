"""
utils.py - Funciones Auxiliares

Contiene funciones matemáticas y de utilidad general
utilizadas en todo el proyecto.
"""

import pygame
import math

def lerp(start, end, t):
    """
    Interpolación lineal entre dos valores.
    
    Args:
        start: Valor inicial
        end: Valor final
        t: Factor de interpolación (0-1)
    
    Returns:
        Valor interpolado
    """
    return start + (end - start) * t

def clamp(value, min_val, max_val):
    """
    Limita un valor entre un mínimo y un máximo.
    
    Args:
        value: Valor a limitar
        min_val: Valor mínimo
        max_val: Valor máximo
    
    Returns:
        Valor limitado
    """
    return max(min_val, min(value, max_val))

def distance(x1, y1, x2, y2):
    """
    Calcula la distancia euclidiana entre dos puntos.
    
    Args:
        x1, y1: Coordenadas del primer punto
        x2, y2: Coordenadas del segundo punto
    
    Returns:
        Distancia entre los puntos
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def rotate_point(x, y, cx, cy, angle):
    """
    Rota un punto alrededor de un centro.
    Implementa la transformación de rotación en 2D.
    
    Args:
        x, y: Coordenadas del punto a rotar
        cx, cy: Centro de rotación
        angle: Ángulo de rotación en grados
    
    Returns:
        Tupla (x_rotado, y_rotado)
    """
    # Convertir ángulo a radianes
    rad = math.radians(angle)
    
    # Trasladar punto al origen
    tx = x - cx
    ty = y - cy
    
    # Aplicar matriz de rotación
    rx = tx * math.cos(rad) - ty * math.sin(rad)
    ry = tx * math.sin(rad) + ty * math.cos(rad)
    
    # Trasladar de vuelta
    return rx + cx, ry + cy

def check_collision_rect(rect1, rect2):
    """
    Detecta colisión entre dos rectángulos.
    
    Args:
        rect1, rect2: pygame.Rect objects
    
    Returns:
        True si hay colisión, False en caso contrario
    """
    return rect1.colliderect(rect2)

def draw_text(surface, text, x, y, font, color=(255, 255, 255), center=False):
    """
    Dibuja texto en una superficie.
    
    Args:
        surface: Superficie donde dibujar
        text: Texto a dibujar
        x, y: Coordenadas
        font: Fuente pygame
        color: Color del texto
        center: Si True, centra el texto en (x, y)
    """
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    surface.blit(text_surface, text_rect)

def sine_wave(time, amplitude, frequency):
    """
    Genera un valor de onda sinusoidal.
    Utilizado para movimientos enemigos.
    
    Args:
        time: Tiempo actual
        amplitude: Amplitud de la onda
        frequency: Frecuencia de la onda
    
    Returns:
        Valor de la onda sinusoidal
    """
    return amplitude * math.sin(time * frequency)

def create_gradient_surface(width, height, color1, color2, vertical=True):
    """
    Crea una superficie con gradiente de color.
    
    Args:
        width, height: Dimensiones de la superficie
        color1: Color inicial
        color2: Color final
        vertical: True para gradiente vertical, False para horizontal
    
    Returns:
        Superficie pygame con gradiente
    """
    surface = pygame.Surface((width, height))
    
    if vertical:
        for y in range(height):
            t = y / height
            r = int(lerp(color1[0], color2[0], t))
            g = int(lerp(color1[1], color2[1], t))
            b = int(lerp(color1[2], color2[2], t))
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    else:
        for x in range(width):
            t = x / width
            r = int(lerp(color1[0], color2[0], t))
            g = int(lerp(color1[1], color2[1], t))
            b = int(lerp(color1[2], color2[2], t))
            pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))
    
    return surface

def screen_shake(magnitude):
    """
    Genera offsets para efecto de screen shake.
    
    Args:
        magnitude: Intensidad del shake
    
    Returns:
        Tupla (offset_x, offset_y)
    """
    import random
    return (random.randint(-magnitude, magnitude), 
            random.randint(-magnitude, magnitude))

def format_time(seconds):
    """
    Formatea segundos a formato MM:SS.
    
    Args:
        seconds: Tiempo en segundos
    
    Returns:
        String formateado
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"