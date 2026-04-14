from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5
    target_acousticness: float = 0.5
    genre_strictness: float = 0.6  # 0=flexible, 1=strict


# ============================================================================
# USER PROFILE EXAMPLES
# ============================================================================

def create_chill_lofi_lover() -> Dict:
    """
    Profile: User who loves relaxed, acoustic lofi music.
    Perfect for studying or sleeping.
    """
    return {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.60,
        "target_acousticness": 0.80,
        "acousticness_weight": 1.0,     # [UPDATED: was 1.5] to reduce acoustic-only bias
        "likes_acoustic": True,
        "genre_strictness": 0.7
    }


def create_intense_rock_fan() -> Dict:
    """
    Profile: User who loves energetic, intense rock music.
    Perfect for workouts or emotional expression.
    """
    return {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.50,
        "target_acousticness": 0.15,
        "acousticness_weight": 0.5,
        "likes_acoustic": False,
        "genre_strictness": 0.6
    }

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Returns list of song dictionaries with all attributes.
    """
    songs = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness'])
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []
    
    return songs

def score_song(song: Dict, user_prefs: Dict) -> float:
    """
    Calculates a recommendation score for a song based on user preferences.
    
    Updated Algorithm (v2):
    - Genre match: +1.5 (reduced from 2.0 to combat filter bubble)
    - Mood match: +1.0
    - Energy similarity: +1.5 × (1 - diff)
    - Energy precision bonus: +0.5 if diff < 0.05 (NEW)
    - Valence similarity: +0.75 × (1 - diff)
    - Acousticness similarity: +weight × (1 - diff)
      [Lofi: 1.0, Rock: 0.5]
    
    MAX SCORE: ~6.75
    """
    score = 0.0
    
    # LEVEL 1: Categorical matches (strong signals)
    # Genre match: +1.5 points (reduced from 2.0)
    if song['genre'].lower() == user_prefs['favorite_genre'].lower():
        score += 1.5
    
    # Mood match: +1.0 point
    if song['mood'].lower() == user_prefs['favorite_mood'].lower():
        score += 1.0
    
    # LEVEL 2: Weighted similarity (numeric - gradual)
    # Energy: Very important for both profiles
    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    energy_score = 1.5 * (1.0 - energy_diff)
    score += energy_score
    
    # Energy precision bonus: +0.5 if energy_diff < 0.05 (NEW)
    if energy_diff < 0.05:
        score += 0.5
    
    # Valence: Moderately important
    valence_diff = abs(song['valence'] - user_prefs['target_valence'])
    valence_score = 0.75 * (1.0 - valence_diff)
    score += valence_score
    
    # Acousticness: Varies by profile (weighted)
    acoustic_diff = abs(song['acousticness'] - user_prefs['target_acousticness'])
    acoustic_weight = user_prefs.get('acousticness_weight', 1.0)
    acoustic_score = acoustic_weight * (1.0 - acoustic_diff)
    score += acoustic_score
    
    return score


def get_explanation(song: Dict, user_prefs: Dict) -> str:
    """
    Generates a human-readable explanation of why a song was recommended.
    """
    reasons = []
    
    # Check for categorical matches
    if song['genre'].lower() == user_prefs['favorite_genre'].lower():
        reasons.append("Genre match")
    
    if song['mood'].lower() == user_prefs['favorite_mood'].lower():
        reasons.append("Mood match")
    
    # Check energy similarity
    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    if energy_diff < 0.05:
        reasons.append(f"Perfect energy ({song['energy']:.2f})")
    elif energy_diff < 0.15:
        reasons.append(f"Good energy match ({song['energy']:.2f})")
    
    # Check acousticness
    acoustic_diff = abs(song['acousticness'] - user_prefs['target_acousticness'])
    if acoustic_diff < 0.1:
        if song['acousticness'] > 0.7:
            reasons.append("High acousticness")
        elif song['acousticness'] < 0.2:
            reasons.append("Low acousticness (electric)")
    
    # Build explanation
    explanation = " + ".join(reasons) if reasons else "Good overall match"
    return explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Recommends top-k songs based on user preferences.
    
    Args:
        user_prefs: User preference dictionary
        songs: List of song dictionaries
        k: Number of recommendations to return (default 5)
    
    Returns:
        List of tuples: (song_dict, score, explanation_string)
    """
    if not songs:
        return []
    
    # Score all songs
    scored_songs = []
    for song in songs:
        score = score_song(song, user_prefs)
        explanation = get_explanation(song, user_prefs)
        scored_songs.append((song, score, explanation))
    
    # Sort by score (descending)
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top-k
    return scored_songs[:k]
