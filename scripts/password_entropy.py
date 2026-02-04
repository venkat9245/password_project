#!/usr/bin/env python3
import math
import re
import sys
from collections import Counter

def calculate_entropy(password):
    if not password:
        return 0
    char_counts = Counter(password)
    length = len(password)
    entropy = 0
    for count in char_counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy

def assess_strength(password):
    entropy = calculate_entropy(password)
    length = len(password)
    char_types = sum([
        bool(re.search(r'[a-z]', password)),
        bool(re.search(r'[A-Z]', password)),
        bool(re.search(r'\d', password)),
        bool(re.search(r'[^a-zA-Z0-9]', password))
    ])
    
    score = min(length * 4 + char_types * 15, 100)
    if score >= 80: strength = "🟢 VERY STRONG"
    elif score >= 60: strength = "🟡 STRONG"
    elif score >= 40: strength = "🟠 MODERATE"
    else: strength = "🔴 WEAK"
    
    return {
        'length': length,
        'entropy': round(entropy, 2),
        'char_types': char_types,
        'score': score,
        'strength': strength
    }

if __name__ == "__main__":
    password = sys.argv[1] if len(sys.argv) > 1 else input("Password: ")
    result = assess_strength(password)
    print(f"\n🔍 Analysis for '{password}'")
    print(f"   Length: {result['length']}")
    print(f"   Entropy: {result['entropy']} bits")
    print(f"   Char Types: {result['char_types']}/4")
    print(f"   Score: {result['score']}/100")
    print(f"   {result['strength']}")
