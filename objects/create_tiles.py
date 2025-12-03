# create_tiles.py - Genera tiles simples si no los tienes

import pygame
import os

def create_blue_tiles():
    """Crea tiles azules simples"""
    os.makedirs("./Assets/Terrain/Blue", exist_ok=True)
    
    for i in range(11):
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        
        # Base azul
        pygame.draw.rect(surf, (50, 50, 200), (0, 0, 64, 64))
        
        # Patrones según variante
        if i == 0:  # Esquina izquierda
            pygame.draw.rect(surf, (100, 100, 255), (0, 0, 32, 64))
        elif i == 1:  # Centro
            pygame.draw.circle(surf, (150, 150, 255), (32, 32), 15)
        elif i == 2:  # Esquina derecha
            pygame.draw.rect(surf, (100, 100, 255), (32, 0, 32, 64))
        elif i >= 3:  # Variantes decorativas
            # Patrón de líneas
            for j in range(4):
                y = j * 16 + 8
                pygame.draw.line(surf, (200, 200, 255), (10, y), (54, y), 2)
        
        # Borde
        pygame.draw.rect(surf, (255, 255, 255), (0, 0, 64, 64), 2)
        
        # Guardar
        pygame.image.save(surf, f"./Assets/Terrain/Blue/blue_{i}.png")
        print(f"[TileGen] Creado blue_{i}.png")

def create_terrain_tiles():
    """Crea tiles de terreno simples"""
    os.makedirs("./Assets/Terrain/Terrain", exist_ok=True)
    
    for i in range(11):
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        
        # Base marrón
        base_color = (139, 69, 19)
        pygame.draw.rect(surf, base_color, (0, 0, 64, 64))
        
        # Texturas según variante
        if i == 0:  # Tierra lisa
            pass
        elif i == 1:  # Hierba (parte superior verde)
            pygame.draw.rect(surf, (34, 139, 34), (0, 0, 64, 16))
        elif i == 2:  # Roca
            for _ in range(20):
                x = pygame.time.get_ticks() % 50 + 7  # Posición pseudo-aleatoria
                y = pygame.time.get_ticks() % 50 + 7
                pygame.draw.circle(surf, (169, 169, 169), (x, y), 3)
        elif i >= 3:  # Variantes decorativas
            # Piedras/hierbas
            for _ in range(5):
                x = (i * 13) % 50 + 7
                y = (i * 17) % 50 + 7
                size = 2 + (i % 3)
                color = (100, 100, 100) if i % 2 == 0 else (34, 139, 34)
                pygame.draw.circle(surf, color, (x, y), size)
        
        # Borde
        pygame.draw.rect(surf, (255, 255, 255), (0, 0, 64, 64), 2)
        
        # Guardar
        pygame.image.save(surf, f"./Assets/Terrain/Terrain/terrain_{i}.png")
        print(f"[TileGen] Creado terrain_{i}.png")

if __name__ == "__main__":
    pygame.init()
    create_blue_tiles()
    create_terrain_tiles()
    print("[TileGen] ¡Tiles creados exitosamente!")