# interpretation.py

# Placeholder for more sophisticated interpretation logic

def get_interpretation_and_suggestion(glyph: dict, archetype: str | None = None) -> dict:
    """Generates a simple interpretation and ritual suggestion based on glyph data.
    This is a placeholder and should be replaced with more advanced logic later.

    Args:
        glyph: The glyph dictionary.
        archetype: The user's archetype (optional, for future use).

    Returns:
        A dictionary containing 'interpretation' and 'ritualSuggestion' strings.
    """
    if not glyph:
        return {
            "interpretation": "Unable to interpret. Glyph data missing.",
            "ritualSuggestion": "Consider performing a ritual to generate a new glyph."
        }

    chakra = glyph.get('subtleEnergy', {}).get('chakra')
    ratio = glyph.get('harmonic', {}).get('ratio')
    note = glyph.get('harmonic', {}).get('note')
    intention = glyph.get('intention', 'an unknown intention')

    interpretation = f"This glyph, born from the intention '{intention}', resonates with the {chakra or 'unknown'} chakra ({note or '?'}) and the harmonic ratio {ratio or '?'}."
    suggestion = "Reflect on the patterns emerging. Consider how this resonance aligns with your current path."

    # --- Basic Rule Examples (Expand significantly later) ---
    if chakra == "Heart" and ratio:
         try:
             x, y = map(int, ratio.split(':'))
             if x > y:
                 interpretation += " It carries an overtone energy, suggesting outward expression of the heart."
                 suggestion = "Perhaps it is time to share something held within?"
             elif y > x:
                 interpretation += " It carries an undertone energy, suggesting inward reflection of the heart."
                 suggestion = "What inner truth of the heart seeks understanding?"
         except (ValueError, TypeError):
             pass # Ignore if ratio is not in expected format

    if chakra == "Throat":
        interpretation += " The Throat chakra signifies expression and communication."
        suggestion = "Is there something that needs to be spoken or created?"
        
    if ratio == "1:1":
        interpretation += " The 1:1 ratio speaks of balance, unity, and grounding."
        suggestion = "Find stillness and observe the equilibrium present in this moment."
        
    # --- Archetype specific (example) ---
    if archetype == 'Weaver' and ratio:
         interpretation += f" As a Weaver, this ratio ({ratio}) might represent a thread in a larger pattern you are discerning."

    # Fallback if no specific rules applied
    if suggestion == "Reflect on the patterns emerging. Consider how this resonance aligns with your current path.":
        if chakra == "Root": suggestion = "Focus on grounding this energy."
        elif chakra == "Third Eye": suggestion = "Open your intuition to the deeper meaning of this symbol."

    return {
        "interpretation": interpretation.strip(),
        "ritualSuggestion": suggestion.strip()
    }

# Example Usage:
if __name__ == "__main__":
    test_glyph_1 = {
        "id": "glyph_test1",
        "intention": "Seek clarity",
        "subtleEnergy": { "chakra": "Heart" },
        "harmonic": { "ratio": "5:4", "note": "F" }
    }
    test_glyph_2 = {
        "id": "glyph_test2",
        "intention": "Understand connection",
        "subtleEnergy": { "chakra": "Throat" },
        "harmonic": { "ratio": "3:2", "note": "G" }
    }
    test_glyph_3 = {
        "id": "glyph_test3",
        "intention": "Find balance",
        "subtleEnergy": { "chakra": "Root" },
        "harmonic": { "ratio": "1:1", "note": "C" }
    }
    
    result1 = get_interpretation_and_suggestion(test_glyph_1, archetype='Seeker')
    result2 = get_interpretation_and_suggestion(test_glyph_2, archetype='Weaver')
    result3 = get_interpretation_and_suggestion(test_glyph_3)

    print("--- Glyph 1 (Seeker) ---")
    print(f"Interpretation: {result1['interpretation']}")
    print(f"Suggestion: {result1['ritualSuggestion']}")
    print("\n--- Glyph 2 (Weaver) ---")
    print(f"Interpretation: {result2['interpretation']}")
    print(f"Suggestion: {result2['ritualSuggestion']}")
    print("\n--- Glyph 3 --- ")
    print(f"Interpretation: {result3['interpretation']}")
    print(f"Suggestion: {result3['ritualSuggestion']}") 