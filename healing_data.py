# healing_data.py

# Data store for Hero Healing Device mappings
# Based on research anchors provided for GPHX-HERO-HEAL-01

# --- Symptom / Ailment to Harmonic Parameters --- 
# Values can include:
# - frequencies: List[float], or str range "min-max", or specific float
# - ratios: List[str] (Harmonic ratios like "3:2")
# - notes: List[str] (Musical notes like ['C4', 'G4'])
# - chakra_focus: List[str] (Primary chakras involved)
# - description: str (Brief explanation of the ailment/focus)

SYMPTOM_TO_HARMONICS = {
    # From Spec:
    "Heart Conditions / Circulation": {
        "frequencies": "64-128", # Lower octaves of C
        "ratios": ["1:2", "2:3", "3:4"], # Grounding ratios
        "notes": ["C2", "G2", "F2"], # Corresponding low notes
        "chakra_focus": ["Heart", "Root"],
        "description": "Lower octaves of C (root stability) for circulatory support."
    },
    "Kidneys / Detox Support": {
        "frequencies": "512-1024", # Higher C + G tones
        "ratios": ["1:1", "3:2"], # Corresponds to C & G in higher octave
        "notes": ["C5", "G5"], # C5=523Hz, G5=784Hz within range
        "chakra_focus": ["Solar Plexus", "Polarity"],
        "description": "Higher C + G frequencies for cleansing and detoxification."
    },
    "Glaucoma / Allergies": {
        "frequencies": "256-288", # Middle C region
        "ratios": ["1:1", "9:8"], # C, D ratios
        "notes": ["C4", "D4"], # Middle C area
        "chakra_focus": ["Third Eye", "Throat"],
        "description": "Middle C region frequencies for glandular calming (eyes/allergies)."
    },
    "Endocrine Imbalance / Hormonal Harmony": {
        "frequencies": None, # Focus on combined intervals
        "ratios": ["3:2", "5:4"], # Simultaneous overtone/undertone pairing (G and E relative to C)
        "notes": ["G4", "E4"], # Corresponding notes relative to C4=256Hz base
        "chakra_focus": ["Throat", "Third Eye", "Solar Plexus"],
        "description": "Harmonizing intervals (Fifth and Major Third) for endocrine balance."
    },
    "Trauma Release / Addiction Support": {
        "frequencies": 384, # Specific G4 frequency used by Hero (approx 384.0 Hz if C4=256)
        # Optional 192 Hz (G3) stacking can be added later
        "ratios": ["3:2"], # G relative to C
        "notes": ["G4"],
        "chakra_focus": ["Root", "Heart", "Crown"],
        "description": "Specific frequency (G=384Hz) used by Hero for deep trauma reset."
    },
    "Emotional Imbalance": {
        "frequencies": 320, # Specific E♭4 frequency (approx 311Hz if C4=256, 320 is close)
        "ratios": ["6:5"], # Minor Third (E♭ relative to C)
        "notes": ["Eb4"],
        "chakra_focus": ["Solar Plexus"],
        "description": "E♭ (approx 320Hz) for Solar Plexus regulation and emotional balance."
    },
    # Added from previous iteration:
     "General Well-being / Balance": {
        "frequencies": "256-512", 
        "ratios": ["1:1", "3:2", "4:3", "5:4", "6:5"], # Consonant intervals
        "notes": ["C4", "G4", "F4", "E4", "Eb4"], 
        "chakra_focus": ["Heart", "Solar Plexus"],
        "description": "A general balancing and harmonizing session."
    },
     "Psychic Interference / Pattern Breaking": {
        "frequencies": None, # Focus on intervals
        "ratios": ["15:16", "8:9"], # Dissonant intervals (Semitone, Major Second)
        "notes": ["B3", "D4"],
        "chakra_focus": ["Solar Plexus", "Crown"],
        "description": "Dissonant intervals to help break rigid patterns or external influences."
    },
}

# --- Affirmation Mapping --- 
# Based on Research Anchors + previous map
AFFIRMATION_MAP = {
    # Ailment specific (using Hero examples where possible)
    "Heart Conditions / Circulation": [
        "I restore the rhythm of my life.", # Added
        "My heart beats with strength and love.", # Modified
        "I restore the temple of my heart.",
        "Life energy flows freely through me."
    ],
    "Kidneys / Detox Support": [
        "I release what I no longer need.", # Added
        "My body cleanses and renews.", # Modified
        "I release that which no longer serves my highest good.",
        "My body's wisdom flows, cleanses, and renews."
    ],
    "Glaucoma / Allergies": [
        "I align to harmony within.", # Added
        "My vision clears, inside and out.",
        "I breathe freely and perceive with clarity.",
    ],
    "Endocrine Imbalance / Hormonal Harmony": [
        "My inner rhythms attune to universal harmony.",
        "I embrace balance and flow within my being.",
        "My body communicates with perfect wisdom."
    ],
    "Trauma Release / Addiction Support": [
        "I release old patterns with grace and compassion.",
        "I am safe, grounded, and centered in my being.",
        "I reclaim my sovereignty and inner peace."
    ],
    "Emotional Imbalance": [
        "I own my power with confidence and grace.", # Solar Plexus related
        "My emotions flow in balanced harmony.", # Added
        "I release emotional blocks."
    ],
    "Psychic Interference / Pattern Breaking": [
        "I stand strong in my own energy field.",
        "My mind is clear, my will is focused.",
        "I dissolve energetic patterns that limit me."
    ],
     "General Well-being / Balance": [
        "My body is the expression of my mind.", # Hero Quote
        "I picture myself as perfectly well.", # Hero Quote
        "I am centered, balanced, and whole.",
        "Harmony resonates through my mind, body, and spirit.",
        "I attune to the frequency of well-being."
    ],
    # Chakra specific (fallbacks)
    "Root": ["I am grounded, safe, and secure."],
    "Polarity": ["My creative energy flows freely and joyfully."],
    "Solar Plexus": ["I own my power with confidence and grace."],
    "Heart": ["I give and receive love unconditionally."],
    "Throat": ["I express my truth with clarity and conviction."],
    "Third Eye": ["I trust my intuition and inner wisdom."],
    "Crown": ["I am connected to Divine source and universal consciousness."],
    "Unknown": ["I am open to the messages of the universe."]
} 