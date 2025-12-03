"""
audio.py - Sistema de Audio ÉPICO
Con música de fondo, efectos temáticos y sonidos legendarios
"""

import pygame
import math
import random
from objects.constants import ENABLE_SOUND

class AudioManager:
    """
    Gestor de audio ÉPICO con música procedural y efectos inmersivos.
    """
    
    def __init__(self):
        """Inicializa el sistema de audio CON TODO EL SAZÓN"""
        self.enabled = ENABLE_SOUND
        
        if not self.enabled:
            print("[Audio] Audio deshabilitado en constants.py")
            return
        
        try:
            # Inicializar mixer con configuración PRO
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)
                pygame.mixer.init()
            
            # Configurar canales para mezcla profesional
            pygame.mixer.set_num_channels(16)  # Más canales para efectos simultáneos
            
            # ============================================
            # 🔊 VOLÚMENES ÉPICOS
            # ============================================
            self.sfx_volume = 0.85      # Efectos de sonido
            self.music_volume = 0.65    # Música de fondo
            self.ambience_volume = 0.4  # Ambiente/sonidos de fondo
            self.ui_volume = 0.9        # Sonidos de interfaz
            
            # ============================================
            # SISTEMA DE MÚSICA
            # ============================================
            self.music_active = True
            self.current_music = None
            self.music_timer = 0
            self.bpm = 120  # Pulsos por minuto para sincronización
            
            # ============================================
            # 🎮 CREAR TODOS LOS SONIDOS
            # ============================================
            self.sounds = {}
            self.music_tracks = {}
            self.ambience_sounds = {}
            
            self._create_sfx()          # Efectos de sonido
            self._create_music()        # Música de fondo
            self._create_ambience()     # Sonidos ambientales
            self._create_ui_sounds()    # Sonidos de interfaz
            
            # ============================================
            # 🔊 SISTEMA DE MEZCLA DINÁMICA
            # ============================================
            self.low_pass_filter = False
            self.reverb_active = False
            self.pitch_variation = 0.1
            
            print(f"AUDIO Audio ÉPICO inicializado:")
            print(f"   - {len(self.sounds)} efectos de sonido")
            print(f"   - {len(self.music_tracks)} pistas musicales")
            print(f"   - {len(self.ambience_sounds)} sonidos ambientales")
            print(f"   - {len(self._create_ui_sounds.__code__.co_names)} sonidos de UI")
            print(f"   - Volumen SFX: {self.sfx_volume}")
            print(f"   - Volumen Música: {self.music_volume}")
            
        except Exception as e:
            print(f"ERROR Error al inicializar audio: {e}")
            import traceback
            traceback.print_exc()
            self.enabled = False
    
    # ============================================
    # 🎮 CREACIÓN DE SONIDOS ÉPICOS
    # ============================================
    
    def _create_sfx(self):
        """
        Crea efectos de sonido ÉPICOS para el gameplay.
        """
        try:
            import numpy as np
            
            # ============================================
            # 🏃 SONIDOS DEL JUGADOR
            # ============================================
            # Salto (con variaciones)
            self.sounds['jump'] = self._create_jump_sound()
            self.sounds['jump_double'] = self._create_jump_sound(pitch=1.2)
            self.sounds['jump_power'] = self._create_jump_sound(pitch=1.5, duration=0.15)
            
            # Aterrizaje
            self.sounds['land'] = self._create_land_sound()
            self.sounds['land_hard'] = self._create_land_sound(pitch=0.8, duration=0.2)
            
            # ============================================
            # ⚔️ SONIDOS DE COMBATE
            # ============================================
            # Daño recibido
            self.sounds['damage'] = self._create_damage_sound()
            self.sounds['damage_shield'] = self._create_shield_hit()
            self.sounds['damage_critical'] = self._create_critical_hit()
            
            # Muerte
            self.sounds['death'] = self._create_death_sound()
            self.sounds['death_fall'] = self._create_fall_sound()
            
            # ============================================
            # ⚡ SONIDOS DE POWER-UPS
            # ============================================
            self.sounds['powerup_shield'] = self._create_powerup_sound(base_freq=440, type='shield')
            self.sounds['powerup_speed'] = self._create_powerup_sound(base_freq=660, type='speed')
            self.sounds['powerup_zoom'] = self._create_powerup_sound(base_freq=550, type='zoom')
            self.sounds['powerup_combo'] = self._create_powerup_sound(base_freq=880, type='combo')
            self.sounds['powerup_collect'] = self._create_collect_sound()
            
            # ============================================
            # 🎯 SONIDOS DE GAMEPLAY
            # ============================================
            self.sounds['platform_touch'] = self._create_platform_sound()
            self.sounds['combo_bonus'] = self._create_combo_sound()
            self.sounds['score_bonus'] = self._create_score_sound()
            self.sounds['level_complete'] = self._create_victory_fanfare()
            self.sounds['game_over'] = self._create_game_over_sound()
            
            # ============================================
            # 🦇 SONIDOS DE ENEMIGOS
            # ============================================
            self.sounds['enemy_spawn'] = self._create_enemy_spawn()
            self.sounds['enemy_hit'] = self._create_enemy_hit()
            self.sounds['bat_flap'] = self._create_bat_sound()
            self.sounds['rock_fall'] = self._create_rock_sound()
            self.sounds['lightning_strike'] = self._create_lightning_sound()
            
            # ============================================
            # 🌋 SONIDOS DE LAVA
            # ============================================
            self.sounds['lava_bubble'] = self._create_lava_bubble()
            self.sounds['lava_splash'] = self._create_lava_splash()
            self.sounds['lava_rise'] = self._create_lava_rise()
            
            print(f"OK {len(self.sounds)} efectos de sonido creados")
            
        except ImportError:
            print("ERROR NumPy no disponible - Usando sonidos básicos")
            self._create_basic_sounds()
        except Exception as e:
            print(f"ERROR Error al crear SFX: {e}")
            self._create_basic_sounds()
    
    def _create_music(self):
        """
        Crea música procedural para cada nivel.
        """
        try:
            import numpy as np
            
            # ============================================
            # MÚSICA POR NIVEL
            # ============================================
            # Nivel 1 - Bosque (melodía tranquila)
            self.music_tracks['level_1'] = self._create_forest_music()
            
            # Nivel 2 - Caverna (ritmo misterioso)
            self.music_tracks['level_2'] = self._create_cavern_music()
            
            # Nivel 3 - Tormenta (tensión épica)
            self.music_tracks['level_3'] = self._create_storm_music()
            
            # ============================================
            # 🎮 MÚSICA DE MENÚ
            # ============================================
            self.music_tracks['menu'] = self._create_menu_music()
            self.music_tracks['boss'] = self._create_boss_music()
            self.music_tracks['victory'] = self._create_ending_music()
            
            print(f"OK {len(self.music_tracks)} pistas musicales creadas")
            
        except Exception as e:
            print(f"ERROR Error al crear música: {e}")
    
    def _create_ambience(self):
        """
        Crea sonidos ambientales para inmersión.
        """
        try:
            import numpy as np
            
            # Ambiente de bosque (viento, pájaros)
            self.ambience_sounds['forest_wind'] = self._create_wind_sound()
            self.ambience_sounds['forest_birds'] = self._create_birds_sound()
            
            # Ambiente de caverna (goteo, ecos)
            self.ambience_sounds['cavern_drip'] = self._create_drip_sound()
            self.ambience_sounds['cavern_echo'] = self._create_echo_sound()
            
            # Ambiente de tormenta (viento fuerte, truenos)
            self.ambience_sounds['storm_wind'] = self._create_storm_wind()
            self.ambience_sounds['thunder'] = self._create_thunder_sound()
            
            # Ambiente general
            self.ambience_sounds['heartbeat'] = self._create_heartbeat()
            self.ambience_sounds['tension'] = self._create_tension_sound()
            
            print(f"OK {len(self.ambience_sounds)} sonidos ambientales creados")
            
        except Exception as e:
            print(f"ERROR Error al crear ambience: {e}")
    
    def _create_ui_sounds(self):
        """
        Crea sonidos para la interfaz de usuario.
        """
        try:
            import numpy as np
            
            self.sounds['ui_select'] = self._create_ui_sound(freq=440, duration=0.1)
            self.sounds['ui_confirm'] = self._create_ui_sound(freq=660, duration=0.15)
            self.sounds['ui_back'] = self._create_ui_sound(freq=330, duration=0.1)
            self.sounds['ui_hover'] = self._create_ui_sound(freq=550, duration=0.08)
            self.sounds['ui_error'] = self._create_ui_sound(freq=220, duration=0.2, wave='square')
            
            print(f"OK Sonidos de UI creados")
            
        except Exception as e:
            print(f"ERROR Error al crear UI sounds: {e}")
    
    def _create_basic_sounds(self):
        """
        Crea sonidos básicos como fallback.
        """
        # Sonidos simples usando beeps básicos
        basic_sounds = {
            'jump': self._simple_beep(440, 0.1),
            'damage': self._simple_beep(220, 0.2),
            'powerup': self._simple_beep(660, 0.15),
            'death': self._simple_beep(110, 0.3),
            'level_complete': self._simple_beep(880, 0.25),
        }
        
        self.sounds.update(basic_sounds)
        print(f"WARNING Sonidos básicos creados como fallback")
    
    # ============================================
    # MÉTODOS DE CREACIÓN DE SONIDOS ESPECÍFICOS
    # ============================================
    
    def _create_jump_sound(self, pitch=1.0, duration=0.12):
        """Crea sonido de salto con ascenso rápido"""
        import numpy as np
        
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        # Frecuencia que asciende rápidamente
        t = np.linspace(0, duration, samples, False)
        freq_sweep = np.linspace(440 * pitch, 660 * pitch, samples)
        
        # Generar onda
        phase = np.cumsum(2 * np.pi * freq_sweep / sample_rate)
        wave = np.sin(phase)
        
        # Envelope con ataque rápido y release
        envelope = np.ones(samples)
        attack = int(sample_rate * 0.01)
        release = int(sample_rate * 0.04)
        
        if attack > 0:
            envelope[:attack] = np.linspace(0, 1, attack)
        if release > 0:
            envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * 0.6
        
        # Añadir un poco de ruido para textura
        noise = np.random.normal(0, 0.1, samples)
        wave = wave * 0.8 + noise * 0.2
        
        return self._numpy_to_sound(wave)
    
    def _create_land_sound(self, pitch=1.0, duration=0.15):
        """Crea sonido de aterrizaje (impacto suave)"""
        import numpy as np
        
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        # Frecuencia que desciende
        t = np.linspace(0, duration, samples, False)
        freq = 330 * pitch * np.exp(-t * 8)
        
        # Onda con harmonics
        wave = np.zeros(samples)
        for harmonic in [1, 2, 3]:
            phase = np.cumsum(2 * np.pi * freq * harmonic / sample_rate)
            wave += np.sin(phase) * (1/harmonic)
        
        # Envelope de percusión
        envelope = np.exp(-t * 15)
        wave = wave * envelope * 0.4
        
        # Añadir ruido de impacto
        impact_noise = np.random.normal(0, 0.3, samples) * np.exp(-t * 30)
        wave = wave + impact_noise * 0.5
        
        return self._numpy_to_sound(wave)
    
    def _create_damage_sound(self):
        """Crea sonido de daño (desagradable)"""
        import numpy as np
        
        duration = 0.25
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)
        
        # Frecuencia modulada
        base_freq = 220
        mod_freq = 10
        freq = base_freq + 50 * np.sin(2 * np.pi * mod_freq * t)
        
        # Onda cuadrada distorsionada
        wave = np.sign(np.sin(2 * np.pi * freq * t))
        
        # Añadir clipping/distorsión
        wave = np.tanh(wave * 2)
        
        # Envelope
        envelope = np.ones(samples)
        attack = int(sample_rate * 0.02)
        release = int(sample_rate * 0.1)
        
        if attack > 0:
            envelope[:attack] = np.linspace(0, 1, attack)
        if release > 0:
            envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * 0.7
        
        return self._numpy_to_sound(wave)
    
    def _create_powerup_sound(self, base_freq=440, type='shield'):
        """Crea sonido de power-up épico"""
        import numpy as np
        
        duration = 0.3
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)
        
        # Barrido de frecuencia según tipo
        if type == 'shield':
            start_freq = base_freq
            end_freq = base_freq * 2
            wave_type = 'sine'
        elif type == 'speed':
            start_freq = base_freq * 1.5
            end_freq = base_freq * 3
            wave_type = 'saw'
        elif type == 'zoom':
            start_freq = base_freq
            end_freq = base_freq * 1.5
            wave_type = 'triangle'
        else:  # combo
            start_freq = base_freq * 0.5
            end_freq = base_freq * 2.5
            wave_type = 'square'
        
        # Barrido exponencial
        freq = start_freq * (end_freq/start_freq) ** (t/duration)
        
        # Generar onda según tipo
        phase = np.cumsum(2 * np.pi * freq / sample_rate)
        
        if wave_type == 'sine':
            wave = np.sin(phase)
        elif wave_type == 'saw':
            wave = 2 * (phase/(2*np.pi) - np.floor(0.5 + phase/(2*np.pi)))
        elif wave_type == 'triangle':
            wave = 2 * np.abs(2 * (phase/(2*np.pi) - np.floor(phase/(2*np.pi) + 0.5))) - 1
        else:  # square
            wave = np.sign(np.sin(phase))
        
        # Envelope con ping
        envelope = np.sin(np.pi * t/duration) ** 0.5
        wave = wave * envelope * 0.5
        
        # Añadir harmonics para brillo
        harmonics = np.sin(phase * 2) * 0.3 + np.sin(phase * 3) * 0.2
        wave = wave * 0.7 + harmonics
        
        return self._numpy_to_sound(wave)
    
    def _create_victory_fanfare(self):
        """Crea fanfarria de victoria"""
        import numpy as np
        
        duration = 1.5
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)
        wave = np.zeros(samples)
        
        # Acorde mayor (C, E, G)
        notes = [261.63, 329.63, 392.00, 523.25]  # C4, E4, G4, C5
        
        for i, freq in enumerate(notes):
            # Cada nota empieza en un tiempo diferente
            start_sample = int(i * 0.1 * sample_rate)
            if start_sample < samples:
                note_samples = samples - start_sample
                note_t = t[:note_samples]
                
                # Envelope para cada nota
                note_env = np.ones(note_samples)
                attack = int(0.05 * sample_rate)
                release = int(0.3 * sample_rate)
                
                if attack > 0:
                    note_env[:attack] = np.linspace(0, 1, attack)
                if release > 0 and note_samples > release:
                    note_env[-release:] = np.linspace(1, 0, release)
                
                # Generar nota
                note_phase = np.cumsum(2 * np.pi * freq * np.ones(note_samples) / sample_rate)
                note_wave = np.sin(note_phase) * note_env * 0.3
                
                wave[start_sample:start_sample + note_samples] += note_wave
        
        # Añadir percusión (tambor)
        kick_times = [0, 0.5, 1.0]
        for kick_time in kick_times:
            kick_sample = int(kick_time * sample_rate)
            if kick_sample < samples:
                kick_env = np.exp(-np.linspace(0, 10, min(1000, samples - kick_sample)))
                noise = np.random.normal(0, 0.5, len(kick_env))
                wave[kick_sample:kick_sample + len(kick_env)] += noise * kick_env * 0.4
        
        return self._numpy_to_sound(wave)
    
    def _create_forest_music(self):
        """Crea música tranquila para el bosque"""
        import numpy as np
        
        duration = 30  # 30 segundos de música
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)
        wave = np.zeros(samples)
        
        # Patrón de acordes simple
        chord_progression = [
            [261.63, 329.63, 392.00],  # C mayor
            [293.66, 369.99, 440.00],  # D menor
            [329.63, 415.30, 493.88],  # E menor
            [349.23, 440.00, 523.25],  # F mayor
        ]
        
        chord_duration = 4  # segundos por acorde
        chords_per_loop = len(chord_progression)
        
        for i in range(int(duration / chord_duration)):
            chord_idx = i % chords_per_loop
            chord = chord_progression[chord_idx]
            start_sample = int(i * chord_duration * sample_rate)
            end_sample = min(start_sample + int(chord_duration * sample_rate), samples)
            
            chord_samples = end_sample - start_sample
            if chord_samples <= 0:
                continue
            
            chord_t = t[start_sample:end_sample] - t[start_sample]
            
            for freq in chord:
                # Envelope suave para cada nota del acorde
                note_env = np.ones(chord_samples)
                attack = int(0.5 * sample_rate)
                release = int(0.5 * sample_rate)
                
                if attack > 0 and attack < chord_samples:
                    note_env[:attack] = np.linspace(0, 1, attack)
                if release > 0 and chord_samples > release:
                    note_env[-release:] = np.linspace(1, 0, release)
                
                # Generar nota con vibrato leve
                vibrato = 1 + 0.005 * np.sin(2 * np.pi * 5 * chord_t)
                phase = np.cumsum(2 * np.pi * freq * vibrato / sample_rate)
                note_wave = np.sin(phase) * note_env * 0.1
                
                wave[start_sample:end_sample] += note_wave
        
        # Añadir bajo
        bass_pattern = [261.63/2, 0, 293.66/2, 0]  # C, silencio, D, silencio
        for i in range(int(duration / 1)):  # Cambio cada segundo
            freq = bass_pattern[i % len(bass_pattern)]
            if freq > 0:
                start_sample = int(i * 1 * sample_rate)
                end_sample = min(start_sample + int(0.8 * sample_rate), samples)
                
                bass_samples = end_sample - start_sample
                if bass_samples > 0:
                    bass_t = t[start_sample:end_sample] - t[start_sample]
                    
                    bass_env = np.ones(bass_samples)
                    attack = int(0.05 * sample_rate)
                    release = int(0.2 * sample_rate)
                    
                    if attack > 0:
                        bass_env[:attack] = np.linspace(0, 1, attack)
                    if release > 0 and bass_samples > release:
                        bass_env[-release:] = np.linspace(1, 0, release)
                    
                    phase = np.cumsum(2 * np.pi * freq * np.ones(bass_samples) / sample_rate)
                    bass_wave = np.sin(phase) * bass_env * 0.15
                    
                    wave[start_sample:end_sample] += bass_wave
        
        # Normalizar
        wave = wave / np.max(np.abs(wave)) * 0.5
        
        return self._numpy_to_sound(wave)
    
    def _create_wind_sound(self):
        """Crea sonido de viento ambiental"""
        import numpy as np
        
        duration = 8.0
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        # Ruido rosa (más natural que blanco)
        white = np.random.normal(0, 1, samples)
        
        # Filtro paso bajo para hacerlo como viento
        b, a = self._butter_lowpass(500, sample_rate)
        from scipy import signal
        wind = signal.filtfilt(b, a, white)
        
        # Modulación de amplitud para efecto de ráfagas
        t = np.linspace(0, duration, samples, False)
        mod = 0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t + np.sin(2 * np.pi * 0.1 * t))
        
        wind = wind * mod
        
        # Fade in/out
        fade = int(0.5 * sample_rate)
        envelope = np.ones(samples)
        envelope[:fade] = np.linspace(0, 1, fade)
        envelope[-fade:] = np.linspace(1, 0, fade)
        
        wind = wind * envelope * 0.3
        
        return self._numpy_to_sound(wind)
    
    def _create_heartbeat(self):
        """Crea sonido de latido para tensión"""
        import numpy as np
        
        duration = 2.0  # Dos latidos
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        wave = np.zeros(samples)
        
        # Dos latidos
        for i, beat_time in enumerate([0.2, 1.0]):
            beat_sample = int(beat_time * sample_rate)
            beat_duration = 0.15
            beat_samples = int(beat_duration * sample_rate)
            
            if beat_sample + beat_samples < samples:
                beat_t = np.linspace(0, beat_duration, beat_samples, False)
                
                # Frecuencia que cae rápidamente
                freq = 80 * np.exp(-beat_t * 20)
                phase = np.cumsum(2 * np.pi * freq / sample_rate)
                
                # Onda con harmonics
                beat_wave = np.sin(phase) + 0.5 * np.sin(2 * phase) + 0.3 * np.sin(3 * phase)
                
                # Envelope
                beat_env = np.exp(-beat_t * 30)
                beat_wave = beat_wave * beat_env
                
                wave[beat_sample:beat_sample + beat_samples] += beat_wave * (0.8 if i == 0 else 0.6)
        
        return self._numpy_to_sound(wave)
    
    def _simple_beep(self, freq, duration):
        """Crea un beep simple (fallback)"""
        import numpy as np
        
        sample_rate = 22050
        samples = int(sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)
        wave = np.sin(2 * np.pi * freq * t)
        
        # Fade in/out
        fade = int(0.01 * sample_rate)
        if fade > 0:
            wave[:fade] *= np.linspace(0, 1, fade)
            wave[-fade:] *= np.linspace(1, 0, fade)
        
        return self._numpy_to_sound(wave)
    
    def _butter_lowpass(self, cutoff, fs, order=4):
        """Diseña un filtro paso bajo Butterworth"""
        import numpy as np
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        from scipy import signal
        b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
        return b, a
    
    def _numpy_to_sound(self, wave):
        """Convierte array numpy a pygame Sound"""
        import numpy as np
        
        # Normalizar
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val * 0.7
        
        # Convertir a 16-bit
        wave_16bit = (wave * 32767).astype(np.int16)
        
        # Estereo
        stereo = np.column_stack((wave_16bit, wave_16bit))
        
        # Crear Sound
        sound = pygame.mixer.Sound(buffer=stereo)
        sound.set_volume(self.sfx_volume)
        
        return sound
    
    # ============================================
    # 🎮 MÉTODOS DE CONTROL DE AUDIO
    # ============================================
    
    def play(self, sound_name, channel=None, volume=None, pitch_variation=True):
        """
        Reproduce un efecto de sonido con opciones avanzadas.
        
        Args:
            sound_name: Nombre del sonido
            channel: Canal específico (0-15)
            volume: Volumen específico (0.0-1.0)
            pitch_variation: Variación aleatoria de pitch
        """
        if not self.enabled or sound_name not in self.sounds:
            return
        
        try:
            sound = self.sounds[sound_name]
            
            # Aplicar variación de pitch si está activada
            if pitch_variation and self.pitch_variation > 0:
                import random
                pitch = 1.0 + random.uniform(-self.pitch_variation, self.pitch_variation)
                # Nota: pygame no soporta cambio de pitch directamente
                # Podrías implementar resampling si es crítico
            
            # Volumen específico o por defecto
            if volume is not None:
                current_volume = sound.get_volume()
                sound.set_volume(volume)
                sound.play()
                sound.set_volume(current_volume)  # Restaurar
            else:
                sound.play()
            
            # Debug opcional
            # print(f"AUDIO Reproduciendo: {sound_name}")
            
        except Exception as e:
            print(f"ERROR Error al reproducir {sound_name}: {e}")
    
    def play_music(self, track_name, loops=-1):
        """
        Reproduce música de fondo.
        
        Args:
            track_name: Nombre de la pista
            loops: Número de loops (-1 = infinito)
        """
        if not self.enabled or not self.music_active or track_name not in self.music_tracks:
            return
        
        try:
            # Detener música actual si hay
            pygame.mixer.music.stop()
            
            # Cargar y reproducir nueva pista
            sound = self.music_tracks[track_name]
            
            # Convertir Sound a música (necesita ser más largo)
            # Para música larga, necesitaríamos guardar como archivo temporal
            # Por ahora, usamos un approach simple
            
            print(f"🎶 Reproduciendo música: {track_name}")
            
            # Nota: pygame.mixer.music necesita archivos o bytes largos
            # Para este demo, usamos el sistema de sonidos
            
        except Exception as e:
            print(f"ERROR Error al reproducir música {track_name}: {e}")
    
    def play_ambience(self, ambience_name, loops=-1):
        """
        Reproduce sonido ambiental.
        
        Args:
            ambience_name: Nombre del sonido ambiental
            loops: Número de loops
        """
        if not self.enabled or ambience_name not in self.ambience_sounds:
            return
        
        try:
            sound = self.ambience_sounds[ambience_name]
            sound.set_volume(self.ambience_volume)
            
            # Reproducir en loop si se especifica
            if loops != 0:
                sound.play(loops=loops)
            
        except Exception as e:
            print(f"ERROR Error al reproducir ambience {ambience_name}: {e}")
    
    def stop_all(self):
        """Detiene todos los sonidos"""
        if not self.enabled:
            return
        
        try:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
        except:
            pass
    
    def stop_sound(self, sound_name):
        """Detiene un sonido específico"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        try:
            # Buscar canal donde se está reproduciendo
            for channel in range(pygame.mixer.get_num_channels()):
                if pygame.mixer.Channel(channel).get_busy():
                    if pygame.mixer.Channel(channel).get_sound() == self.sounds[sound_name]:
                        pygame.mixer.Channel(channel).stop()
        except:
            pass
    
    def set_sfx_volume(self, volume):
        """
        Ajusta el volumen de efectos de sonido.
        
        Args:
            volume: Volumen (0.0 a 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        
        if self.enabled:
            for name, sound in self.sounds.items():
                if not name.startswith('music_') and not name.startswith('ambience_'):
                    sound.set_volume(self.sfx_volume)
    
    def set_music_volume(self, volume):
        """Ajusta volumen de música"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_ambience_volume(self, volume):
        """Ajusta volumen ambiental"""
        self.ambience_volume = max(0.0, min(1.0, volume))
        
        if self.enabled:
            for sound in self.ambience_sounds.values():
                sound.set_volume(self.ambience_volume)
    
    def fade_out(self, duration_ms=1000):
        """Desvanece todos los sonidos"""
        if not self.enabled:
            return
        
        try:
            pygame.mixer.fadeout(duration_ms)
        except:
            pass
    
    def toggle_sound(self):
        """Activa/desactiva el sonido"""
        self.enabled = not self.enabled
        
        if not self.enabled:
            self.stop_all()
        
        print(f"🔊 Audio {'activado' if self.enabled else 'desactivado'}")
        return self.enabled
    
    def toggle_music(self):
        """Activa/desactiva la música"""
        self.music_active = not self.music_active
        
        if not self.music_active:
            pygame.mixer.music.stop()
        
        print(f"AUDIO Música {'activada' if self.music_active else 'desactivada'}")
        return self.music_active
    
    def update(self, dt):
        """Actualiza estado del audio (para música dinámica)"""
        if not self.enabled:
            return
        
        self.music_timer += dt
        
        # Cambios dinámicos basados en gameplay podrían ir aquí
        # Ej: subir tempo cuando sube la lava, etc.


# ============================================
# 🎮 INTERFAZ GLOBAL SIMPLIFICADA
# ============================================

# Instancia global
_audio_manager = None

def init_audio():
    """Inicializa el gestor de audio global"""
    global _audio_manager
    try:
        _audio_manager = AudioManager()
        return _audio_manager
    except Exception as e:
        print(f"ERROR Audio no disponible: {e}")
        _audio_manager = None
        return None

def play_sound(sound_name, **kwargs):
    """
    Función auxiliar para reproducir sonidos.
    
    Args:
        sound_name: Nombre del sonido
        **kwargs: Argumentos adicionales para play()
    """
    if _audio_manager:
        _audio_manager.play(sound_name, **kwargs)
    else:
        # Fallback silencioso
        pass

def play_music(track_name):
    """Reproduce música"""
    if _audio_manager:
        _audio_manager.play_music(track_name)

def play_ambience(ambience_name):
    """Reproduce sonido ambiental"""
    if _audio_manager:
        _audio_manager.play_ambience(ambience_name)

def stop_all_sounds():
    """Detiene todos los sonidos"""
    if _audio_manager:
        _audio_manager.stop_all()

def set_sfx_volume(volume):
    """Ajusta volumen de efectos"""
    if _audio_manager:
        _audio_manager.set_sfx_volume(volume)

def set_music_volume(volume):
    """Ajusta volumen de música"""
    if _audio_manager:
        _audio_manager.set_music_volume(volume)

def toggle_sound():
    """Activa/desactiva sonido"""
    if _audio_manager:
        return _audio_manager.toggle_sound()
    return False

def toggle_music():
    """Activa/desactiva música"""
    if _audio_manager:
        return _audio_manager.toggle_music()
    return False

# ============================================
# 🎯 SONIDOS ESPECÍFICOS PARA TU JUEGO
# ============================================

# Funciones helper para sonidos comunes del juego
def play_jump(double=False, powered=False):
    """Reproduce sonido de salto apropiado"""
    if not _audio_manager:
        return
    
    if powered:
        play_sound('jump_power')
    elif double:
        play_sound('jump_double')
    else:
        play_sound('jump')

def play_powerup(powerup_type):
    """Reproduce sonido de power-up según tipo"""
    if not _audio_manager:
        return
    
    sound_map = {
        'shield': 'powerup_shield',
        'speed': 'powerup_speed',
        'zoom': 'powerup_zoom',
        'combo': 'powerup_combo',
        'time_slow': 'powerup_collect',
        'magnet': 'powerup_collect',
        'double_jump': 'powerup_collect'
    }
    
    sound_name = sound_map.get(powerup_type, 'powerup_collect')
    play_sound(sound_name)

def play_damage(shield_hit=False, critical=False):
    """Reproduce sonido de daño"""
    if not _audio_manager:
        return
    
    if critical:
        play_sound('damage_critical')
    elif shield_hit:
        play_sound('damage_shield')
    else:
        play_sound('damage')

def play_level_music(level_number):
    """Reproduce música para el nivel actual"""
    if not _audio_manager:
        return
    
    track_name = f'level_{min(level_number, 3)}'
    if hasattr(_audio_manager, 'music_tracks') and track_name in _audio_manager.music_tracks:
        _audio_manager.play_music(track_name)

def play_environment_ambience(level_number):
    """Reproduce ambiente para el nivel actual"""
    if not _audio_manager:
        return
    
    if level_number == 1:
        play_ambience('forest_wind')
    elif level_number == 2:
        play_ambience('cavern_drip')
    elif level_number == 3:
        play_ambience('storm_wind')

def play_ui_sound(sound_type):
    """Reproduce sonido de interfaz"""
    if not _audio_manager:
        return
    
    sound_map = {
        'select': 'ui_select',
        'confirm': 'ui_confirm',
        'back': 'ui_back',
        'hover': 'ui_hover',
        'error': 'ui_error'
    }
    
    if sound_type in sound_map:
        play_sound(sound_map[sound_type])