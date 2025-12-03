"""
SkyRunner - Runner Vertical 2D
Proyecto de Informática Gráfica
"""

import pygame
import sys
import json
import os
from datetime import datetime
from objects.constants import *
from objects.game import Game
from objects.audio import init_audio
from objects.utils import draw_text, lerp
from Models.lava import Lava
from objects.platforms import Platform, MovingPlatform

class MenuState:
    """Estados del menú principal"""
    MAIN = "main"
    HIGH_SCORES = "high_scores"
    DIFFICULTY = "difficulty"
    CONTROLS = "controls"
    CREDITS = "credits"

def load_high_scores():
    """Cargar puntuaciones altas desde archivo"""
    try:
        if os.path.exists("high_scores.json"):
            with open("high_scores.json", "r") as f:
                return json.load(f)
    except:
        pass
    # Puntuaciones por defecto
    return {
        "easy": [
            {"name": "PRO", "score": 15000, "date": "2024-01-01"},
            {"name": "MASTER", "score": 12000, "date": "2024-01-01"},
            {"name": "SKILL", "score": 10000, "date": "2024-01-01"},
        ],
        "normal": [
            {"name": "LEGEND", "score": 20000, "date": "2024-01-01"},
            {"name": "HERO", "score": 15000, "date": "2024-01-01"},
            {"name": "CHAMP", "score": 12000, "date": "2024-01-01"},
        ],
        "hard": [
            {"name": "GOD", "score": 30000, "date": "2024-01-01"},
            {"name": "TITAN", "score": 25000, "date": "2024-01-01"},
            {"name": "DEMON", "score": 20000, "date": "2024-01-01"},
        ]
    }

def save_high_score(difficulty, name, score):
    """Guardar nueva puntuación alta"""
    try:
        high_scores = load_high_scores()
        high_scores[difficulty].append({
            "name": name[:3].upper(),
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        # Ordenar y mantener solo top 10
        high_scores[difficulty].sort(key=lambda x: x["score"], reverse=True)
        high_scores[difficulty] = high_scores[difficulty][:10]
        
        with open("high_scores.json", "w") as f:
            json.dump(high_scores, f, indent=2)
        return True
    except:
        return False

def draw_gradient_background(screen, color_top, color_bottom):
    """Dibujar fondo degradado"""
    for y in range(SCREEN_HEIGHT):
        factor = y / SCREEN_HEIGHT
        r = int(lerp(color_top[0], color_bottom[0], factor))
        g = int(lerp(color_top[1], color_bottom[1], factor))
        b = int(lerp(color_top[2], color_bottom[2], factor))
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

def draw_particle_background(screen, particles):
    """Dibujar partículas de fondo"""
    for particle in particles:
        pygame.draw.circle(screen, (100, 200, 255), 
                          (int(particle[0]), int(particle[1])), 
                          int(particle[2]))
        # Actualizar posición
        particle[0] += particle[3]
        particle[1] += particle[4]
        particle[2] -= 0.1
        
        # Reiniciar partícula si sale de pantalla o se hace muy pequeña
        if (particle[0] < 0 or particle[0] > SCREEN_WIDTH or 
            particle[1] < 0 or particle[1] > SCREEN_HEIGHT or 
            particle[2] <= 0):
            particle[0] = pygame.time.get_ticks() % SCREEN_WIDTH
            particle[1] = SCREEN_HEIGHT
            particle[2] = pygame.time.get_ticks() % 3 + 1
            particle[3] = (pygame.time.get_ticks() % 3 - 1) * 0.5
            particle[4] = - (pygame.time.get_ticks() % 2 + 1)

def draw_text_with_shadow(screen, text, x, y, font, color, center=False, shadow_color=(0, 0, 0)):
    """Dibujar texto con sombra (versión alternativa si draw_text no soporta shadow)"""
    # Primero dibujar sombra
    shadow_surf = font.render(text, True, shadow_color)
    shadow_rect = shadow_surf.get_rect()
    if center:
        shadow_rect.center = (x + 2, y + 2)  # Desplazamiento para sombra
    else:
        shadow_rect.topleft = (x + 2, y + 2)
    screen.blit(shadow_surf, shadow_rect)
    
    # Luego dibujar texto principal
    return draw_text(screen, text, x, y, font, color, center)

def draw_menu_option(screen, x, y, width, height, text, font, color, 
                    hover=False, selected=False):
    """Dibujar una opción del menú con efectos visuales"""
    if selected:
        # Marco brillante para opción seleccionada
        pygame.draw.rect(screen, (255, 255, 200), 
                        (x-5, y-5, width+10, height+10), 
                        border_radius=15)
        
    if hover:
        # Fondo animado para opción con hover
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
        color_pulse = tuple(min(255, int(c + 50 * pulse)) for c in color[:3])
        pygame.draw.rect(screen, color_pulse, (x, y, width, height), 
                        border_radius=10)
        text_color = (0, 0, 0)  # Texto negro sobre fondo claro
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), 
                        0 if hover else 3, border_radius=10)
        text_color = color  # Texto del color del borde
    
    # Texto
    draw_text(screen, text, x + width//2, y + height//2, 
             font, text_color, center=True)

def show_high_scores_menu(screen, clock, font_title, font_subtitle, font_normal, difficulty):
    """Mostrar menú de puntuaciones altas"""
    high_scores = load_high_scores()
    scores = high_scores.get(difficulty, [])
    
    # Partículas para fondo animado
    particles = []
    for _ in range(50):
        particles.append([
            pygame.time.get_ticks() % SCREEN_WIDTH,
            pygame.time.get_ticks() % SCREEN_HEIGHT,
            pygame.time.get_ticks() % 3 + 1,
            (pygame.time.get_ticks() % 3 - 1) * 0.5,
            - (pygame.time.get_ticks() % 2 + 1)
        ])
    
    while True:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]:
                    return True
                elif event.key in [pygame.K_1, pygame.K_KP1, pygame.K_e]:
                    difficulty = "easy"
                    scores = high_scores.get(difficulty, [])
                elif event.key in [pygame.K_2, pygame.K_KP2, pygame.K_n]:
                    difficulty = "normal"
                    scores = high_scores.get(difficulty, [])
                elif event.key in [pygame.K_3, pygame.K_KP3, pygame.K_h]:
                    difficulty = "hard"
                    scores = high_scores.get(difficulty, [])
        
        # Dibujar fondo con partículas
        draw_gradient_background(screen, (5, 5, 15), (15, 10, 40))
        draw_particle_background(screen, particles)
        
        # Título con sombra manual
        draw_text_with_shadow(screen, "🏆 PUNTUACIONES ALTAS", SCREEN_WIDTH // 2, 60,
                             font_title, (255, 215, 0), center=True)
        
        # Selector de dificultad
        diff_settings = DIFFICULTY_SETTINGS[difficulty]
        diff_color = diff_settings["color"]
        diff_name = diff_settings["name"]
        
        pygame.draw.rect(screen, diff_color,
                        (SCREEN_WIDTH//2 - 150, 120, 300, 40), 
                        border_radius=5)
        draw_text(screen, f"Dificultad: {diff_name}", SCREEN_WIDTH // 2, 140,
                 font_subtitle, (0, 0, 0), center=True)
        
        draw_text(screen, "E:Fácil  N:Normal  H:Difícil",
                 SCREEN_WIDTH // 2, 180, font_normal, (200, 200, 200), center=True)
        
        # Tabla de puntuaciones
        y_start = 240
        
        # Fondo semi-transparente para la tabla (SIN borde)
        table_surface = pygame.Surface((500, 320), pygame.SRCALPHA)
        pygame.draw.rect(table_surface, (20, 20, 40, 200), (0, 0, 500, 320), border_radius=10)
        screen.blit(table_surface, (SCREEN_WIDTH//2 - 250, y_start - 10))
        
        # Borde exterior decorativo
        pygame.draw.rect(screen, (100, 200, 255),
                        (SCREEN_WIDTH//2 - 250, y_start - 10, 500, 320),
                        2, border_radius=10)
        
        # Encabezados de la tabla
        headers = ["POS", "NOMBRE", "PUNTUACIÓN", "FECHA"]
        header_x = [SCREEN_WIDTH//2 - 220, SCREEN_WIDTH//2 - 120, 
                   SCREEN_WIDTH//2 + 30, SCREEN_WIDTH//2 + 180]
        
        for i, header in enumerate(headers):
            draw_text(screen, header, header_x[i], y_start + 10,
                     font_normal, (100, 200, 255), center=False)
        
        # Línea separadora de encabezados
        pygame.draw.line(screen, (100, 200, 255),
                        (SCREEN_WIDTH//2 - 240, y_start + 40),
                        (SCREEN_WIDTH//2 + 240, y_start + 40), 2)
        
        # Lista de puntuaciones
        for i, score_data in enumerate(scores[:10]):  # Mostrar top 10
            y_pos = y_start + 60 + i * 26
            
            # Color alternado para filas (fondo más visible)
            if i % 2 == 0:
                row_surface = pygame.Surface((480, 24), pygame.SRCALPHA)
                pygame.draw.rect(row_surface, (255, 255, 255, 30), (0, 0, 480, 24))
                screen.blit(row_surface, (SCREEN_WIDTH//2 - 240, y_pos - 12))
            
            # Posición con medalla para top 3
            if i == 0:
                pos_text = "1st"
                pos_color = (255, 215, 0)  # Oro
            elif i == 1:
                pos_text = "2nd"
                pos_color = (192, 192, 192)  # Plata
            elif i == 2:
                pos_text = "3rd"
                pos_color = (205, 127, 50)  # Bronce
            else:
                pos_text = f"{i+1}"
                pos_color = (200, 200, 200)
            
            # Mostrar datos con mejor espaciado
            draw_text(screen, pos_text, header_x[0], y_pos,
                     font_normal, pos_color, center=False)
            draw_text(screen, score_data["name"], header_x[1], y_pos,
                     font_normal, (255, 255, 255), center=False)
            draw_text(screen, str(score_data["score"]), header_x[2], y_pos,
                     font_normal, (100, 255, 100), center=False)
            draw_text(screen, score_data["date"], header_x[3], y_pos,
                     font_normal, (180, 180, 180), center=False)
        
        # Si no hay suficientes puntuaciones
        if len(scores) < 10:
            for i in range(len(scores), 10):
                y_pos = y_start + 60 + i * 26
                draw_text(screen, "- - -", SCREEN_WIDTH // 2, y_pos,
                         font_normal, (100, 100, 100), center=True)
        
        # Instrucciones
        draw_text(screen, "ESC o ENTER para volver",
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60,
                 font_normal, (200, 200, 200), center=True)
        
        pygame.display.flip()

def show_controls_menu(screen, clock, font_title, font_normal):
    """Mostrar menú de controles"""
    controls = [
        ("<- ->", "Moverse izquierda/derecha"),
        ("SPACE", "Saltar"),
        ("DOWN", "Caída rápida"),
        ("ESC", "Pausa/Menú"),
        ("R", "Reiniciar juego"),
        ("M", "Silenciar audio"),
        ("F", "Fullscreen"),
        ("F1", "Salir/entrar del fullscreen")
    ]
    
    while True:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    return True
        
        # Fondo
        draw_gradient_background(screen, (10, 10, 40), (20, 10, 60))
        
        # Título
        draw_text_with_shadow(screen, "🎮 CONTROLES", SCREEN_WIDTH // 2, 80,
                             font_title, (100, 200, 255), center=True)
        
        # Tabla de controles
        y_start = 180
        pygame.draw.rect(screen, (255, 255, 255, 30),
                        (SCREEN_WIDTH//2 - 250, y_start - 20, 500, 280),
                        2, border_radius=10)
        
        for i, (key, description) in enumerate(controls):
            y_pos = y_start + i * 50
            
            # Tecla
            pygame.draw.rect(screen, (255, 215, 0),
                           (SCREEN_WIDTH//2 - 200, y_pos - 15, 100, 40),
                           border_radius=5)
            draw_text(screen, key, SCREEN_WIDTH//2 - 150, y_pos + 5,
                     font_normal, (0, 0, 0), center=True)
            
            # Descripción
            draw_text(screen, description, SCREEN_WIDTH//2 + 80, y_pos + 5,
                     font_normal, (255, 255, 255), center=False)
        
        # Instrucciones
        draw_text(screen, "ESC o ENTER para volver",
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80,
                 font_normal, (200, 200, 200), center=True)
        
        pygame.display.flip()

def show_credits_menu(screen, clock, font_title, font_normal):
    """Mostrar créditos del juego"""
    credits = [
        "SKYRUNNER - Runner Vertical 2D",
        "Desarrollado con PyGame",
        "",
        "🎮 DESARROLLADOR PRINCIPAL",
        "Proyecto de Informática Gráfica",
        "",
        "🖼️ ARTE Y DISEÑO",
        "Sprites y efectos visuales",
        "",
        "AUDIO Y EFECTOS DE SONIDO",
        "Banda sonora y efectos",
        "",
        "💻 PROGRAMACIÓN",
        "Lógica del juego y física",
        "",
        "© 2024 SkyRunner Team",
        "Todos los derechos reservados"
    ]
    
    scroll_pos = SCREEN_HEIGHT
    scroll_speed = 20  # píxeles por segundo
    
    while True:
        dt = clock.tick(FPS) / 1000.0
        
        # Actualizar posición del scroll
        scroll_pos -= scroll_speed * dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    return True
        
        # Fondo
        draw_gradient_background(screen, (0, 0, 20), (10, 0, 40))
        
        # Estrellas animadas
        for i in range(100):
            x = (i * 37) % SCREEN_WIDTH
            y = (i * 23 + scroll_pos * 0.5) % SCREEN_HEIGHT
            size = (i % 3) + 1
            alpha = abs((pygame.time.get_ticks() + i * 100) % 2000 - 1000) / 1000
            color = tuple(min(255, int(255 * alpha)) for _ in range(3))
            pygame.draw.circle(screen, color, (int(x), int(y)), size)
        
        # Título fijo
        draw_text_with_shadow(screen, "🌟 CRÉDITOS", SCREEN_WIDTH // 2, 60,
                             font_title, (255, 255, 100), center=True)
        
        # Créditos en scroll
        for i, line in enumerate(credits):
            y_pos = scroll_pos + i * 50
            
            if 100 < y_pos < SCREEN_HEIGHT - 50:
                color = (255, 255, 255)
                if "SKYRUNNER" in line:
                    color = (100, 200, 255)
                elif "DESARROLLADOR" in line or "PROGRAMACIÓN" in line:
                    color = (255, 100, 100)
                elif "ARTE" in line:
                    color = (100, 255, 100)
                elif "AUDIO" in line:
                    color = (255, 100, 255)
                elif "©" in line:
                    color = (200, 200, 200)
                
                # Usar sombra solo para líneas importantes
                if "SKYRUNNER" in line or "DESARROLLADOR" in line or "ARTE" in line or "AUDIO" in line or "PROGRAMACIÓN" in line:
                    draw_text_with_shadow(screen, line, SCREEN_WIDTH // 2, y_pos,
                                         font_normal, color, center=True)
                else:
                    draw_text(screen, line, SCREEN_WIDTH // 2, y_pos,
                             font_normal, color, center=True)
        
        # Si el scroll ha terminado, reiniciar
        if scroll_pos < -len(credits) * 50:
            scroll_pos = SCREEN_HEIGHT
        
        # Instrucciones
        draw_text(screen, "ESC o ENTER para volver",
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40,
                 font_normal, (200, 200, 200), center=True)
        
        pygame.display.flip()

def main():
    """Punto de entrada principal del juego"""
    # Inicializar Pygame
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"[Audio WARN] No se pudo inicializar el audio: {e}")

    # Configurar ventana
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SkyRunner - Runner Vertical 2D")
    clock = pygame.time.Clock()

    # Inicializar audio
    init_audio()

    # Fuentes para menú
    font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
    font_subtitle = pygame.font.Font(None, FONT_SIZE_SUBTITLE)
    font_normal = pygame.font.Font(None, FONT_SIZE_HUD)
    
    # Estado del menú
    menu_state = MenuState.MAIN
    selected_option = 0
    difficulty = "normal"
    
    # Opciones del menú principal
    main_options = [
        ("🎮 COMENZAR JUEGO", MenuState.MAIN),
        ("🏆 PUNTUACIONES ALTAS", MenuState.HIGH_SCORES),
        ("⚙️ CONTROLES", MenuState.CONTROLS),
        ("🌟 CRÉDITOS", MenuState.CREDITS),
        ("🚪 SALIR", MenuState.MAIN)
    ]
    
    # Partículas para fondo animado
    particles = []
    for _ in range(30):
        particles.append([
            pygame.time.get_ticks() % SCREEN_WIDTH,
            pygame.time.get_ticks() % SCREEN_HEIGHT,
            pygame.time.get_ticks() % 3 + 1,
            (pygame.time.get_ticks() % 3 - 1) * 0.5,
            - (pygame.time.get_ticks() % 2 + 1)
        ])

    try:
        running = True
        start_game = False
        
        while running:
            dt = clock.tick(FPS) / 1000.0

            # Manejo de eventos según el estado del menú
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if menu_state == MenuState.MAIN:
                        if event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % len(main_options)
                        elif event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % len(main_options)
                        elif event.key == pygame.K_RETURN:
                            option_text, _ = main_options[selected_option]
                            if option_text == "🎮 COMENZAR JUEGO":
                                menu_state = MenuState.MAIN
                                # Salir del menú para comenzar juego
                                running = False
                                start_game = True
                            elif option_text == "🏆 PUNTUACIONES ALTAS":
                                menu_state = MenuState.HIGH_SCORES
                            elif option_text == "⚙️ CONTROLES":
                                menu_state = MenuState.CONTROLS
                            elif option_text == "🌟 CRÉDITOS":
                                menu_state = MenuState.CREDITS
                            elif option_text == "🚪 SALIR":
                                return
                        elif event.key in [pygame.K_1, pygame.K_KP1, pygame.K_e]:
                            difficulty = "easy"
                        elif event.key in [pygame.K_2, pygame.K_KP2, pygame.K_n]:
                            difficulty = "normal"
                        elif event.key in [pygame.K_3, pygame.K_KP3, pygame.K_h]:
                            difficulty = "hard"
                        elif event.key == pygame.K_f:
                            # Pantalla completa
                            pygame.display.toggle_fullscreen()
                    
                    elif event.key == pygame.K_ESCAPE:
                        # Volver al menú principal desde cualquier submenú
                        if menu_state != MenuState.MAIN:
                            menu_state = MenuState.MAIN
                        else:
                            # Si ya estamos en el menú principal, ESC cierra el juego
                            return
            
            # Renderizar según el estado actual
            if menu_state == MenuState.MAIN:
                # Dibujar fondo con partículas
                draw_gradient_background(screen, (5, 5, 25), (15, 10, 50))
                draw_particle_background(screen, particles)
                
                # Título con efecto brillante
                pulse = abs(pygame.time.get_ticks() % 2000 - 1000) / 1000
                title_color = tuple(int(c * (0.7 + 0.3 * pulse)) for c in CYAN)
                
                draw_text_with_shadow(screen, "SKYRUNNER", SCREEN_WIDTH // 2, 80,
                                     font_title, title_color, center=True)
                draw_text(screen, "Runner Vertical 2D", SCREEN_WIDTH // 2, 130,
                         font_subtitle, (200, 200, 255), center=True)
                
                # Indicador de dificultad
                diff_settings = DIFFICULTY_SETTINGS[difficulty]
                diff_color = diff_settings["color"]
                diff_name = diff_settings["name"]
                
                pygame.draw.rect(screen, diff_color,
                               (SCREEN_WIDTH//2 - 150, 170, 300, 40), 
                               border_radius=5)
                draw_text(screen, f"Dificultad: {diff_name}", SCREEN_WIDTH // 2, 190,
                         font_subtitle, (0, 0, 0), center=True)
                
                # Instrucciones para cambiar dificultad
                draw_text(screen, "E:Fácil  N:Normal  H:Difícil ",
                         SCREEN_WIDTH // 2, 230, font_normal, (200, 200, 200), center=True)
                
                # Opciones del menú principal
                y_start = 300
                for i, (option_text, _) in enumerate(main_options):
                    is_hover = (i == selected_option)
                    
                    draw_menu_option(
                        screen,
                        SCREEN_WIDTH//2 - 200,
                        y_start + i*80 - 20,
                        400,
                        60,
                        option_text,
                        font_subtitle,
                        YELLOW,
                        hover=is_hover,
                        selected=is_hover
                    )
                
                # Instrucciones de navegación
                draw_text(screen, "UP DOWN - Navegar   ENTER - Seleccionar   ESC - Salir",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40,
                         font_normal, (200, 200, 200), center=True)
                
                pygame.display.flip()
            
            elif menu_state == MenuState.HIGH_SCORES:
                if not show_high_scores_menu(screen, clock, font_title, 
                                           font_subtitle, font_normal, difficulty):
                    running = False
                else:
                    menu_state = MenuState.MAIN
            
            elif menu_state == MenuState.CONTROLS:
                if not show_controls_menu(screen, clock, font_title, font_normal):
                    running = False
                else:
                    menu_state = MenuState.MAIN
            
            elif menu_state == MenuState.CREDITS:
                if not show_credits_menu(screen, clock, font_title, font_normal):
                    running = False
                else:
                    menu_state = MenuState.MAIN
            
          # Si salimos del menú para comenzar juego
            if start_game:
                try:
                    # Crear instancia del juego con dificultad seleccionada, pasando la pantalla existente
                    game = Game(difficulty, screen)
                    
                    # Ejecutar el juego
                    game.run()
                    
                    # Debug: Verificar estado de la bandera
                    print(f"[DEBUG] Después de game.run(): return_to_menu = {getattr(game, 'return_to_menu', 'NO EXISTE')}")
                    
                    # Verificar si el juego quiere volver al menú o salir completamente
                    if hasattr(game, 'return_to_menu') and game.return_to_menu:
                        print("[DEBUG] Regresando al menú principal desde juego")
                        # Limpiar eventos pendientes para evitar conflictos
                        pygame.event.clear()
                        # Regresar al menú principal
                        menu_state = MenuState.MAIN
                        selected_option = 0
                        start_game = False
                        running = True  # CRÍTICO: Reactivar el loop del menú
                    else:
                        print("[DEBUG] Juego terminó - cerrando aplicación")
                        # El juego terminó por cerrar ventana
                        running = False
                except Exception as e:
                    print(f"[Error] Se produjo un error durante la ejecución del juego: {e}")
                    import traceback
                    traceback.print_exc()
                    # Regresar al menú después de un error
                    menu_state = MenuState.MAIN
                    selected_option = 0
                    start_game = False
                    running = True  # Mantener el menú activo tras error
        
    except Exception as e:
        print(f"[Error] Se produjo un error durante la ejecución del juego: {e}")
        import traceback
        traceback.print_exc()

    # Cerrar Pygame correctamente solo al final
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()