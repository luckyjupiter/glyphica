# chronomancer.py
import datetime

# Maps a musical note (string) to its corresponding Chakra name.
# Based on Hero's system mapping.
NOTE_TO_CHAKRA_MAPPING = {
    "C": "Root",
    "D": "Polarity",  # Sometimes Sacral
    "E": "Solar Plexus",
    "F": "Heart",
    "G": "Throat",
    "A": "Third Eye",
    "B": "Crown"
    # Add sharps/flats if needed, mapping them appropriately or defaulting
}

def get_lambdoma_ratio_for_time(timestamp: datetime.datetime) -> dict:
    """Derives a harmonic ratio and base musical note by mapping the timestamp
    to a conceptual 16x16 Lambdoma grid based on minutes and seconds.

    Args:
        timestamp: The timestamp to analyze.

    Returns:
        A dictionary containing the ratio, note, and indices:
        { 'ratio': 'x:y', 'note': 'C', 'x': 0, 'y': 15 }
    """
    if not isinstance(timestamp, datetime.datetime):
        print("Warning: get_lambdoma_ratio_for_time requires a datetime object. Using current time.")
        # Ensure timestamp is timezone-aware if converting, assuming UTC if naive
        try:
            timestamp = datetime.datetime.fromisoformat(timestamp)
            if timestamp.tzinfo is None:
                 timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)
        except (TypeError, ValueError):
             timestamp = datetime.datetime.now(datetime.timezone.utc)


    minutes = timestamp.minute
    seconds = timestamp.second

    # Map minute and second to 0-15 indices for a 16x16 grid
    x = minutes % 16  # Represents the 'overtone' or column index (0-15)
    y = seconds % 16  # Represents the 'undertone' or row index (0-15)

    # Derive the ratio: Use indices + 1 to get ratios like 1:1, 16:16 etc.
    ratio = f"{x + 1}:{y + 1}"

    # Derive a base musical note from one of the indices (e.g., x-axis)
    # Using a simple cyclical mapping to C, D, E, F, G, A, B
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    note = notes[x % 7]  # Use modulo 7 for the 7 standard notes

    return {
        "ratio": ratio,
        "note": note,
        "x": x,
        "y": y,
    }

def get_chakra_from_note(note: str) -> str | None:
    """Gets the Chakra name corresponding to a given musical note.
    Uses the NOTE_TO_CHAKRA_MAPPING.

    Args:
        note: The musical note (e.g., "C", "G").

    Returns:
        The corresponding Chakra name or None if not found.
    """
    # Basic lookup, could be expanded for sharps/flats later
    return NOTE_TO_CHAKRA_MAPPING.get(note.upper())

# Example Usage (can be run directly with `python chronomancer.py`):
if __name__ == "__main__":
    now = datetime.datetime.now(datetime.timezone.utc)
    # Test with string timestamp as well
    now_str = now.isoformat()
    
    cell = get_lambdoma_ratio_for_time(now)
    chakra = get_chakra_from_note(cell['note'])
    
    cell_from_str = get_lambdoma_ratio_for_time(now_str)
    chakra_from_str = get_chakra_from_note(cell_from_str['note'])

    print(f"Time (datetime obj): {now.minute}:{now.second}")
    print(f"Lambdoma Cell: x={cell['x']}, y={cell['y']}")
    print(f"Ratio: {cell['ratio']}, Note: {cell['note']}, Chakra: {chakra}")
    print("---")
    print(f"Time (ISO string): {now_str}")
    print(f"Lambdoma Cell: x={cell_from_str['x']}, y={cell_from_str['y']}")
    print(f"Ratio: {cell_from_str['ratio']}, Note: {cell_from_str['note']}, Chakra: {chakra_from_str}") 