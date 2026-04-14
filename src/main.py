"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import (
    load_songs, 
    recommend_songs,
    create_chill_lofi_lover,
    create_intense_rock_fan
)


def main() -> None:
    print("=" * 70)
    print("[MUSIC RECOMMENDER SIMULATION]")
    print("=" * 70)
    
    songs = load_songs("data/songs.csv")
    
    # =======================================================================
    # PROFILE 1: Chill Lofi Lover
    # =======================================================================
    print("\n\n[PROFILE 1] Chill Lofi Lover")
    print("-" * 70)
    user_prefs_1 = create_chill_lofi_lover()
    print(f"Preferences: {user_prefs_1}")
    
    recommendations_1 = recommend_songs(user_prefs_1, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_1:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()
    
    # =======================================================================
    # PROFILE 2: Intense Rock Fan
    # =======================================================================
    print("\n\n[PROFILE 2] Intense Rock Fan")
    print("-" * 70)
    user_prefs_2 = create_intense_rock_fan()
    print(f"Preferences: {user_prefs_2}")
    
    recommendations_2 = recommend_songs(user_prefs_2, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_2:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()


if __name__ == "__main__":
    main()
