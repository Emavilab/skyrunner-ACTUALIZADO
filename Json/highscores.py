"""
highscores.py - Sistema de High Scores

Maneja el guardado y carga de las mejores puntuaciones.
"""

import json
import os
from datetime import datetime
from objects.constants import HIGH_SCORES_FILE, MAX_HIGH_SCORES

class HighScoreManager:
    """
    Gestor de puntuaciones altas.
    Guarda y carga puntuaciones en un archivo JSON.
    """
    
    def __init__(self):
        """Inicializa el gestor de high scores"""
        self.scores = []
        self.load_scores()
    
    def load_scores(self):
        """Carga las puntuaciones desde el archivo"""
        try:
            if os.path.exists(HIGH_SCORES_FILE):
                with open(HIGH_SCORES_FILE, 'r') as f:
                    self.scores = json.load(f)
            else:
                # Crear puntuaciones por defecto
                self.scores = []
        except Exception as e:
            print(f"Error al cargar puntuaciones: {e}")
            self.scores = []
    
    def save_scores(self):
        """Guarda las puntuaciones en el archivo"""
        try:
            with open(HIGH_SCORES_FILE, 'w') as f:
                json.dump(self.scores, f, indent=4)
        except Exception as e:
            print(f"Error al guardar puntuaciones: {e}")
    
    def add_score(self, player_name, score, level_reached):
        """
        Agrega una nueva puntuación.
        
        Args:
            player_name: Nombre del jugador
            score: Puntuación obtenida
            level_reached: Nivel alcanzado
        
        Returns:
            Posición en el ranking (None si no entró al top)
        """
        # Crear entrada
        entry = {
            'name': player_name,
            'score': score,
            'level': level_reached,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        # Agregar a la lista
        self.scores.append(entry)
        
        # Ordenar por puntuación (descendente)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Encontrar posición
        position = None
        for i, s in enumerate(self.scores):
            if s == entry:
                position = i + 1
                break
        
        # Mantener solo las mejores
        self.scores = self.scores[:MAX_HIGH_SCORES]
        
        # Guardar
        self.save_scores()
        
        return position if position and position <= MAX_HIGH_SCORES else None
    
    def is_high_score(self, score):
        """
        Verifica si una puntuación califica para el ranking.
        
        Args:
            score: Puntuación a verificar
        
        Returns:
            True si califica, False en caso contrario
        """
        if len(self.scores) < MAX_HIGH_SCORES:
            return True
        
        return score > self.scores[-1]['score']
    
    def get_scores(self):
        """
        Obtiene la lista de puntuaciones.
        
        Returns:
            Lista de diccionarios con puntuaciones
        """
        return self.scores
    
    def clear_scores(self):
        """Borra todas las puntuaciones"""
        self.scores = []
        self.save_scores()


# Instancia global
high_score_manager = HighScoreManager()

def add_high_score(player_name, score, level_reached):
    """
    Función auxiliar para agregar puntuación.
    
    Args:
        player_name: Nombre del jugador
        score: Puntuación
        level_reached: Nivel alcanzado
    
    Returns:
        Posición en el ranking
    """
    return high_score_manager.add_score(player_name, score, level_reached)

def is_high_score(score):
    """
    Verifica si es high score.
    
    Args:
        score: Puntuación a verificar
    
    Returns:
        Boolean
    """
    return high_score_manager.is_high_score(score)

def get_high_scores():
    """Obtiene las puntuaciones"""
    return high_score_manager.get_scores()
