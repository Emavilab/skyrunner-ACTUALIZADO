"""
test_powerups.py - Prueba visual de power-ups
"""

import pygame
import sys
from objects.constants import *

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Importar power-ups
try:
    from objects.powerup_simple import PowerUp
    print("OK Power-ups simples importados")
except Exception as e:
    print(f"ERROR Error importando power-ups: {e}")
    sys.exit(1)

# Crear power-ups de prueba
test_powerups = [
    PowerUp(200, 200, 'shield'),
    PowerUp(400, 200, 'speed'),
    PowerUp(600, 200, 'zoom'),
    PowerUp(200, 400, 'combo'),
    PowerUp(400, 400, 'magnet'),
    PowerUp(600, 400, 'double_jump')
]

print(f"OK {len(test_powerups)} power-ups creados")

running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Actualizar power-ups
    for powerup in test_powerups:
        powerup.update(dt)
    
    # Dibujar
    screen.fill((50, 50, 50))
    
    # Título
    font = pygame.font.Font(None, 48)
    title = font.render("PRUEBA DE POWER-UPS", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
    
    # Instrucciones
    font_small = pygame.font.Font(None, 24)
    instructions = font_small.render("Deberían verse círculos de colores con símbolos", True, (200, 200, 200))
    screen.blit(instructions, (SCREEN_WIDTH//2 - instructions.get_width()//2, 120))
    
    # Dibujar power-ups
    for i, powerup in enumerate(test_powerups):
        powerup.draw(screen, 0)  # camera_offset = 0
        
        # Nombre del tipo debajo
        type_text = font_small.render(powerup.type.upper(), True, (255, 255, 255))
        screen.blit(type_text, (powerup.x - type_text.get_width()//2, powerup.y + 50))
    
    pygame.display.flip()

pygame.quit()