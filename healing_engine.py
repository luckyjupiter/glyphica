# healing_engine.py
import random
import math
from typing import Optional, Dict, List

# Import data and mappings
from healing_data import SYMPTOM_TO_HARMONICS, AFFIRMATION_MAP
from lambdoma_matrix import ( # Reuse helpers from lambdoma_matrix
    frequency_to_midi, 
    midi_to_note_name, 
    NOTE_TO_CHAKRA_MAPPING, 
    CHAKRA_TO_COLOR_MAPPING, 
    NOTES
)

DEFAULT_BASE_FREQ = 256.0 # Base frequency for ratio calculations if needed (e.g., C4)

# --- Helper Functions --- 

def get_note_details(note_name: str) -> dict:
    """Gets chakra and color for a given note name."""
    base_note = None
    if note_name and note_name != "Invalid":
        base_note = note_name.rstrip('0123456789#b')
    chakra = NOTE_TO_CHAKRA_MAPPING.get(base_note, "Unknown") if base_note else "Unknown"
    color = CHAKRA_TO_COLOR_MAPPING.get(chakra, CHAKRA_TO_COLOR_MAPPING['Unknown'])
    return {"chakra": chakra, "color": color}

def ratio_to_frequency(ratio_str: str, base_freq: float = DEFAULT_BASE_FREQ) -> Optional[float]:
    """Calculates frequency from a ratio string (e.g., "3:2") and base frequency."""
    try:
        num, den = map(int, ratio_str.split(':'))
        if den == 0: return None
        return base_freq * (num / den)
    except (ValueError, AttributeError, TypeError):
        return None

def parse_frequency_range(freq_range_str: str) -> Optional[float]:
    """Parses a string like "min-max" and returns the midpoint frequency."""
    try:
        min_freq, max_freq = map(float, freq_range_str.split('-'))
        return (min_freq + max_freq) / 2.0
    except (ValueError, AttributeError, TypeError):
        return None

def get_frequency_from_note(note_name: str) -> Optional[float]:
    """Calculates frequency from note name (e.g., C4 -> 261.63)."""
    try:
        note_part = note_name.upper().rstrip('0123456789')
        octave_part = note_name.lstrip(note_part)
        octave = int(octave_part)
        
        base_note = note_part.rstrip('#B') 
        semitones_from_C0 = NOTES.index(note_part) - 9 + (octave * 12) # C0 is MIDI 12, A4 is 69(index 9 + 4*12)
        # Correcting calculation: MIDI = 12 * (octave + 1) + note_index
        note_index_in_octave = NOTES.index(note_part)
        midi_note = 12 * (octave + 1) + note_index_in_octave
        
        # Calculate frequency based on A4=440Hz
        frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
        return frequency
    except (ValueError, IndexError, TypeError):
        return None

def get_frequency_from_ratio(ratio_str: str, base_freq: float = 256.0) -> Optional[float]:
    """Calculates frequency from a ratio string (e.g., '3:2')."""
    try:
        num, den = map(float, ratio_str.split(':'))
        if den == 0: return None
        return base_freq * (num / den)
    except (ValueError, ZeroDivisionError, TypeError):
        return None

# --- Main Engine Logic --- 

def get_healing_session_parameters(ailment: str) -> Optional[Dict]:
    """Gets the parameters for a healing session based on the selected ailment.

    Args:
        ailment: The name of the ailment (must be a key in SYMPTOM_TO_HARMONICS).

    Returns:
        A dictionary with session parameters (frequency, ratio, note, chakra, 
        color, affirmation, description) or None if ailment not found.
    """
    
    ailment_data = SYMPTOM_TO_HARMONICS.get(ailment)
    if not ailment_data:
        return None

    frequency = None
    ratio = None
    note = None
    chakra = None
    color = None
    affirmation = None

    # --- Determine primary harmonic parameter (Frequency > Ratio > Note) --- 
    
    # 1. Check for specific frequency or range
    freq_spec = ailment_data.get('frequencies')
    if isinstance(freq_spec, (int, float)): # Specific frequency given
        frequency = float(freq_spec)
    elif isinstance(freq_spec, str): # Range given (e.g., "64-128")
        frequency = parse_frequency_range(freq_spec)
    elif isinstance(freq_spec, list) and freq_spec: # List of frequencies
         frequency = random.choice(freq_spec) # Pick one randomly for now

    # 2. If no frequency, check for specific ratios
    if frequency is None:
        ratios = ailment_data.get('ratios')
        if isinstance(ratios, list) and ratios:
            # Special case: Endocrine Imbalance - requires two ratios, pick one for now
            # Phase II could handle playing both.
            if ailment == "Endocrine Imbalance / Hormonal Harmony" and len(ratios) >= 2:
                 # Prioritize 3:2 (Perfect Fifth) or pick first? Let's pick first for now.
                 ratio = ratios[0]
            else:
                 ratio = random.choice(ratios) # Pick one randomly
            frequency = ratio_to_frequency(ratio) # Calculate frequency from ratio
            
    # 3. If still no frequency, check for specific notes
    if frequency is None:
        notes = ailment_data.get('notes')
        if isinstance(notes, list) and notes:
            note = random.choice(notes) # Pick one randomly
            # Attempt to convert note name back to frequency (Requires more robust note parsing/mapping)
            # For now, we might need to pre-calculate frequencies for notes in healing_data.py
            # Placeholder: Use default frequency if note->freq fails
            # TODO: Implement robust note_name_to_frequency or store freq in data
            temp_midi = None # Placeholder
            if note == "G4": frequency = 384.0 # Specific case for trauma based on data
            elif note == "Eb4": frequency = 320.0 # Specific case for emotion based on data
            else: frequency = DEFAULT_BASE_FREQ # Fallback

    # Ensure we have a frequency if possible
    if frequency is None: 
        frequency = DEFAULT_BASE_FREQ # Ultimate fallback

    # --- Derive remaining parameters from the chosen frequency/note/ratio --- 
    midi_note_num = frequency_to_midi(frequency)
    if note is None and midi_note_num is not None:
        note = midi_to_note_name(midi_note_num)
    
    # Get Chakra and Color based on the derived note
    note_details = get_note_details(note)
    chakra = note_details['chakra']
    color = note_details['color']
    
    # If chakra wasn't determined by note, check chakra_focus list
    if chakra == "Unknown":
        chakra_focus_list = ailment_data.get('chakra_focus')
        if isinstance(chakra_focus_list, list) and chakra_focus_list:
            chakra = random.choice(chakra_focus_list) # Pick one from the focus list
            color = CHAKRA_TO_COLOR_MAPPING.get(chakra, CHAKRA_TO_COLOR_MAPPING['Unknown'])

    # --- Select Affirmation --- 
    # Prioritize ailment-specific affirmations
    affirmations = AFFIRMATION_MAP.get(ailment)
    if not affirmations:
        # Fallback to chakra-specific affirmations
        affirmations = AFFIRMATION_MAP.get(chakra)
    if not affirmations:
        # Ultimate fallback
        affirmations = AFFIRMATION_MAP.get("Unknown", ["Release and allow."])
        
    affirmation = random.choice(affirmations)

    # --- Construct result --- 
    session_params = {
        "ailment": ailment,
        "frequency": round(frequency, 2) if frequency else None,
        "ratio": ratio, # Store the ratio if explicitly used
        "note": note,
        "chakra": chakra,
        "color": color,
        "affirmation": affirmation,
        "description": ailment_data.get("description", "Harmonic entrainment session.")
    }
    
    return session_params

# Example Usage
if __name__ == "__main__":
    test_ailments = [
        "Heart Conditions / Circulation",
        "Kidneys / Detox Support",
        "Endocrine Imbalance / Hormonal Harmony",
        "Trauma Release / Addiction Support",
        "Emotional Imbalance",
        "NonExistentCondition"
    ]
    
    for ailment in test_ailments:
        params = get_healing_session_parameters(ailment)
        print(f"--- Parameters for: {ailment} ---")
        if params:
            print(f"  Frequency: {params['frequency']} Hz")
            print(f"  Ratio Used: {params['ratio']}")
            print(f"  Note Derived: {params['note']}")
            print(f"  Chakra: {params['chakra']}")
            print(f"  Color: {params['color']}")
            print(f"  Affirmation: '{params['affirmation']}'")
            print(f"  Description: {params['description']}")
        else:
            print("  Ailment not found in healing data.")
        print("---") 