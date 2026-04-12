from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_score_song_perfect_match():
    """
    Tests if a song that perfectly matches user preferences gets a high score.
    """
    from src.recommender import score_song
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_danceability": 0.8,
        "target_valence": 0.9,
        "target_tempo_bpm": 120,
        "likes_acoustic": False
    }
    song = {
        "genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.1,
        "danceability": 0.8, "valence": 0.9, "tempo_bpm": 120
    }
    
    # Min/max tempo don't have to be exact for this test, just representative
    score, reasons = score_song(user_prefs, song, 60, 180)
    
    # With perfect matches on almost everything, score should be very high
    assert score > 0.9
    assert "Genre match" in ", ".join(reasons)
    assert "Mood match" in ", ".join(reasons)
    assert "Energy is a close match" in ", ".join(reasons)
    assert "Danceability is a close match" in ", ".join(reasons)
    assert "Valence (mood positivity) is a close match" in ", ".join(reasons)
    assert "Tempo is a close match" in ", ".join(reasons)


def test_score_song_mismatch():
    """
    Tests if a song that mismatches preferences gets a low score.
    """
    from src.recommender import score_song
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_danceability": 0.8,
        "target_valence": 0.9,
        "target_tempo_bpm": 120,
        "likes_acoustic": False
    }
    song = {
        "genre": "rock", "mood": "sad", "energy": 0.2, "acousticness": 0.9,
        "danceability": 0.2, "valence": 0.1, "tempo_bpm": 80
    }
    
    score, reasons = score_song(user_prefs, song, 60, 180)
    
    # With no matches, the score should be very low.
    assert score < 0.2
    assert len(reasons) == 0


def test_score_song_acoustic_preference():
    """
    Tests the scoring logic for the 'likes_acoustic' preference.
    """
    from src.recommender import score_song
    
    # Create a base user profile and song with neutral values
    base_prefs = {
        "favorite_genre": "a", "favorite_mood": "b", "target_energy": 0.5,
        "target_danceability": 0.5, "target_valence": 0.5, "target_tempo_bpm": 120
    }
    base_song = {
        "genre": "c", "mood": "d", "energy": 0.5, "danceability": 0.5,
        "valence": 0.5, "tempo_bpm": 120, "acousticness": 0.95
    }

    # Case 1: User likes acoustic
    prefs_like_acoustic = {**base_prefs, "likes_acoustic": True}
    score_like, _ = score_song(prefs_like_acoustic, base_song, 60, 180)

    # Case 2: User dislikes acoustic
    prefs_dislike_acoustic = {**base_prefs, "likes_acoustic": False}
    score_dislike, _ = score_song(prefs_dislike_acoustic, base_song, 60, 180)

    # The score for the user who likes the highly acoustic song should be higher
    assert score_like > score_dislike


def test_score_song_tempo_normalization():
    """
    Tests that tempo is normalized and scored correctly.
    """
    from src.recommender import score_song
    user_prefs = {
        "favorite_genre": "a", "favorite_mood": "b", "target_energy": 0.5,
        "target_danceability": 0.5, "target_valence": 0.5, "target_tempo_bpm": 100,
        "likes_acoustic": False
    }
    # Song with tempo close to target
    song_close_tempo = {
        "genre": "c", "mood": "d", "energy": 0.5, "danceability": 0.5,
        "valence": 0.5, "tempo_bpm": 105, "acousticness": 0.5
    }
    # Song with tempo far from target
    song_far_tempo = {**song_close_tempo, "tempo_bpm": 170}

    min_tempo, max_tempo = 60, 180

    score_close, _ = score_song(user_prefs, song_close_tempo, min_tempo, max_tempo)
    score_far, _ = score_song(user_prefs, song_far_tempo, min_tempo, max_tempo)

    # The song with the closer tempo should have a higher score
    assert score_close > score_far


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_danceability=0.8,
        target_valence=0.9,
        target_tempo_bpm=120,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_danceability=0.8,
        target_valence=0.9,
        target_tempo_bpm=120,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
