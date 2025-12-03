"""
save_score.py - Manejo de records del juego
"""

import json
import os
from datetime import datetime

SCORES_FILE = "game_scores.json"

def load_scores():
    """Carga las puntuaciones desde el archivo"""
    try:
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    
    # Estructura por defecto
    return {
        "easy": [],
        "normal": [],
        "hard": []
    }

def save_score(difficulty, player_name, score, level):
    """Guarda una nueva puntuación"""
    scores = load_scores()
    
    new_entry = {
        "name": player_name[:10],  # Limitar a 10 caracteres
        "score": score,
        "level": level,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    # Añadir a la lista de la dificultad
    if difficulty in scores:
        scores[difficulty].append(new_entry)
        # Ordenar por puntuación (mayor a menor)
        scores[difficulty].sort(key=lambda x: x["score"], reverse=True)
        # Mantener solo top 10
        scores[difficulty] = scores[difficulty][:10]
    else:
        scores[difficulty] = [new_entry]
    
    # Guardar en archivo
    try:
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
        return True
    except:
        return False

def is_new_record(difficulty, score):
    """Verifica si una puntuación es un nuevo record"""
    scores = load_scores()
    
    if difficulty not in scores or not scores[difficulty]:
        return True  # No hay records aún
    
    # Verificar si está en el top 10
    if len(scores[difficulty]) < 10:
        return True
    
    return score > scores[difficulty][-1]["score"]

def get_top_scores(difficulty, limit=10):
    """Obtiene las mejores puntuaciones para una dificultad"""
    scores = load_scores()
    
    if difficulty in scores:
        return scores[difficulty][:limit]
    return []