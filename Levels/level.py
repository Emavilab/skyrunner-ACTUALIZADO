"""
level.py - Sistema de Niveles ÉPICO CON TILE MANAGER
VERSIÓN CORREGIDA CON POWER-UPS FUNCIONALES
"""

import pygame
import random
import math
import os
# Removed invalid import as it is unnecessary and already handled in the corrected imports below.
from objects.constants import *
from objects.platforms import Platform, MovingPlatform, CastlePlatform, VictoryFlag
from Models.enemies import Bat, RotatingTrap, FallingRock, Lightning, SurveillanceDrone

# ============================================
# 🔧 IMPORTACIÓN CORREGIDA DE POWER-UPS
# ============================================

# SOLUCIÓN: Importar solo UNA vez correctamente
try:
    # Primero intenta con powerup_simple (nuestra versión de prueba)
    from objects.powerup_simple import PowerUp, CollectionEffect
    print("[Level] OK Usando powerup_simple.py para power-ups")
except ImportError:
    print("[Level] WARNING powerup_simple.py no encontrado, intentando alternativas...")
    try:
        from objects.powerup import PowerUp, CollectionEffect
        print("[Level] OK Usando powerup.py original")
    except ImportError:
        print("[Level] WARNING powerup.py no encontrado, creando emergencia...")
        # Clase de emergencia mínima
        class PowerUp:
            def __init__(self, x, y, powerup_type='shield'):
                self.x = x
                self.y = y
                self.type = powerup_type
                self.collected = False
                self.size = 25
                print(f"[EMERGENCIA] PowerUp creado en ({x}, {y}) tipo: {powerup_type}")
            
            def update(self, dt):
                pass
            
            def draw(self, surface, camera_offset):
                if not self.collected:
                    screen_y = self.y - camera_offset
                    pygame.draw.circle(surface, (255, 0, 0), 
                                     (int(self.x), int(screen_y)), self.size)
            
            def get_rect(self):
                return pygame.Rect(self.x - self.size, self.y - self.size, 
                                 self.size*2, self.size*2)
            
            def collect(self):
                if not self.collected:
                    self.collected = True
                    return True
                return False
        
        class CollectionEffect:
            def __init__(self, x, y, color, powerup_type='shield'):
                self.x = x
                self.y = y
                self.color = color
                self.active = True
            
            def update(self, dt):
                self.active = False
            
            def draw(self, surface, camera_offset):
                pass


class Level:
    """
    Clase que representa un nivel del juego.
    Genera y gestiona todos los elementos del nivel.
    """
    
    def __init__(self, level_number, custom_config=None, use_tiles=True, difficulty="normal"):
        """
        Inicializa un nivel.
        
        Args:
            level_number: Número del nivel (1-3)
            custom_config: Configuración personalizada (opcional)
            use_tiles: True para usar TileManager (por defecto)
            difficulty: Dificultad del juego ("easy", "normal", "hard")
        """
        self.number = level_number
        self.difficulty = difficulty
        self.config = custom_config if custom_config else LEVELS_CONFIG[level_number]
        self.theme = LEVEL_COLORS[level_number]
        self.use_tiles = use_tiles
        
        # Intentar cargar TileManager
        self.tile_manager = None
        if self.use_tiles:
            self.tile_manager = self._try_load_tile_manager()
            if not self.tile_manager:
                print(f"[Level {self.number}] Usando sistema de plataformas original")
                self.use_tiles = False
        
        # Listas de objetos
        self.platforms = []        # Plataformas regulares
        self.tile_platforms = []   # Plataformas de tiles (si usamos TileManager)
        self.enemies = []
        self.powerups = []
        self.effects = []
        self.flags = []            # Lista de banderas de victoria
        
        # Referencia a plataforma final
        self.final_platform = None
        
        # Altura del nivel - ¡MUCHO MÁS GRANDE!
        self.height = self.config['platforms'] * PLATFORM_VERTICAL_SPACING * 2
        
        # Parallax layers
        self.parallax_layers = self._create_parallax_layers()
        
        # Generar nivel
        self._generate()
        
        print(f"[Level {self.number}] Altura total del nivel: {self.height}px")
        print(f"[Level {self.number}] Power-ups generados: {len(self.powerups)}")
        
    def _try_load_tile_manager(self):
        """Intenta cargar TileManager, retorna None si falla"""
        try:
            # Buscar el archivo en diferentes ubicaciones
            tile_manager_paths = [
                "tile_manager.py",
                "./tile_manager.py",
                "../tile_manager.py",
                "objects/tile_manager.py",
                "Levels/tile_manager.py"
            ]
            
            for path in tile_manager_paths:
                try:
                    if path == "tile_manager.py":
                        from .tile_manager import TileManager
                    elif path == "./tile_manager.py":
                        from Levels.tile_manager import TileManager
                    elif path == "objects/tile_manager.py":
                        from objects.tile_manager import TileManager
                    elif path == "Levels/tile_manager.py":
                        from .tile_manager import TileManager
                    
                    tm = TileManager(self.number, level_height=self.height)
                    print(f"[Level {self.number}] TileManager cargado exitosamente desde {path}")
                    return tm
                except ImportError:
                    continue
                except Exception as e:
                    print(f"[Level {self.number}] Error cargando TileManager desde {path}: {e}")
                    continue
            
            print(f"[Level {self.number}] No se encontró TileManager")
            return None
            
        except Exception as e:
            print(f"[Level {self.number}] Error general cargando TileManager: {e}")
            return None
    
    def _create_parallax_layers(self):
        """Crea layers de parallax para el fondo - ADAPTADO PARA NIVEL GRANDE"""
        layers = []
        
        # Generar más elementos para nivel grande
        elements_count = {
            'far': 15,   # Más elementos lejanos
            'mid': 25,   # Más elementos medios
            'near': 35   # Más elementos cercanos
        }
        
        # Layer 1 - Muy lejano
        layers.append({
            'color': tuple(min(255, c + 30) for c in self.theme['bg']),
            'speed': 0.2,
            'offset': 0,
            'elements': self._generate_background_elements(elements_count['far'], 'far')
        })
        
        # Layer 2 - Medio
        layers.append({
            'color': tuple(min(255, c + 15) for c in self.theme['bg']),
            'speed': 0.5,
            'offset': 0,
            'elements': self._generate_background_elements(elements_count['mid'], 'mid')
        })
        
        # Layer 3 - Cercano
        layers.append({
            'color': self.theme['bg'],
            'speed': 0.8,
            'offset': 0,
            'elements': self._generate_background_elements(elements_count['near'], 'near')
        })
        
        return layers
    
    def _generate_background_elements(self, count, depth):
        """Genera elementos decorativos para el fondo - ADAPTADO PARA NIVEL GRANDE"""
        elements = []
        
        # Tamaño según profundidad
        size_range = {
            'far': (10, 30),
            'mid': (20, 50),
            'near': (30, 80)
        }
        
        # Distribuir elementos a lo largo de toda la altura del nivel
        for i in range(count):
            elements.append({
                'x': random.randint(0, SCREEN_WIDTH * 2),  # Más ancho
                'y': random.randint(-200, self.height + 200),  # Distribuir en toda la altura
                'size': random.randint(*size_range[depth]),
                'type': self.number
            })
        
        return elements
    
    def _generate(self):
        """Genera TODA la estructura del nivel - VERSIÓN MÁS GRANDE"""
        
        print(f"[Level {self.number}] Generando nivel ÉPICO de {self.height}px...")
        
        # Usar TileManager si está disponible
        if self.use_tiles and self.tile_manager:
            print(f"[Level {self.number}] Usando TileManager con tilesets")
            self.tile_platforms = self.tile_manager.get_platforms()
            
            # Obtener plataforma final del tile manager
            tile_final = self.tile_manager.get_final_platform()
            
            # Crear plataforma final estilo castillo
            if tile_final and hasattr(tile_final, 'x') and hasattr(tile_final, 'y'):
                print(f"[Level] Creando CastlePlatform sobre tile final")
                castle_platform = CastlePlatform(
                    tile_final.x,
                    tile_final.y - 60,  # Más arriba
                    240,  # Más ancha
                    self.number
                )
                castle_platform.is_final = True
                self.platforms.append(castle_platform)
                self.final_platform = castle_platform
                
                # BANDERA DE VICTORIA MÁS GRANDE
                flag_x = castle_platform.x - 90
                flag_y = castle_platform.y - 80
                victory_flag = VictoryFlag(flag_x, flag_y, self.number)
                victory_flag.scale = 1.5  # Bandera más grande
                self.flags.append(victory_flag)
            
            # Añadir plataformas móviles extras para nivel grande
            self._add_extra_moving_platforms()
        else:
            # SISTEMA ORIGINAL MODIFICADO PARA NIVEL GRANDE
            print(f"[Level {self.number}] Usando sistema de plataformas original (mejorado)")
            self._generate_extended_platforms()
        
        # GENERAR ELEMENTOS - MÁS Y MEJOR DISTRIBUIDOS
        print(f"[Level {self.number}] Generando enemigos y power-ups...")
        self._generate_bats()
        self._generate_traps()
        self._generate_rocks()
        
        # Rayos solo en nivel 3
        if self.number == 3:
            self._generate_lightning()
        
        # Generar power-ups (¡IMPORTANTE!)
        self._generate_powerups_mejorado()
        
        # Añadir drones en niveles altos
        if self.number >= 2:
            self._generate_drones()
        
        print(f"[Level {self.number}] ¡Generación completada!")
        print(f"  - Altura total: {self.height}px")
        print(f"  - {len(self.tile_platforms)} tiles")
        print(f"  - {len(self.platforms)} plataformas especiales")
        print(f"  - {len(self.enemies)} enemigos")
        print(f"  - {len(self.powerups)} power-ups")
        print(f"  - {len(self.flags)} banderas")
    
    def _generate_extended_platforms(self):
        """Genera plataformas usando sistema original EXTENDIDO"""
        # ============================================
        # 🏁 PLATAFORMA INICIAL (spawn seguro)
        # ============================================
        spawn_platform = Platform(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            180,  # Más ancha
            self.number
        )
        spawn_platform.is_spawn = True
        self.platforms.append(spawn_platform)
        
        current_y = SCREEN_HEIGHT - 100
        
        # ============================================
        # 📊 PLATAFORMAS NORMALES - MÁS Y MEJOR ESPACIADAS
        # ============================================
        platform_count = self.config['platforms']
        
        for i in range(1, platform_count + 1):
            # Variar el espaciado vertical para crear secciones
            if i % 5 == 0:
                # Cada 5 plataformas, hacer un salto más grande
                current_y -= PLATFORM_VERTICAL_SPACING * 1.5
            else:
                current_y -= PLATFORM_VERTICAL_SPACING
            
            # Posición horizontal variada
            if i % 3 == 0:
                # Plataformas a la izquierda
                x = random.randint(PLATFORM_WIDTH + 50, SCREEN_WIDTH // 2 - 50)
            elif i % 3 == 1:
                # Plataformas a la derecha
                x = random.randint(SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH - PLATFORM_WIDTH - 50)
            else:
                # Plataformas en el centro
                x = random.randint(SCREEN_WIDTH // 2 - 100, SCREEN_WIDTH // 2 + 100)
            
            # Ancho según nivel y posición
            if i < platform_count * 0.3:  # Primera parte
                width = random.randint(160, 200)
                move_chance = 0.1
            elif i < platform_count * 0.7:  # Parte media
                width = random.randint(140, 180)
                move_chance = 0.25
            else:  # Parte final
                width = random.randint(120, 160)
                move_chance = 0.4
            
            # Decidir tipo de plataforma
            if random.random() < move_chance:
                platform = MovingPlatform(
                    x, current_y, width, self.number,
                    move_range=random.randint(100, 200),
                    speed=random.uniform(1.0, 3.0)
                )
            else:
                platform = Platform(x, current_y, width, self.number)
            
            # Marcar plataformas difíciles en la parte superior
            if i > platform_count * 0.6:
                platform.is_difficult = True
            
            self.platforms.append(platform)
        
        # ============================================
        # 🏰 PLATAFORMA FINAL CASTILLO (EN LA CIMA)
        # ============================================
        final_platform_y = current_y - PLATFORM_VERTICAL_SPACING * 2
        
        final_platform = CastlePlatform(
            SCREEN_WIDTH // 2,
            final_platform_y,
            280,  # Más ancha
            self.number
        )
        final_platform.is_final = True
        self.platforms.append(final_platform)
        self.final_platform = final_platform
        
        # ============================================
        # BANDERA DE VICTORIA (MÁS GRANDE)
        # ============================================
        flag_x = SCREEN_WIDTH // 2 - 100
        flag_y = final_platform_y - 100
        victory_flag = VictoryFlag(flag_x, flag_y, self.number)
        victory_flag.scale = 1.8  # Bandera más grande para nivel grande
        self.flags.append(victory_flag)
    
    def _add_extra_moving_platforms(self):
        """Añade plataformas móviles extras para nivel grande"""
        if not self.tile_platforms:
            return
        
        # Encontrar plataformas adecuadas para convertir en móviles
        static_tiles = [p for p in self.tile_platforms if not hasattr(p, 'is_moving')]
        
        # Convertir algunas en móviles (20%)
        num_to_convert = max(3, len(static_tiles) // 5)
        for _ in range(num_to_convert):
            if static_tiles:
                tile = random.choice(static_tiles)
                static_tiles.remove(tile)
                
                # Crear plataforma móvil en esa posición
                moving_platform = MovingPlatform(
                    tile.x, tile.y, 
                    random.randint(100, 180),  # Ancho variable
                    self.number,
                    move_range=random.randint(80, 150),
                    speed=random.uniform(1.0, 2.0)
                )
                self.platforms.append(moving_platform)
    
    def _generate_bats(self):
        """Genera murciélagos - MEJOR DISTRIBUIDOS CON SEGURIDAD"""
        bats_to_generate = self.config['bats']
        all_platforms = self.get_all_platforms()
        
        if len(all_platforms) < 5:
            print(f"[Level] Muy pocas plataformas para generar murciélagos")
            return
        
        print(f"[Level] Generando {bats_to_generate} murciélagos...")
        
        # CORRECCIÓN: Evitar división por cero
        if bats_to_generate <= 0:
            print(f"[Level] No hay murciélagos para generar")
            return
        
        # Asegurar que siempre haya al menos 1 sección
        num_sections = max(2, bats_to_generate // 2)
        section_height = self.height / num_sections
        
        for i in range(bats_to_generate):
            # Seleccionar sección del nivel
            section_index = i % num_sections
            target_y = section_index * section_height + section_height / 2
            
            # Encontrar plataforma cercana a esa altura
            closest_platform = None
            min_distance = float('inf')
            
            for platform in all_platforms:
                if hasattr(platform, 'y'):
                    distance = abs(platform.y - target_y)
                    if distance < min_distance and distance < 300:
                        min_distance = distance
                        closest_platform = platform
            
            if closest_platform:
                # Posicionar murciélago
                offset_x = random.choice([-150, 150])
                x = closest_platform.x + offset_x
                y = closest_platform.y - random.randint(60, 120)
                
                # Configuración según nivel
                if self.number == 1:
                    pattern_width = random.randint(100, 180)
                    speed = random.uniform(1.5, 2.0)
                elif self.number == 2:
                    pattern_width = random.randint(120, 200)
                    speed = random.uniform(2.0, 2.5)
                else:
                    pattern_width = random.randint(150, 250)
                    speed = random.uniform(2.5, 3.0)
                
                bat = Bat(x, y, pattern_width)
                bat.speed = speed
                self.enemies.append(bat)
    
    def _generate_traps(self):
        """Genera trampas rotantes - MEJOR DISTRIBUIDAS"""
        traps_to_generate = self.config['traps']
        all_platforms = self.get_all_platforms()
        
        if len(all_platforms) < 4:
            return
        
        print(f"[Level] Generando {traps_to_generate} trampas rotantes...")
        
        for i in range(traps_to_generate):
            # Colocar trampas en espacios entre plataformas
            if i < len(all_platforms) - 1:
                platform1 = all_platforms[i]
                platform2 = all_platforms[i + 1]
                
                # Solo colocar trampa si hay espacio suficiente
                if abs(platform1.y - platform2.y) > 120:
                    x = (platform1.x + platform2.x) // 2
                    y = (platform1.y + platform2.y) // 2
                    
                    trap = RotatingTrap(x, y)
                    
                    # Aumentar velocidad de rotación según nivel
                    if self.number == 2:
                        trap.rotation_speed *= 1.3
                    elif self.number == 3:
                        trap.rotation_speed *= 1.6
                    
                    self.enemies.append(trap)
    
    def _generate_rocks(self):
        """Genera rocas que caen - MEJOR DISTRIBUIDAS"""
        rocks_to_generate = self.config['rocks']
        all_platforms = self.get_all_platforms()
        
        if len(all_platforms) < 3:
            return
        
        print(f"[Level] Generando {rocks_to_generate} rocas...")
        
        # Posicionar rocas en diferentes alturas
        height_sections = 4
        section_height = self.height / height_sections
        
        for i in range(rocks_to_generate):
            # Seleccionar sección
            section = i % height_sections
            target_min_y = section * section_height + 100
            target_max_y = (section + 1) * section_height - 100
            
            # Encontrar plataforma en esa sección
            suitable_platforms = []
            for platform in all_platforms:
                if hasattr(platform, 'y'):
                    if target_min_y < platform.y < target_max_y:
                        suitable_platforms.append(platform)
            
            if suitable_platforms:
                platform = random.choice(suitable_platforms)
                x = platform.x + random.randint(-80, 80)
                y = platform.y - random.randint(200, 350)
                
                rock = FallingRock(x, y)
                
                # Aumentar gravedad según nivel
                if self.number == 2:
                    rock.gravity *= 1.2
                elif self.number == 3:
                    rock.gravity *= 1.4
                
                self.enemies.append(rock)
    
    def _generate_lightning(self):
        """Genera rayos (solo nivel 3)"""
        print("[Level] Configurando sistema de rayos para nivel 3...")
        # Los rayos se generan dinámicamente en update
    
    def _generate_drones(self):
        """Genera drones iniciales para niveles 2 y 3, ajustado por dificultad"""
        try:
            # Cantidad base de drones según nivel
            base_count = {2: 2, 3: 3}[self.number]
            
            # Ajustar según dificultad
            difficulty_multiplier = {
                "easy": 0.5,
                "normal": 1.0,
                "hard": 1.5
            }.get(self.difficulty, 1.0)
            
            drone_count = max(1, int(base_count * difficulty_multiplier))
            all_platforms = self.get_all_platforms()
            
            print(f"[Level] Generando {drone_count} drones iniciales (difficulty: {self.difficulty})...")
            
            for i in range(drone_count):
                if len(all_platforms) > i * 2:
                    # Posicionar drones en la mitad superior del nivel
                    target_y = self.height * 0.3 + (i * 150)
                    
                    # Encontrar posición adecuada
                    x = random.randint(100, SCREEN_WIDTH - 100)
                    y = target_y
                    
                    # Ajustar parámetros según dificultad
                    patrol_range = 150
                    detection_range = 200
                    
                    if self.difficulty == "hard":
                        detection_range = 300
                        patrol_range = 200
                    elif self.difficulty == "easy":
                        detection_range = 150
                        patrol_range = 120
                    
                    drone = SurveillanceDrone(x, y, patrol_range=patrol_range, detection_range=detection_range)
                    
                    # Mejorar drones según nivel
                    if self.number == 3:
                        drone.detection_range += 50
                        drone.speed = 2.5 if self.difficulty == "hard" else 2.0
                    
                    self.enemies.append(drone)
        except ImportError as e:
            print(f"[Level] Error importando SurveillanceDrone: {e}")
    
    def _generate_powerups_mejorado(self):
        """VERSIÓN MEJORADA Y SEGURA para generar power-ups"""
        print("=" * 50)
        print(f"[DEBUG POWER-UPS] Iniciando generación...")
        
        powerups_to_generate = self.config.get('powerups', 0)
        print(f"[DEBUG] Config powerups: {powerups_to_generate}")
        print(f"[DEBUG] Config completa: {self.config}")
        
        if powerups_to_generate <= 0:
            print(f"[ERROR] ¡powerups_to_generate es {powerups_to_generate}!")
            print(f"[SOLUCIÓN] Forzando creación de 3 power-ups de prueba")
            powerups_to_generate = 3
        
        all_platforms = self.get_all_platforms()
        print(f"[DEBUG] Total plataformas disponibles: {len(all_platforms)}")
        
        # Tipos de power-ups
        all_types = ['shield', 'speed', 'zoom', 'combo', 'time_slow', 'magnet', 'double_jump']
        
        powerups_creados = 0
        
        # POWER-UP DE PRUEBA 1: En posición segura y visible
        x_test = SCREEN_WIDTH // 2
        y_test = SCREEN_HEIGHT - 150  # Justo encima del spawn
        try:
            powerup_test = PowerUp(x_test, y_test, 'shield')
            self.powerups.append(powerup_test)
            powerups_creados += 1
            print(f"[TEST] OK Power-up TEST creado en posición visible: ({x_test}, {y_test})")
        except Exception as e:
            print(f"[ERROR] No se pudo crear power-up de test: {e}")
        
        # POWER-UP DE PRUEBA 2: En el centro de la pantalla
        x_test2 = SCREEN_WIDTH // 2
        y_test2 = SCREEN_HEIGHT // 2
        try:
            powerup_test2 = PowerUp(x_test2, y_test2, 'speed')
            self.powerups.append(powerup_test2)
            powerups_creados += 1
            print(f"[TEST] OK Power-up TEST 2 creado en centro: ({x_test2}, {y_test2})")
        except Exception as e:
            print(f"[ERROR] No se pudo crear power-up de test 2: {e}")
        
        # Generar power-ups adicionales en plataformas
        for i in range(powerups_to_generate - 2):  # Ya creamos 2
            if len(all_platforms) > 4:
                # Seleccionar plataforma aleatoria
                platform = random.choice(all_platforms)
                
                # Verificar que sea una plataforma normal
                if (hasattr(platform, 'is_final') and platform.is_final) or \
                   (hasattr(platform, 'is_spawn') and platform.is_spawn):
                    continue  # Saltar plataformas especiales
                
                x = platform.x
                y = platform.y - 50  # Un poco arriba de la plataforma
                
                try:
                    powerup_type = random.choice(all_types)
                    powerup = PowerUp(x, y, powerup_type)
                    self.powerups.append(powerup)
                    powerups_creados += 1
                    print(f"[OK] Power-up {powerup_type} creado en ({x:.0f}, {y:.0f})")
                except Exception as e:
                    print(f"[ERROR] No se pudo crear power-up: {e}")
                    continue
        
        print(f"[DEBUG] Total power-ups creados: {powerups_creados}")
        print(f"[DEBUG] Power-ups en lista: {len(self.powerups)}")
        print("=" * 50)
    
    # ============================================
    # 🔧 MÉTODOS DE UTILIDAD
    # ============================================
    
    def get_all_platforms(self):
        """Retorna todas las plataformas"""
        all_platforms = []
        
        if self.use_tiles and self.tile_platforms:
            all_platforms.extend(self.tile_platforms)
        
        all_platforms.extend(self.platforms)
        
        return all_platforms
    
    def get_spawn_position(self):
        """Retorna la posición de spawn del jugador"""
        all_platforms = self.get_all_platforms()
        
        for platform in all_platforms:
            if hasattr(platform, 'is_spawn') and platform.is_spawn:
                return platform.x, platform.y - 150  # Más arriba
        
        return SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200
    
    # ============================================
    # 🔄 MÉTODOS DE ACTUALIZACIÓN
    # ============================================
    
    def update(self, dt, player_y, player_x=None):
        """
        Actualiza todos los elementos del nivel.
        
        Args:
            dt: Delta time
            player_y: Posición Y del jugador
            player_x: Posición X del jugador (para drones)
        """
        # Actualizar plataformas móviles
        for platform in self.platforms:
            if isinstance(platform, MovingPlatform):
                platform.update(dt)
            elif isinstance(platform, CastlePlatform):
                platform.update(dt)
        
        # Actualizar banderas
        for flag in self.flags:
            flag.update(dt)
        
        # Actualizar enemigos
        active_enemies = []
        for enemy in self.enemies:
            if enemy.active:
                # Pasar posición del jugador a drones
                if hasattr(enemy, '__class__') and enemy.__class__.__name__ == 'SurveillanceDrone':
                    enemy.update(dt, (player_x, player_y) if player_x else None)
                else:
                    enemy.update(dt)
                
                if hasattr(enemy, 'should_remove'):
                    if not enemy.should_remove():
                        active_enemies.append(enemy)
                else:
                    active_enemies.append(enemy)
        self.enemies = active_enemies
        
        # Actualizar power-ups
        for powerup in self.powerups:
            if not powerup.collected:
                powerup.update(dt)
        
        # Actualizar efectos
        active_effects = []
        for effect in self.effects:
            if effect.active:
                effect.update(dt)
                active_effects.append(effect)
        self.effects = active_effects
        
        # Spawning dinámico mejorado
        if player_y is not None:
            self._dynamic_spawning(player_y, dt, player_x)
        
        # Limpiar power-ups recolectados
        self.powerups = [p for p in self.powerups if not p.collected]
    
    def _dynamic_spawning(self, player_y, dt, player_x=None):
        """Spawning dinámico mejorado"""
        # ROCAS - más frecuentes cerca de la cima
        if self.final_platform:
            distance_to_top = abs(player_y - self.final_platform.y)
            
            # Base chance aumenta cerca de la cima
            rock_base_chance = {1: 0.003, 2: 0.004, 3: 0.005}[self.number]
            
            if distance_to_top < 800:  # Rango más amplio
                multiplier = 1.0 + (4.0 * (1 - distance_to_top / 800))
                rock_chance = rock_base_chance * multiplier
            else:
                rock_chance = rock_base_chance
            
            if random.random() < rock_chance * dt * 60:
                # Variar posición de caída
                if player_x:
                    x = player_x + random.randint(-200, 200)
                    x = max(60, min(SCREEN_WIDTH - 60, x))
                else:
                    x = random.randint(60, SCREEN_WIDTH - 60)
                
                y = player_y - random.randint(200, 500)
                rock = FallingRock(x, y)
                self.enemies.append(rock)
        
        # RAYOS - nivel 3
        if self.number == 3:
            if random.random() < 0.008 * dt * 60:  # Más frecuentes
                if player_x:
                    x = player_x + random.randint(-150, 150)
                    x = max(80, min(SCREEN_WIDTH - 80, x))
                else:
                    x = random.randint(80, SCREEN_WIDTH - 80)
                
                y = player_y - random.randint(50, 200)
                lightning = Lightning(x, y)
                self.enemies.append(lightning)
        
        # MURCIÉLAGOS EXTRA - en niveles altos
        if player_y < self.height * 0.4:  # En la mitad superior
            bat_chance = {1: 0.002, 2: 0.003, 3: 0.004}[self.number]
            
            if random.random() < bat_chance * dt * 60:
                if player_x:
                    x = player_x + random.choice([-250, 250])
                    x = max(100, min(SCREEN_WIDTH - 100, x))
                else:
                    x = random.randint(100, SCREEN_WIDTH - 100)
                
                y = player_y - random.randint(100, 300)
                
                # Configurar según nivel
                if self.number == 1:
                    patrol_range = random.randint(100, 180)
                elif self.number == 2:
                    patrol_range = random.randint(120, 200)
                else:
                    patrol_range = random.randint(150, 250)
                
                bat = Bat(x, y, patrol_range)
                bat.speed = random.uniform(2.0, 3.0)
                self.enemies.append(bat)
    
    # ============================================
    # 🎨 MÉTODOS DE DIBUJADO - ADAPTADOS PARA NIVEL GRANDE
    # ============================================
    
    def draw_background(self, surface, camera_offset):
        """Dibuja el fondo con parallax - ADAPTADO PARA NIVEL GRANDE"""
        surface.fill(self.theme['bg'])
        
        for layer in self.parallax_layers:
            layer['offset'] = camera_offset * layer['speed']
            
            for elem in layer['elements']:
                screen_y = elem['y'] - layer['offset']
                
                # Wrap around para nivel grande
                while screen_y < -elem['size'] * 2:
                    screen_y += self.height + elem['size'] * 4
                while screen_y > SCREEN_HEIGHT + elem['size'] * 2:
                    screen_y -= self.height + elem['size'] * 4
                
                self._draw_background_element(surface, elem, 
                                             int(elem['x']), 
                                             int(screen_y))
    
    def _draw_background_element(self, surface, elem, x, y):
        """Dibuja elemento decorativo - MEJORADO"""
        if self.number == 1:  # Bosque
            # Árbol más detallado
            pygame.draw.rect(surface, (101, 67, 33),
                           (x - elem['size']//6, y, 
                            elem['size']//3, elem['size']))
            
            # Copa del árbol con gradiente
            for i in range(3):
                radius = elem['size']//3 - i*2
                if radius > 0:
                    pygame.draw.circle(surface, (0, 80 + i*20, 0),
                                     (x, y - elem['size']//6), radius)
        
        elif self.number == 2:  # Caverna
            # Estalactita más detallada
            points = [
                (x, y - elem['size']//2),
                (x - elem['size']//3, y + elem['size']//2),
                (x + elem['size']//3, y + elem['size']//2)
            ]
            pygame.draw.polygon(surface, (80, 60, 50), points)
            pygame.draw.polygon(surface, (100, 80, 70), points, 2)
        
        elif self.number == 3:  # Tormenta
            # Nube más detallada
            for dx, dy, size in [(-elem['size']//3, 0, elem['size']//3),
                               (elem['size']//3, 0, elem['size']//3),
                               (0, -elem['size']//4, elem['size']//2)]:
                pygame.draw.circle(surface, (200, 200, 220),
                                 (x + dx, y + dy), size)
    
    def draw(self, surface, camera_offset):
        """Dibuja todos los elementos del nivel"""
        # Dibujar tiles primero
        if self.use_tiles and self.tile_manager:
            self.tile_manager.draw(surface, camera_offset)
        
        # Dibujar plataformas especiales
        for platform in self.platforms:
            platform.draw(surface, camera_offset)
        
        # Dibujar banderas
        for flag in self.flags:
            flag.draw(surface, camera_offset)
        
        # Dibujar power-ups (¡CON DEBUG!)
        powerups_dibujados = 0
        for i, powerup in enumerate(self.powerups):
            if not powerup.collected:
                try:
                    powerup.draw(surface, camera_offset)
                    powerups_dibujados += 1
                except Exception as e:
                    # Dibujo de emergencia
                    print(f"[DEBUG] Error dibujando power-up {i}: {e}")
                    screen_y = getattr(powerup, 'y', 0) - camera_offset
                    pygame.draw.circle(surface, (255, 0, 0), 
                                     (int(getattr(powerup, 'x', 100)), int(screen_y)), 20)
                    font = pygame.font.Font(None, 20)
                    text = font.render("P", True, (255, 255, 255))
                    surface.blit(text, (getattr(powerup, 'x', 100) - 5, screen_y - 10))
        
        # Dibujar enemigos
        for enemy in self.enemies:
            if enemy.active:
                enemy.draw(surface, camera_offset)
        
        # Dibujar efectos
        for effect in self.effects:
            if effect.active:
                effect.draw(surface, camera_offset)
    
    # ============================================
    # 🎮 MÉTODOS DE INTERACCIÓN
    # ============================================
    
    def check_flag_collision(self, player_rect):
        for flag in self.flags:
            if not flag.raised and player_rect.colliderect(flag.get_rect()):
                flag.raise_flag()
                return True
        return False
    
    def get_all_platforms_for_player(self):
        all_platforms = []
        
        if hasattr(self, 'tile_platforms'):
            all_platforms.extend(self.tile_platforms)
        
        all_platforms.extend(self.platforms)
        
        return all_platforms
    
    def check_player_collision(self, player_rect):
        for enemy in self.enemies:
            if enemy.active and player_rect.colliderect(enemy.get_rect()):
                return True
        return False