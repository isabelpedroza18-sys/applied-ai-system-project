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
    Required by src/main.py
    """
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                row['id'] = int(row['id'])
                row['energy'] = float(row['energy'])
                row['tempo_bpm'] = float(row['tempo_bpm'])
                row['valence'] = float(row['valence'])
                row['danceability'] = float(row['danceability'])
                row['acousticness'] = float(row['acousticness'])
                songs.append(row)
            except (ValueError, KeyError) as e:
                print(f"Skipping row due to error: {row} - {e}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences and provides reasons."""
    score = 0.0
    reasons = []

    # Define weights for each feature
    weights = {
        "genre": 0.3,
        "mood": 0.3,
        "energy": 0.3,
        "acoustic": 0.1
    }

    # 1. Score Genre
    if song["genre"] == user_prefs["favorite_genre"]:
        genre_score = 1.0
        reasons.append(f"Genre match (+{weights['genre'] * genre_score:.2f})")
    else:
        genre_score = 0.0
    score += weights["genre"] * genre_score

    # 2. Score Mood
    if song["mood"] == user_prefs["favorite_mood"]:
        mood_score = 1.0
        reasons.append(f"Mood match (+{weights['mood'] * mood_score:.2f})")
    else:
        mood_score = 0.0
    score += weights["mood"] * mood_score

    # 3. Score Energy
    energy_score = 1 - abs(song["energy"] - user_prefs["target_energy"])
    if energy_score > 0.7: # Add reason only if it's a good match
        reasons.append(f"Energy is a close match (+{weights['energy'] * energy_score:.2f})")
    score += weights["energy"] * energy_score

    # 4. Score Acoustic Preference
    if user_prefs["likes_acoustic"]:
        acoustic_score = song["acousticness"]
        if acoustic_score > 0.6:
            reasons.append(f"Acoustic preference match (+{weights['acoustic'] * acoustic_score:.2f})")
    else:
        acoustic_score = 1 - song["acousticness"]
        if acoustic_score > 0.6: # Corresponds to low actual acousticness
            reasons.append(f"Acoustic preference match (+{weights['acoustic'] * acoustic_score:.2f})")
    score += weights["acoustic"] * acoustic_score
    
    # Ensure the final score is not above 1.0, just in case of rounding issues
    final_score = min(score, 1.0)

    return (final_score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores and ranks all songs to find the top k recommendations."""
    scored_songs = []
    
    # Loop through all songs and score them against user preferences
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        if reasons: # Only consider songs that have at least one matching reason
            explanation = ", ".join(reasons)
            scored_songs.append((song, score, explanation))

    # Sort the list of scored songs in descending order (highest score first)
    # The `lambda` function tells sorted() to use the score (the second item in each tuple) as the key.
    # `reverse=True` ensures the sort is from highest to lowest.
    sorted_songs = sorted(scored_songs, key=lambda item: item[1], reverse=True)
    
    # Return the top k results
    return sorted_songs[:k]
