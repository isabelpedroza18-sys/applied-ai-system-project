"""
Explainer module for the RAG (Retrieval-Augmented Generation) layer.

This module is responsible for the "A" and "G" in RAG:
- Augmentation: building a prompt that combines the user's preferences,
  the song's metadata and score, and the retrieved description.
- Generation: calling Claude to generate a natural-language explanation
  of why this song is a good (or poor) match for the user.
"""

import os
from typing import Dict, List
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables (API key) from .env file once on import
load_dotenv()

# Initialize the Anthropic client once and reuse for all calls
_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Model and generation settings
MODEL = "claude-haiku-4-5"
MAX_TOKENS = 200  # ~2-3 sentences of output


def build_prompt(
    song: Dict,
    user_prefs: Dict,
    score: float,
    reasons: List[str],
    description: str,
) -> str:
    """
    Builds the augmented prompt string that gets sent to Claude.

    This is the "Augmentation" step in RAG: we combine the structured
    scoring data with the retrieved description to give the LLM rich
    context for generating a thoughtful explanation.
    """
    reasons_text = ", ".join(reasons) if reasons else "no specific feature matches"

    prompt = f"""You are a friendly music recommender explaining why a song was suggested to a user.

USER PREFERENCES:
- Favorite genre: {user_prefs.get('favorite_genre')}
- Favorite mood: {user_prefs.get('favorite_mood')}
- Target energy level: {user_prefs.get('target_energy')}
- Target danceability: {user_prefs.get('target_danceability')}
- Target valence (positivity): {user_prefs.get('target_valence')}
- Likes acoustic music: {user_prefs.get('likes_acoustic')}

RECOMMENDED SONG:
- Title: {song.get('title')}
- Artist: {song.get('artist')}
- Genre: {song.get('genre')}
- Mood: {song.get('mood')}
- Score: {score:.2f}
- Match reasons: {reasons_text}

SONG DESCRIPTION (from our knowledge base):
{description}

TASK:
Write a warm, natural 2-3 sentence explanation of why this song is a good match for the user. Reference specific things from the song description and connect them to the user's preferences. Do NOT mention the numeric score or the word "score." Do NOT use bullet points. Speak directly to the user as if you are recommending the song to a friend."""

    return prompt


def generate_explanation(
    song: Dict,
    user_prefs: Dict,
    score: float,
    reasons: List[str],
    description: str,
) -> str:
    """
    Generates a natural-language explanation by calling Claude.

    Returns:
        A 2-3 sentence explanation, or a graceful fallback message
        if the API call fails.
    """
    prompt = build_prompt(song, user_prefs, score, reasons, description)

    try:
        response = _client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        # Graceful fallback - don't crash the whole pipeline if the LLM is down
        return f"(AI explanation unavailable: {e})"


# Standalone test block - run with: python -m src.explainer
# if __name__ == "__main__":
#     print("Testing explainer module...\n")

#     # Sample data simulating what main.py would pass in
#     sample_song = {
#         "id": 1,
#         "title": "Sunrise City",
#         "artist": "Neon Echo",
#         "genre": "pop",
#         "mood": "happy",
#     }

#     sample_prefs = {
#         "favorite_genre": "pop",
#         "favorite_mood": "happy",
#         "target_energy": 0.8,
#         "target_danceability": 0.8,
#         "target_valence": 0.8,
#         "likes_acoustic": False,
#     }

#     sample_score = 0.92
#     sample_reasons = ["Genre match (+0.25)", "Mood match (+0.20)", "Energy is a close match (+0.15)"]
#     sample_description = (
#         "A bright, sun-soaked pop anthem from Neon Echo featuring bouncy synths "
#         "and a soaring chorus that feels like rolling down the highway with the windows down. "
#         "The track radiates pure summer optimism, perfect for road trips and beach days."
#     )

#     print("Calling Claude...\n")
#     explanation = generate_explanation(
#         sample_song, sample_prefs, sample_score, sample_reasons, sample_description
#     )
#     print("AI Explanation:")
#     print(explanation)