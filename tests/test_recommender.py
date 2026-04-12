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
        "likes_acoustic": False
    }
    song = {
        "genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.1
    }
    
    score, reasons = score_song(user_prefs, song)
    
    # With perfect matches on genre, mood, and energy, and a good acoustic score,
    # the total score should be very high (close to 1.0)
    assert score > 0.9
    assert "Genre match" in ", ".join(reasons)
    assert "Mood match" in ", ".join(reasons)
    assert "Energy is a close match" in ", ".join(reasons)


def test_score_song_mismatch():
    """
    Tests if a song that mismatches preferences gets a low score.
    """
    from src.recommender import score_song
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False
    }
    song = {
        "genre": "rock", "mood": "sad", "energy": 0.2, "acousticness": 0.9
    }
    
    score, reasons = score_song(user_prefs, song)
    
    # With no matches, the score should be very low.
    # It won't be 0 because of the energy and acoustic calculations, but it will be small.
    assert score < 0.3
    assert len(reasons) == 0


def test_score_song_acoustic_preference():
    """
    Tests the scoring logic for the 'likes_acoustic' preference.
    """
    from src.recommender import score_song
    
    # Case 1: User likes acoustic, song is highly acoustic
    user_likes_acoustic = {"likes_acoustic": True}
    acoustic_song = {"acousticness": 0.95}
    
    # We only need a subset of keys for this test
    acoustic_score_like = score_song(
        {"likes_acoustic": True, "favorite_genre": "", "favorite_mood": "", "target_energy": 0},
        {"acousticness": 0.95, "genre": "", "mood": "", "energy": 0}
    )[0]

    # Case 2: User dislikes acoustic, song is highly acoustic
    acoustic_score_dislike = score_song(
        {"likes_acoustic": False, "favorite_genre": "", "favorite_mood": "", "target_energy": 0},
        {"acousticness": 0.95, "genre": "", "mood": "", "energy": 0}
    )[0]

    # The score for the user who likes acoustic should be significantly higher
    assert acoustic_score_like > acoustic_score_dislike


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
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
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
