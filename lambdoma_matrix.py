# lambdoma_matrix.py
import math
from typing import List, Dict, Optional

# Re-use Chakra mapping (consider centralizing later)
# TODO: Import directly if chronomancer.py is stable and finalized
NOTE_TO_CHAKRA_MAPPING = {
    "C": "Root", "D": "Polarity", "E": "Solar Plexus",
    "F": "Heart", "G": "Throat", "A": "Third Eye", "B": "Crown"
}

# Basic Chakra to Color mapping (Hex codes)
CHAKRA_TO_COLOR_MAPPING = {
    'Root': '#ef4444', # red-500
    'Polarity': '#f97316', # orange-500 (Sacral)
    'Solar Plexus': '#eab308', # yellow-500
    'Heart': '#22c55e', # green-500
    'Throat': '#3b82f6', # blue-500
    'Third Eye': '#6366f1', # indigo-500
    'Crown': '#a855f7', # purple-500
    'Unknown': '#6b7280' # gray-500
}

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def frequency_to_midi(freq: float) -> Optional[int]:
    """Converts frequency (Hz) to MIDI note number."""
    if freq <= 0: return None
    try:
        # MIDI note number for A4 (440 Hz) is 69
        return round(69 + 12 * math.log2(freq / 440.0))
    except ValueError:
        return None

def midi_to_note_name(midi_note: int) -> str:
    """Converts MIDI note number to note name (e.g., C4, F#5)."""
    if not (0 <= midi_note <= 127):
        return "Invalid"
    note_index = midi_note % 12
    octave = (midi_note // 12) - 1
    return f"{NOTES[note_index]}{octave}"

def get_lambdoma_matrix(base_freq: float = 256.0, grid_size: int = 16) -> List[List[Dict]]:
    """Generates the data for the Lambdoma matrix.

    Args:
        base_freq: The base frequency (Hz) for the 1:1 ratio, defaults to 256 Hz (C4).
        grid_size: The dimension of the square grid (e.g., 16 for 16x16).

    Returns:
        A list of lists, where each inner list is a row, and each item is a 
        dictionary (LambdomaCell) containing data for that cell.
    """
    if grid_size < 1: grid_size = 1
    matrix = []
    center_row = (grid_size -1) / 2.0 # Use float for quadrant calc
    center_col = (grid_size -1) / 2.0

    for r in range(grid_size): # 0 to grid_size-1
        row_data = []
        for c in range(grid_size): # 0 to grid_size-1
            # Use 1-based index for ratio calculation
            row_num = r + 1
            col_num = c + 1
            
            ratio_str = f"{row_num}:{col_num}"
            
            try:
                frequency = base_freq * (row_num / col_num)
            except ZeroDivisionError:
                 frequency = 0 # Or handle as infinity/error?

            midi_note = frequency_to_midi(frequency) if frequency > 0 else None
            note_name = midi_to_note_name(midi_note) if midi_note is not None else None
            
            # Get base note (without octave/sharp) for chakra mapping
            base_note = None
            if note_name and note_name != "Invalid":
                base_note = note_name.rstrip('0123456789#b')
                
            chakra = NOTE_TO_CHAKRA_MAPPING.get(base_note, "Unknown") if base_note else "Unknown"
            color = CHAKRA_TO_COLOR_MAPPING.get(chakra, CHAKRA_TO_COLOR_MAPPING['Unknown'])

            # Determine quadrant (1=TR, 2=TL, 3=BL, 4=BR)
            quadrant = 0
            if r < center_row and c >= center_col: quadrant = 1
            elif r < center_row and c < center_col: quadrant = 2
            elif r >= center_row and c < center_col: quadrant = 3
            elif r >= center_row and c >= center_col: quadrant = 4
            # Adjust for exact center lines if needed
            if r == center_row and c == center_col : quadrant = 0 # Center/Origin

            cell_data = {
                "row": r, # 0-indexed for array access
                "col": c, # 0-indexed for array access
                "ratioNum": (row_num, col_num),
                "ratioStr": ratio_str,
                "frequencyHz": round(frequency, 2) if frequency is not None else None,
                "midiNote": midi_note,
                "noteName": note_name,
                "chakra": chakra,
                "color": color,
                "quadrant": quadrant
            }
            row_data.append(cell_data)
        matrix.append(row_data)
        
    return matrix

# --- Helper to get a specific cell (optional) ---
def get_cell(row: int, col: int, matrix: List[List[Dict]]) -> Optional[Dict]:
    """Retrieves data for a specific cell from a pre-computed matrix."""
    if 0 <= row < len(matrix) and 0 <= col < len(matrix[row]):
        return matrix[row][col]
    return None

# Example Usage
if __name__ == "__main__":
    matrix_16 = get_lambdoma_matrix(grid_size=16)
    matrix_8 = get_lambdoma_matrix(grid_size=8, base_freq=440.0)
    
    print(f"Generated 16x16 Matrix (Base Freq 256 Hz)")
    # Print corner cells and center-ish cell for example
    print(f"Cell (0,0): {get_cell(0, 0, matrix_16)}")
    print(f"Cell (15,15): {get_cell(15, 15, matrix_16)}")
    print(f"Cell (0,15): {get_cell(0, 15, matrix_16)}")
    print(f"Cell (15,0): {get_cell(15, 0, matrix_16)}")
    print(f"Cell (7,7): {get_cell(7, 7, matrix_16)}") # Near center (index 7 is 8th row/col)
    print(f"Cell (8,8): {get_cell(8, 8, matrix_16)}") 
    
    print("\nGenerated 8x8 Matrix (Base Freq 440 Hz)")
    print(f"Cell (0,0): {get_cell(0, 0, matrix_8)}")
    print(f"Cell (3,4): {get_cell(3, 4, matrix_8)}") # Ratio 4:5
    print(f"Cell (7,7): {get_cell(7, 7, matrix_8)}") 