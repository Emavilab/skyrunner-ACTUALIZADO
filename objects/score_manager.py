"""
score_manager.py - Manejo de records dinámicos
"""

import json
import os
from datetime import datetime

SCORES_FILE = "game_records.json"

class ScoreManager:
    def __init__(self):
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Carga los records desde archivo"""
        try:
            if os.path.exists(SCORES_FILE):
                with open(SCORES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[ScoreManager] Error cargando records: {e}")
        
        # Estructura por defecto si no existe el archivo
        return {
            "easy": [],
            "normal": [],
            "hard": []
        }
    
    def save_scores(self):
        """Guarda los records en archivo"""
        try:
            with open(SCORES_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[ScoreManager] Error guardando records: {e}")
            return False
    
    def add_score(self, difficulty, player_name, score, level, time_elapsed):
        """Añade un nuevo record"""
        if difficulty not in self.scores:
            self.scores[difficulty] = []
        
        new_entry = {
            "name": player_name[:15].upper(),
            "score": score,
            "level": level,
            "time": time_elapsed,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # Añadir y ordenar
        self.scores[difficulty].append(new_entry)
        self.scores[difficulty].sort(key=lambda x: x["score"], reverse=True)
        
        # Mantener solo top 10
        self.scores[difficulty] = self.scores[difficulty][:10]
        
        # Guardar
        self.save_scores()
        
        # Verificar si es el nuevo mejor score
        if self.scores[difficulty][0] == new_entry:
            return True  # Es el nuevo record
        return False  # No es record
    
    def get_top_scores(self, difficulty, limit=10):
        """Obtiene los mejores records para una dificultad"""
        if difficulty in self.scores:
            return self.scores[difficulty][:limit]
        return []
    
    def is_new_record(self, difficulty, score):
        """Verifica si un puntaje sería un nuevo record"""
        if difficulty not in self.scores or not self.scores[difficulty]:
            return True
        
        # Verificar si hay menos de 10 records o si supera el último
        if len(self.scores[difficulty]) < 10:
            return True
        
        return score > self.scores[difficulty][-1]["score"]
    
    def clear_scores(self):
        """Limpia todos los records"""
        self.scores = {
            "easy": [],
            "normal": [],
            "hard": []
        }
        self.save_scores()

# Instancia global
score_manager = ScoreManager()