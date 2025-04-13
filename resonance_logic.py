# resonance_logic.py

# Placeholder mapping for chakra activation
# Example: (Chakra1, Chakra2) -> DerivedChakra
# Use frozenset to make the key order-independent
CHAKRA_ACTIVATION_MAP = {
    frozenset(["Heart", "Throat"]): "Solar Plexus",
    frozenset(["Root", "Crown"]): "Third Eye", # Example
    frozenset(["Polarity", "Solar Plexus"]): "Heart", # Example
    # Add more combinations as defined by the system
}

# Placeholder mapping for note to chakra
# (Duplicate from chronomancer for now, consider centralizing later)
NOTE_TO_CHAKRA_MAPPING = {
    "C": "Root", "D": "Polarity", "E": "Solar Plexus",
    "F": "Heart", "G": "Throat", "A": "Third Eye", "B": "Crown"
}

def combine_ratios(ratio1: str, ratio2: str) -> str | None:
    """Calculates the combined ratio (multiplication). Placeholder for chord detection."""
    try:
        a, b = map(int, ratio1.split(':'))
        c, d = map(int, ratio2.split(':'))
        # Basic simplification could be added here (GCD)
        return f"{a * c}:{b * d}"
    except (ValueError, AttributeError, TypeError):
        return None # Invalid ratio format

def get_derived_chakra(chakra1: str, chakra2: str) -> str | None:
    """Finds the derived chakra based on the combination of two input chakras."""
    if not chakra1 or not chakra2:
        return None
    # Use frozenset for order-independent lookup
    combination = frozenset([chakra1, chakra2])
    return CHAKRA_ACTIVATION_MAP.get(combination)

# --- Helper to get chakra directly from glyph if needed ---
# (Assumes glyph has the structure defined previously)
def get_glyph_chakra(glyph: dict) -> str | None:
     if not glyph: return None
     return glyph.get('subtleEnergy', {}).get('chakra')

def get_glyph_ratio(glyph: dict) -> str | None:
     if not glyph: return None
     return glyph.get('harmonic', {}).get('ratio') 