import datetime
import hashlib
import random
# --- Import Chronomancer Logic ---
from chronomancer import get_lambdoma_ratio_for_time, get_chakra_from_note
# --- End Import ---

def generate_glyph(intention: str, source: str = "Simulated Ritual") -> dict:
    """Generates a placeholder SVG glyph based on an intention and source,
       including subtle energy and harmonic data based on the timestamp.
    """
    # Create a timezone-aware datetime object first
    datetime_obj = datetime.datetime.now(datetime.timezone.utc)
    timestamp_str = datetime_obj.isoformat() # ISO format string for storage

    # --- Calculate Harmonic/Chakra Data ---
    lambdoma_data = get_lambdoma_ratio_for_time(datetime_obj)
    chakra = get_chakra_from_note(lambdoma_data['note'])
    # --- End Calculation ---

    # Create a stable but unique-ish ID based on intention and timestamp
    # Use a combination of intention hash and a bit of randomness for the visual
    seed_str = f"{intention}-{timestamp_str}-{random.random()}"
    hash_object = hashlib.sha256(seed_str.encode())
    hex_dig = hash_object.hexdigest()
    
    glyph_id = f"glyph_{hex_dig[:8]}"
    # Simple placeholder SVG - could be expanded later
    # Use parts of the hash to influence the visual
    hue = int(hex_dig[8:10], 16) * 360 // 256
    bg_color = f"hsl({hue}, 50%, 90%)"
    text_y = 50 + (int(hex_dig[10:12], 16) % 40 - 20) # Vary text position slightly

    svg = (
        f'<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg" style="background-color: {bg_color}; border: 1px solid #ccc;">'
        f'<text x="50%" y="{text_y}%" dominant-baseline="middle" text-anchor="middle" font-size="10" font-family="monospace" fill="#333">{glyph_id}</text>'
        f'<title>Intention: {intention}\nSource: {source}\nDate: {timestamp_str}</title>'
        f'</svg>'
    )
    
    return {
        "id": glyph_id,
        "imageUrl": svg, # This is the raw SVG string
        "intention": intention,
        "entropySource": source,
        "date": timestamp_str, # Use the ISO string for the date field
        "dream": source == "Dreaming Codex", # Automatically set dream status
        "subtleEnergy": {
            "chakra": chakra, # Populated by T001/E001
            "complementaryChakra": None, # To be filled by E001
            "overtoneOrUndertone": None, # Transmitter/Receiver - requires more logic
            "colorEmitted": None, # To be filled by T001
            "soundReceived": None, # Hz - To be filled by T001
            "psiChargeLevel": 0, # Starts at 0, per E002
        },
        "harmonic": {
            "ratio": lambdoma_data.get('ratio'), # Populated by T001
            "quadrant": None, # 1-4, To be filled by T001/G001 logic
            "midiNote": None, # To be filled by T001
            "frequencyHz": None, # To be filled by T001
            "harmonicAncestors": [], # To be filled by G001/S002 logic
            "harmonicDescendants": [], # To be filled by G001/S002 logic
            "note": lambdoma_data.get('note') # Store the derived note
        }
    } 