# oracle_engine.py
import datetime
from typing import Optional

from flask import session # To get archetype

from symbol_engine import generate_glyph
from interpretation import get_interpretation_and_suggestion

def generate_oracle_reading(intention: str, timestamp: Optional[datetime.datetime] = None) -> dict | None:
    """Generates a glyph based on intention and time, then adds interpretation.

    Args:
        intention: The user's stated intention.
        timestamp: Optional timestamp (defaults to now). For future use or testing.

    Returns:
        An OracleReading dictionary containing the glyph and its interpretation,
        or None if generation fails.
    """
    # Note: symbol_engine.generate_glyph currently uses its own internal `now()`
    # If we need to pass a specific timestamp here, symbol_engine needs modification.
    # For now, we ignore the timestamp argument passed here and let symbol_engine use now().
    
    try:
        # 1. Generate the base glyph (includes harmonic data calculation internally)
        # We set the source to indicate it came from the Oracle
        glyph_data = generate_glyph(intention, source="Oracle Ritual")
        if not glyph_data:
            print("Error: Failed to generate glyph in symbol_engine.")
            return None

        # 2. Get interpretation and suggestion
        # Retrieve archetype from session
        store = session.get('codex_store', {})
        archetype = store.get('codex', {}).get('archetype')
        
        interp_data = get_interpretation_and_suggestion(glyph_data, archetype)

        # 3. Construct the OracleReading object
        reading = {
            'glyph': glyph_data,
            # Use the timestamp generated within the glyph data for consistency
            'timestamp': datetime.datetime.fromisoformat(glyph_data['date']),
            # Extract key harmonic signature details for easier access if needed
            'harmonicSignature': {
                'ratio': glyph_data.get('harmonic', {}).get('ratio'),
                'note': glyph_data.get('harmonic', {}).get('note'),
                'chakra': glyph_data.get('subtleEnergy', {}).get('chakra'),
            },
            'interpretation': interp_data['interpretation'],
            'ritualSuggestion': interp_data['ritualSuggestion']
        }
        return reading

    except Exception as e:
        print(f"Error generating oracle reading: {e}")
        import traceback
        traceback.print_exc()
        return None

# Example Usage (if run directly, needs Flask app context for session)
# if __name__ == "__main__":
#     # This would require mocking the session or running within app context
#     # from flask import Flask
#     # app = Flask(__name__)
#     # app.secret_key = 'testkey'
#     # with app.test_request_context('/'):
#     #     session['codex_store'] = {'codex': {'archetype': 'Weaver'}}
#     #     reading = generate_oracle_reading("Test oracle intention")
#     #     if reading:
#     #         print(reading) 