"""
Retriever module for the RAG (Retrieval-Augmented Generation) layer.

This module is responsible for the "R" in RAG: retrieving rich song
descriptions from the knowledge base (data/song_descriptions.csv) so they
can be used to augment LLM prompts.
"""

import csv
from typing import Dict


def load_descriptions(csv_path: str = "data/song_descriptions.csv") -> Dict[int, str]:
    """
    Loads song descriptions from a CSV file into a dictionary.

    Args:
        csv_path: Path to the descriptions CSV file.

    Returns:
        A dictionary mapping song id (int) to description (str).
    """
    descriptions = {}
    with open(csv_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                song_id = int(row["id"])
                descriptions[song_id] = row["description"]
            except (ValueError, KeyError) as e:
                print(f"Skipping row due to error: {row} - {e}")
    return descriptions


def get_description(song_id: int, descriptions: Dict[int, str]) -> str:
    """
    Retrieves the description for a given song ID.

    Args:
        song_id: The id of the song to retrieve.
        descriptions: The dictionary returned by load_descriptions().

    Returns:
        The description string, or a fallback message if the ID isn't found.
    """
    return descriptions.get(
        song_id,
        "No additional description available for this song."
    )


# Standalone test block - run with: python -m src.retriever
if __name__ == "__main__":
    print("Testing retriever module...\n")
    descriptions = load_descriptions()
    print(f"Loaded {len(descriptions)} descriptions.\n")

    # Show a few sample lookups
    for test_id in [1, 13, 27, 999]:  # 999 is intentionally invalid
        desc = get_description(test_id, descriptions)
        print(f"Song ID {test_id}:")
        print(f"  {desc}\n")