"""
Command line runner for the Music Recommender Simulation
extended with a RAG (Retrieval-Augmented Generation) layer.

The flow:
1. Load songs from data/songs.csv
2. Score and rank them against user preferences (existing scoring engine)
3. For each top-K result:
   a. Retrieve a rich description from the knowledge base
   b. Send it (with the score reasons) to Claude
   c. Print both the original reasons AND the AI-generated explanation
"""

from src.recommender import load_songs, recommend_songs
from src.retriever import load_descriptions, get_description
from src.explainer import generate_explanation

def main() -> None:
    """
    Main function to run the music recommender simulation with RAG.
    """
    # 1. Load songs from the CSV file
    songs_path = "data/songs.csv"
    songs = load_songs(songs_path)

    if not songs:
        print("No songs were loaded. Exiting.")
        return

    # 2. Load song descriptions for the RAG layer (one-time load)
    descriptions = load_descriptions("data/song_descriptions.csv")
    print(f"Loaded {len(songs)} songs and {len(descriptions)} descriptions.\n")

    # 3. Define user taste profiles (kept from your original)
    taste_profile1 = {
        "favorite_genre": "indie pop",
        "favorite_mood": "chill",
        "target_energy": 0.6,
        "target_danceability": 0.7,
        "target_valence": 0.75,
        "target_tempo_bpm": 120,
        "likes_acoustic": False,
    }

    taste_profile2 = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "target_danceability": 0.6,
        "target_valence": 0.4,
        "target_tempo_bpm": 150,
        "likes_acoustic": False,
    }

    taste_profile3 = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_danceability": 0.8,
        "target_valence": 0.8,
        "target_tempo_bpm": 125,
        "likes_acoustic": False,
    }

    # Adversarial profiles to test edge cases
    adversarial_profile_1 = {
        "favorite_genre": "lofi",
        "favorite_mood": "any",
        "target_energy": 0.95,
        "target_danceability": 0.9,
        "target_valence": 0.8,
        "target_tempo_bpm": 140,
        "likes_acoustic": False,
    }

    adversarial_profile_2 = {
        "favorite_genre": "nonexistent_genre",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_danceability": 0.7,
        "target_valence": 0.5,
        "target_tempo_bpm": 160,
        "likes_acoustic": False,
    }

    adversarial_profile_3 = {
        "favorite_genre": "nonexistent_genre",
        "favorite_mood": "any",
        "target_energy": 0.5,
        "target_danceability": 0.5,
        "target_valence": 0.5,
        "target_tempo_bpm": 90,
        "likes_acoustic": True,
    }

    user_profiles = [
        taste_profile1,
        taste_profile2,
        taste_profile3,
        adversarial_profile_1,
        adversarial_profile_2,
        adversarial_profile_3,
    ]

    # 4. For each user profile, get and print recommendations with RAG explanations
    for i, profile in enumerate(user_profiles, 1):
        print("=" * 60)
        print(f"RECOMMENDATIONS FOR USER PROFILE #{i}")
        print(f"  Preferences: {profile}")
        print("=" * 60)

        recommendations = recommend_songs(profile, songs, k=5)

        if not recommendations:
            print("No suitable recommendations found for this profile.")
            print()
            continue

        for song, score, explanation in recommendations:
            # Original scoring output
            print(f"\n  Song:    {song['title']} by {song['artist']}")
            print(f"  Score:   {score:.2f}")
            print(f"  Reasons: {explanation}")

            # NEW: RAG-powered explanation
            description = get_description(int(song["id"]), descriptions)
            ai_explanation = generate_explanation(
                song=song,
                user_prefs=profile,
                score=score,
                reasons=explanation.split(", "),
                description=description,
            )
            print(f"  AI Says: {ai_explanation}")

        print("\n")


if __name__ == "__main__":
    main()
