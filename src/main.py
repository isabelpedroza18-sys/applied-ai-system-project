"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    """
    Main function to run the music recommender simulation.
    """
    # 1. Load songs from the CSV file
    songs_path = 'data/songs.csv'
    songs = load_songs(songs_path)

    if not songs:
        print("No songs were loaded. Exiting.")
        return

    # 2. Define two different user taste profiles
    taste_profile1 = {
        "favorite_genre": "indie pop",
        "favorite_mood": "chill",
        "target_energy": 0.6,
        "likes_acoustic": False
    }

    taste_profile2 = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False
    }
    #default user profile initially provided. I added likes acoustic as false.
    taste_profile3 = {
        "favorite_genre": "pop", 
        "favorite_mood": "happy", 
        "target_energy": 0.8,
        "likes_acoustic": False
    }

    # Adversarial profiles to test edge cases
    adversarial_profile_1 = {
        "favorite_genre": "lofi",
        "favorite_mood": "any", # A mood not in the dataset
        "target_energy": 0.95,  # Extremely high energy
        "likes_acoustic": False
    }

    adversarial_profile_2 = {
        "favorite_genre": "nonexistent_genre", # A genre that is not in songs.csv
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "likes_acoustic": False
    }

    adversarial_profile_3 = {
        "favorite_genre": "nonexistent_genre",
        "favorite_mood": "any",
        "target_energy": 0.5, # A neutral energy target
        "likes_acoustic": True
    }
    
    user_profiles = [taste_profile1, taste_profile2, taste_profile3, adversarial_profile_1, adversarial_profile_2, adversarial_profile_3]
    
    # 3. For each user profile, get and print recommendations
    for i, profile in enumerate(user_profiles, 1):
        print("="*50)
        print(f"RECOMMENDATIONS FOR USER PROFILE #{i}")
        print(f"  Preferences: {profile}")
        print("="*50)

        recommendations = recommend_songs(profile, songs, k=5)

        if not recommendations:
            print("No suitable recommendations found for this profile.")
        else:
            for song, score, explanation in recommendations:
                print(f"\n  Song:    {song['title']} by {song['artist']}")
                print(f"  Score:   {score:.2f}")
                print(f"  Reasons: {explanation}")
        
        print("\n")


if __name__ == "__main__":
    main()
