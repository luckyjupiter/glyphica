import random
import datetime

from symbol_engine import generate_glyph # Assuming generate_glyph is in symbol_engine.py

# Configurable probability for dreaming
DREAM_PROBABILITY = 0.1 # 10% chance per check

def should_dream(store: dict) -> bool:
    """Determines probabilistically if the Codex should dream."""
    # Basic probability check
    should = random.random() < DREAM_PROBABILITY
    print(f"Checking if should dream: {should}")
    return should
    # Could add more complex logic later, e.g.:
    # - Based on time since last dream
    # - Based on number of glyphs/logs
    # - Based on specific patterns in the store

def generate_dream(store: dict) -> tuple[dict, dict]:
    """Generates a dream glyph and log entry.

    Args:
        store: The current codex_store dictionary from the session.

    Returns:
        A tuple containing the new_glyph dictionary and the new_log dictionary.
    """
    print("Codex is dreaming...")
    
    # 1. Determine the 'intention' or theme of the dream
    #    For now, use a placeholder. Could be derived from recent logs/glyphs later.
    dream_intention = "Internal Resonance" 
    source = "Dreaming Codex"

    # 2. Generate the Glyph using the symbol engine
    glyph_data = generate_glyph(dream_intention, source)
    glyph_data['dream'] = True # Explicitly set dream flag

    # 3. Create the Log Entry
    timestamp = glyph_data['date']
    log_text = f"The Codex dreamt a glyph representing: {dream_intention}"
    tags = ['dream', 'glyph_generation', 'system']
    
    new_log = {
        'id': f'log_{timestamp}_{random.randint(1000, 9999)}', # Add random int for uniqueness
        'text': log_text,
        'tags': tags,
        'linkedGlyphId': glyph_data['id'],
        'timestamp': timestamp
    }

    # 4. Prepare the Glyph dictionary
    new_glyph = {
        'id': glyph_data['id'],
        'date': glyph_data['date'],
        'intention': glyph_data['intention'], # Store the derived intention
        'entropySource': glyph_data['entropySource'],
        'imageUrl': glyph_data['imageUrl'],
        'dream': True # Ensure dream status is explicitly True
    }

    print(f"Generated Dream Glyph ID: {new_glyph['id']}")
    print(f"Created Dream Log ID: {new_log['id']}")

    return new_glyph, new_log 