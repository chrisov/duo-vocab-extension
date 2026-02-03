#!/usr/bin/env python3
"""
Test script to view extracted Spanish vocabulary from Duolingo lessons
"""

import json
import os
from collections import Counter

VOCAB_FILE = "../config/spanish_words.json"

def view_vocabulary():
    if not os.path.exists(VOCAB_FILE):
        print("No vocabulary file found yet.")
        print("Complete some Duolingo lessons to start collecting words!")
        return
    
    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 60)
    print("DUOLINGO SPANISH VOCABULARY COLLECTION")
    print("=" * 60)
    print(f"\nTotal words captured: {data['total_count']}")
    print(f"Unique words: {len(set(w['word'] for w in data['words']))}")
    
    # Show word frequency
    print("\n" + "-" * 60)
    print("MOST COMMON WORDS:")
    print("-" * 60)
    word_counts = Counter(w['word'] for w in data['words'])
    for word, count in word_counts.most_common(20):
        print(f"  {word:30s} - seen {count} time(s)")
    
    # Show by exercise type
    print("\n" + "-" * 60)
    print("WORDS BY EXERCISE TYPE:")
    print("-" * 60)
    for exercise_type, words_list in data['by_exercise_type'].items():
        unique_words = set(w['word'] for w in words_list)
        print(f"\n{exercise_type}:")
        print(f"  Total encounters: {len(words_list)}")
        print(f"  Unique words: {len(unique_words)}")
        print(f"  Examples: {', '.join(list(unique_words)[:5])}")
    
    # Show recent words
    print("\n" + "-" * 60)
    print("RECENTLY ADDED WORDS (last 10):")
    print("-" * 60)
    for word_entry in data['words'][-10:]:
        print(f"  {word_entry['word']:20s} - {word_entry['exercise_type']:25s} - {word_entry.get('question', '')[:40]}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    view_vocabulary()
