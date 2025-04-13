import datetime
import random

# Import the glyph generation function
from symbol_engine import generate_glyph

def perform_ritual(intention: str, store: dict) -> tuple[dict, dict]:
    """Handles the logic for performing a user-initiated ritual.
    
    Args:
        intention: The user's stated intention for the ritual.
        store: The current codex_store dictionary from the session.
        
    Returns:
        A tuple containing the new_glyph dictionary and the new_log dictionary.
    """
    print(f"Performing ritual for intention: '{intention}'")
    
    # 1. Generate the Glyph
    source = "Simulated Ritual" 
    glyph_data = generate_glyph(intention, source)
    
    # 2. Create the Log Entry
    timestamp = glyph_data['date'] # Use the timestamp from glyph generation for consistency
    log_text = f'Ritual performed with intention: "{intention}"'
    tags = ['ritual', 'glyph_generation']
    
    new_log = {
         'id': f'log_{timestamp}_{random.randint(1000, 9999)}', # Add random int to ensure uniqueness if multiple happen same second
         'text': log_text,
         'tags': tags,
         'linkedGlyphId': glyph_data['id'],
         'timestamp': timestamp
     }

    # 3. Prepare the Glyph dictionary (extract relevant parts from glyph_data)
    new_glyph = {
        'id': glyph_data['id'],
        'date': glyph_data['date'],
        'intention': glyph_data['intention'],
        'entropySource': glyph_data['entropySource'],
        'imageUrl': glyph_data['imageUrl'],
        'dream': glyph_data['dream']
    }

    print(f"Generated Glyph ID: {new_glyph['id']}")
    print(f"Created Log ID: {new_log['id']}")

    return new_glyph, new_log

# --- Helper Functions (if needed later) --- 
# Example: Maybe a function to validate intentions?
# def validate_intention(intention: str) -> bool:
#     return bool(intention and intention.strip()) 