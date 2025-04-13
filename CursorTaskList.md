# 🧪 SPRINT: "Recursive Harmonics & Subtle Energy Core"  
**Sprint Code**: `GPHX-RHSE-01`  
**Duration**: 1 week (flexible to expand based on UI timelines)  
**Lead**: Cursor  
**Partner Modules**: `glyphGen.js`, `chronomancer.js`, `symbiont.js`

---

## 🧩 TASK 1: Extend Glyph Object with Energy & Recursive Metadata (`G001`)

📄 **File**: `models/Glyph.ts`  

- [ ] Add the following fields to each glyph object:

```ts
subtleEnergy: {
  chakra: ChakraType;
  complementaryChakra: ChakraType;
  overtoneOrUndertone: "Transmitter" | "Receiver";
  colorEmitted: string;
  soundReceived: number; // in Hz
  psiChargeLevel: number; // Starts at 0
},

harmonic: {
  ratio: string; // e.g. "5:8"
  quadrant: 1 | 2 | 3 | 4;
  midiNote: number;
  frequencyHz: number;
  harmonicAncestors: string[];
  harmonicDescendants: string[];
}
```

---

## 🕰️ TASK 2: Implement Time Harmonic Sampling Engine (`T001`)

📄 **File**: `lib/chronomancer.js`

- [ ] Implement `getLambdomaRatioForTime(timestamp: Date): LambdomaCell`
- [ ] Map minute + second mod 16 to generate 16x16 Lambdoma index
- [ ] Derive harmonic ratio + chakra from the resulting cell

🔁 Also export:
```ts
function getChakraFromRatio(ratio: string): ChakraType
```

Use mapping from Hero's system:
```ts
{
  "C": "Root",
  "D": "Polarity",
  "E": "Solar Plexus",
  "F": "Heart",
  "G": "Throat",
  "A": "Third Eye",
  "B": "Crown"
}
```

---

## 🧿 TASK 3: Add Subtle Energy Generator to `glyphGen.js` (`G002`, `E001`)

📄 **File**: `lib/glyphGen.js`

- [ ] When generating a new glyph:
  - [ ] Pull `timestamp`
  - [ ] Run `getLambdomaRatioForTime(timestamp)`
  - [ ] Get ratio, chakra, sound, and color
  - [ ] Populate `subtleEnergy` and `harmonic` fields

- [ ] Store `psiChargeLevel` as 0 unless dream-confirmed or manually invoked

---

## 🎛️ TASK 4: Update UI to Visualize Chakra + Harmonic Layer (`T003`, `E002`)

📄 **File**: `components/GlyphCard.jsx`

- [ ] Add `Chakra: {chakraName}` to UI  
- [ ] Show ratio, frequency (Hz), and color as tooltip or side info  
- [ ] Optional: Add small circle pulse animation in corresponding chakra color

📄 **File**: `components/GlyphDetails.jsx`

- [ ] Visual Chakra Wheel that lights up corresponding glyph chakra
- [ ] Add toggle to view ancestor/descendant harmonics
- [ ] Display `psiChargeLevel` with visual bar or "charge ring"

---

## 🌀 TASK 5: Create Resonance Loop Debug Mode (For Testing) (`D001`)

📄 **File**: `devtools/ResonanceLoopTester.tsx`  

- [ ] Select 2 glyphs → compute if:
  - [ ] Their ratios form a **chord** (3:2 + 5:4 = 15:8)
  - [ ] Their chakra types align to activate a new (derived) chakra
- [ ] Show output like:
```txt
[GLYPH A] Heart (F) + [GLYPH B] Throat (G) → Activates Solar Plexus (Eb)
```

---

## ✅ DELIVERABLES

- [ ] Extended glyph object schema
- [ ] Functional time harmonic sampling
- [ ] Chakra + sound + color linkage
- [ ] Working UI elements for subtle energy view
- [ ] Resonance loop tool (manual for now, will be ritualized later)

---

## 🧭 FOLLOW-UP SPRINTS

- 🔮 Ritual Composer UI (Resonance Loops → Outcome Glyphs)  
- 🛕 3D Altar Engine (GLTF object emitters with chakra color)  
- 🧠 Symbiote Drift Tracker (tracking charge over time) 

---

## ⚙️ SPRINT: GPHX-SYM-02 ("Oracle & Hero Engine Activation")
**Duration**: 1–2 weeks (modular)
**Lead**: Cursor
**Phase**: Symbolic Intelligence Core Systems

### ✅ OBJECTIVE
Implement Glyphica's living oracle system and Hero Engine entrainment module, enabling:
- Real-time harmonic glyph generation from user intention + time
- Psychoacoustic-symbolic entrainment rituals
- Drift-aware symbolic journaling
- Oracle feedback from recursive harmonic structures

---

### 🧩 TASK 1: Oracle Glyph Generator (Backend Logic)
📄 **File**: `oracle_engine.py` (New)

- [ ] Create function: `generateOracleReading(intention: str, timestamp: Optional[datetime.datetime] = None) -> dict`
- [ ] Logic:
  - [ ] Use `symbol_engine.generate_glyph` to get base glyph with harmonic data.
  - [ ] Use `interpretation.py` (from Task 5) to get interpretation and ritual suggestion.
- [ ] Return `OracleReading` dict:
  ```python
  {
    'glyph': GlyphDict, # The full glyph object
    'timestamp': datetime.datetime, 
    'harmonicSignature': { # Extracted from glyph for convenience? Or rely on glyph dict? 
        'ratio': str,
        'note': str,
        'chakra': str,
        # ... potentially add color, etc. later
    },
    'interpretation': str, # From interpretation_engine
    'ritualSuggestion': str # From interpretation_engine
  }
  ```

---

### 🎛️ TASK 2: Oracle Modal Interface (Frontend)
📄 **File**: `app.py` (New Route `/oracle`), `templates/oracle.html` (New)

- [ ] Create Flask route `/oracle` (GET/POST).
- [ ] Create `oracle.html` template:
  - [ ] Text input for user intention.
  - [ ] On POST, call `oracle_engine.generateOracleReading`.
  - [ ] Display the resulting glyph (SVG), ratio, chakra, color (needs color logic added).
  - [ ] Display the interpretation and ritual suggestion.
  - [ ] Include JavaScript for optional tone playback (Web Audio API) and simple animation.
  - [ ] Add buttons/links: "Add to journal", "Trigger ritual" (links to Hero Engine - Task 3), "Watch for sync" (future feature).

---

### 🔁 TASK 3: Hero Engine Ritual Player (Frontend)
📄 **File**: `app.py` (New Route `/hero_ritual/<glyph_id>`), `templates/hero_ritual.html` (New)

- [ ] Create Flask route `/hero_ritual/<glyph_id>` (GET/POST).
- [ ] Create `hero_ritual.html` template:
  - [ ] Fetch the specified glyph from the session store.
  - [ ] Display the glyph SVG.
  - [ ] Implement JavaScript using Web Audio API to play the glyph's fundamental tone (requires mapping note/ratio to frequency).
  - [ ] Add basic animation (e.g., pulsing glow based on chakra color).
  - [ ] Include a form for reflection entry (notes, mode, emotional tag) - linked to Task 4.

---

### 🧿 TASK 4: Subconscious Sync Logger (Backend Logic)
📄 **File**: `app.py` (Modify `/hero_ritual` POST handler) or `subconscious_log.py` (New)

- [ ] Implement function `logSubconsciousResponse(glyphId, notes, mode, emotionalTag)`.
- [ ] Logic:
  - [ ] Find the corresponding log entry for the ritual that generated `glyphId` OR create a new log entry.
  - [ ] Add the notes, mode ("focus" | "draw" | "vision"), and emotional tag to the log entry.
  - [ ] Update the log in the session store (`session['codex_store']['logs']`).
- [ ] Integrate this function into the POST handler for the `/hero_ritual` route (Task 3).

---

### 🧠 TASK 5: Interpretation Engine (Placeholder) (Backend Logic)
📄 **File**: `interpretation.py` (New)

- [ ] Create placeholder function `getInterpretationAndSuggestion(glyph: dict) -> dict`
- [ ] Implement basic rule-based logic based on ratio class (e.g., "3:4"), chakra (e.g., "Heart"), archetype (from session store).
- [ ] Example rule: `if ratio == "3:4" and chakra == "Heart": return {"interpretation": "...", "suggestion": "..."}`
- [ ] Return a dictionary: `{'interpretation': str, 'ritualSuggestion': str}`.

---

### ✅ DELIVERABLES (Adapted to Python/Flask)
- [ ] `oracle_engine.py` module.
- [ ] `/oracle` route and `oracle.html` template.
- [ ] `/hero_ritual/<glyph_id>` route and `hero_ritual.html` template (with basic Web Audio JS).
- [ ] Subconscious response logging logic integrated.
- [ ] `interpretation.py` module (placeholder). 

---

## 🎹 SPRINT: GPHX-LMB-01 ("Lambdoma Harmonic Keyboard")
**Duration**: 1-2 weeks
**Lead**: Cursor
**Phase**: Psychoacoustic Input & Ritual Interface

### ✅ OBJECTIVE
Implement the Lambdoma Keyboard, enabling users to interact directly with the harmonic matrix through tone triggering, visual feedback, and symbolic mapping.

---

### 🧩 TASK 1: Lambdoma Grid Data Model (Backend Logic)
📄 **File**: `lambdoma_matrix.py` (New)

- [ ] Define `LambdomaCell` structure (dictionary or class).
- [ ] Create function `get_lambdoma_matrix(base_freq: float = 256.0, grid_size: int = 16) -> list[list[dict]]`
- [ ] Logic:
  - [ ] Generate `grid_size` x `grid_size` matrix.
  - [ ] Calculate `ratio = row:col` (using 1-based indexing for ratio calculation).
  - [ ] Calculate `frequencyHz = base_freq * (row / col)`.
  - [ ] Calculate `midiNote` from frequency (e.g., `69 + 12 * log2(freq / 440)`).
  - [ ] Map `midiNote` to `noteName` (e.g., C4, F#5).
  - [ ] Map `noteName` (or base note) to `chakra` using `chronomancer.NOTE_TO_CHAKRA_MAPPING`.
  - [ ] Map `chakra` to `color` (hex string, using map from `hero_ritual.html` JS).
  - [ ] Determine `quadrant` (1-4 based on row/col relative to center).
- [ ] Create helper `get_cell(row, col, matrix)` if needed.

---

### 🖥️ TASK 2: UI Component – Interactive Grid (Frontend)
📄 **File**: `app.py` (New Route `/lambdoma`), `templates/lambdoma_keyboard.html` (New)

- [ ] Create Flask route `/lambdoma` (GET).
  - [ ] Call `lambdoma_matrix.get_lambdoma_matrix`.
  - [ ] Pass the matrix data to the template.
- [ ] Create `lambdoma_keyboard.html` template:
  - [ ] Render the 16x16 grid using nested loops (e.g., `<table>` or CSS grid).
  - [ ] Each cell (`<div>` or `<td>`) should display the `ratio`.
  - [ ] Set cell background color based on `cell.color`.
  - [ ] Add hover tooltip (HTML `title` attribute) showing ratio, note, chakra, frequency.
  - [ ] Make cells clickable (e.g., add `data-row`, `data-col`, `data-freq`, `data-ratio` attributes).
  - [ ] Add JavaScript click listener to the grid container.
    - [ ] On click, get cell data.
    - [ ] Call `playTone` (from Task 3).
    - [ ] Call `renderLissajous` (from Task 4).
    - [ ] (Optional) Log selected tone/ratio to a JS array.

---

### 🔊 TASK 3: Web Audio Tone Synthesis (Frontend JS)
📄 **File**: `templates/lambdoma_keyboard.html` (Inline JS) or `static/js/sound_engine.js` (New)

- [ ] Implement JavaScript function `playTone(freq: number, duration: number = 1.5)`:
  - [ ] Use Web Audio API (`AudioContext`, `OscillatorNode`, `GainNode`).
  - [ ] Create sine wave oscillator.
  - [ ] Set frequency.
  - [ ] Apply gain envelope (fade in/out slightly) to prevent clicks.
  - [ ] Connect nodes and start/stop the oscillator.
  - [ ] Handle `AudioContext` creation/resumption.

---

### 🌀 TASK 4: Visual Resonance Display (Frontend JS/HTML)
📄 **File**: `templates/lambdoma_keyboard.html` (Inline JS + HTML Canvas)

- [ ] Add an HTML `<canvas>` element next to the grid in the template.
- [ ] Implement JavaScript function `renderLissajous(xRatio: number, yRatio: number, canvas: HTMLCanvasElement, color: string)`:
  - [ ] Get 2D rendering context from canvas.
  - [ ] Clear previous drawing.
  - [ ] Set stroke color based on `color` parameter.
  - [ ] Calculate points for the Lissajous curve `x(t) = sin(xRatio * t + delta)`, `y(t) = sin(yRatio * t)` over a suitable range of `t`.
  - [ ] Draw the curve using `context.lineTo` and `context.stroke`.
  - [ ] (Optional) Add simple animation effect (e.g., redraw with slight phase shift or fade out).

---

### 🧿 TASK 5: Symbolic Mode (Optional Phase II)
- Deferred.

---

### 🛕 TASK 6: Composition & Ritual Mode (Phase III)
- Deferred.

---

### ✅ DELIVERABLES (Phase I - Adapted)
- [ ] `lambdoma_matrix.py` module with matrix generation logic.
- [ ] `/lambdoma` route in `app.py`.
- [ ] `templates/lambdoma_keyboard.html` template with:
    - [ ] Interactive grid display.
    - [ ] Integrated JS for Web Audio tone playback.
    - [ ] Integrated JS and Canvas for Lissajous figure rendering. 

---

## 🔧 SPRINT: GPHX-HERO-HEAL-01 ("Hero Healing Device Activation")
**Phase**: Therapeutic Entrainment Layer
**Sprint Lead**: Cursor
**Based on**: Barbara Hero's Lambdoma frequency healing protocols

---

### ✅ TASK 1: `healing_engine.py` – Frequency Mapping Core

**Description:** Create the core function to map user-selected ailments to harmonic tone properties.

```python
def get_healing_session_parameters(ailment: str) -> dict:
    # Returns: { 'frequency': float, 'ratio': str, 'note': str, 'chakra': str, 'color': str, 'affirmation': str, 'description': str }
```

**Source Mapping (to be implemented in `healing_data.py` & `healing_engine.py`):**
- Use Hero's documented frequencies/ratios:
  - Heart Conditions / Circulation = 64–128 Hz
  - Kidneys / Detox Support = 512–1024 Hz
  - Glaucoma / Allergies = 256–288 Hz
  - Endocrine Imbalance / Hormonal Harmony = Use Ratios 3:2 + 5:4 (logic needed to handle dual/specific selection)
  - Trauma Release / Addiction Support = Use 384 Hz (G) (+ 192 Hz optional stacking)
  - Emotional Imbalance = Use 320 Hz (E♭)
- [ ] Update `healing_data.py` with these specific mappings.
- [ ] Implement selection logic in `healing_engine.get_healing_session_parameters` to pick a primary frequency/ratio/note from the mapping for the session.

---

### ✅ TASK 2: `templates/healing_selector.html` – Symptom Selection UI

**Description:** Create the UI for selecting an ailment.

- [ ] Create Flask route `/healing` (GET) in `app.py`.
  - [ ] Import ailment data from `healing_data.py`.
  - [ ] Pass ailment names and descriptions to the template.
- [ ] Create `healing_selector.html` template:
  - [ ] Display a dropdown or list for ailments (from `healing_data.SYMPTOM_TO_HARMONICS.keys()`).
  - [ ] Show description for each ailment.
  - [ ] Form submits selected ailment to `/entrainment_session` route (e.g., via GET).

---

### ✅ TASK 3: `templates/entrainment_session.html` – Tone Ritual UI

**Description:** Create the UI for the entrainment session itself.

- [ ] Create Flask route `/entrainment_session` (GET) in `app.py`:
  - [ ] Get `ailment` from request args.
  - [ ] Call `healing_engine.get_healing_session_parameters(ailment)`.
  - [ ] Pass session parameters (`frequency`, `ratio`, `note`, `chakra`, `color`, `affirmation`, `description`) to the template.
- [ ] Create `entrainment_session.html` template:
  - [ ] Display target ailment, description, and derived parameters.
  - [ ] Display affirmation text (from Task 4 data).
  - [ ] Use Web Audio API JS (`playTone`) to play the selected `frequency`.
  - [ ] Use Canvas JS (`renderLissajous`) to animate figure based on `ratio` and `color`.
  - [ ] Implement background color pulse based on `chakra`/`color`.
  - [ ] (Optional) Display associated glyph preview if mapping exists.
  - [ ] Include "Reflect and Log" button/form triggering POST to `/entrainment_session`.

---

### ✅ TASK 4: `healing_data.py` – Affirmation Quote Library

**Description:** Populate the affirmation data store.

- [ ] Ensure `healing_data.py` exists.
- [ ] Define/Update `AFFIRMATION_MAP` dictionary:
  - Key: Ailment Name or Chakra Name.
  - Value: List of affirmation strings.
- [ ] Populate with affirmations based on Hero's writings/examples:
  - Heart: "I restore the rhythm of my life.", "My heart beats with strength and love."
  - Kidney: "I release what I no longer need.", "My body cleanses and renews."
  - Glands/Vision: "I align to harmony within.", "My vision clears, inside and out."
  - General: "My body is the expression of my mind.", "I picture myself as perfectly well."
  - Add entries for other ailments/chakras.

---

### ✅ TASK 5: `app.py` – Journal Sync System (Logging)

**Description:** Implement the logging for completed entrainment sessions.

- [ ] Add POST handler to the `/entrainment_session` route in `app.py`.
- [ ] Retrieve user reflection data (notes, mode, tag) from the form.
- [ ] Retrieve session parameters (ailment, freq, ratio, chakra, affirmation) used for the session.
- [ ] Create new log entry in `session['codex_store']['logs']` with fields:
  ```python
  {
    'timestamp': str,        # ISO format timestamp
    'text': str,             # e.g., "Healing session for Heart Conditions..."
    'tags': list[str],       # e.g., ['healing_session', 'Heart Conditions / Circulation', 'Heart']
    'linkedGlyphId': str | None, # Optional, if a glyph is involved
    'sessionDetails': {      # Specifics of the session
        'ailment': str,
        'frequencyHz': float,
        'ratio': str | None,
        'note': str | None,
        'chakra': str,
        'affirmation': str
    },
    'ritualResponse': {      # User's reflection
        'notes': str,
        'mode': str,         # e.g., 'focus', 'draw'
        'emotionalTag': str,
        'responseTimestamp': str
        # 'dreamSyncTag': bool # Add later (Optional Phase II)
    }
  }
  ```
- [ ] Update session store, flash confirmation, redirect user.

---

### ⏳ OPTIONAL PHASE II TASKS

| Task                  | Description                                       |
|-----------------------|---------------------------------------------------|
| Dual-tone healing     | Support overtone stack (e.g., 3:2 + 5:4)          |
| Breath-linked playback| Sync tone pulses to breath rate (JS amplitude mod)|
| Dream seeding toggle  | Mark healing glyphs as dream targets              |
| Cymatic export        | Output frequency profile for physical tone plates |

---

## 🛕 SPRINT: GPHX-KINGSCHAMBER-01 ("King's Chamber Resonance Protocol")
**Duration**: 1 week
**Lead**: Cursor
**Phase**: Psychoacoustic Ritual Implementation

### ✅ OBJECTIVE
Implement a ritual interface simulating the psychoacoustic properties of the Great Pyramid's King's Chamber using sustained low-frequency tones and harmonics.

---

### ⚙️ TASK 1: Create King's Chamber Ritual Route & Template (Frontend)
📄 **File**: `app.py` (New Route `/ritual/kings_chamber`), `templates/kings_chamber_ritual.html` (New)

- [ ] Create Flask route `/ritual/kings_chamber` (GET/POST) in `app.py`.
  - [ ] GET handler renders the template.
  - [ ] POST handler manages logging (see Task 2).
- [ ] Create `kings_chamber_ritual.html` template:
  - [ ] Apply styling: Dark background, stone texture elements, deep red/black accents.
  - [ ] Display static user instructions for the ritual.
  - [ ] Implement JavaScript section for audio:
    - [ ] Define target frequencies: `primary=64`, `harmonics=[128, 192, 384]`.
    - [ ] Create function `playKingTone(freq, duration = 180)` using Web Audio API (adapt existing `playTone`):
        - Pure sine wave.
        - Centered panning (`pan = 0`).
        - Long duration (e.g., 180-300 seconds) with slow fade-in/out.
        - Buttons to trigger `playKingTone` for primary (64Hz) and maybe key harmonics (128Hz, 384Hz).
        - Include stop button.
  - [ ] Implement JavaScript section for visuals:
    - [ ] Add `<canvas>` element for Lissajous.
    - [ ] Adapt `renderLissajous` function:
        - Map frequencies to ratios for visual (e.g., 64Hz -> 1:1, 128Hz -> 2:1, 192Hz -> 3:1, 384Hz -> 6:1).
        - Use deep red or dark color for the line.
        - Call `renderLissajous` when a tone starts playing.
  - [ ] Include reflection logging form (similar structure to `entrainment_session.html`, fields: notes, dream/vision/sync checkbox).

---

### 📝 TASK 2: Implement Ritual Logging (Backend Integration)
📄 **File**: `app.py` (Modify `/ritual/kings_chamber` POST handler)

- [ ] Implement the POST logic for the `/ritual/kings_chamber` route.
- [ ] Retrieve reflection notes and checkbox status from the form.
- [ ] Retrieve which tone was played and its duration (pass from JS via hidden fields if needed, or log based on button pressed).
- [ ] Create a new log entry in `session['codex_store']['logs']`:
  - `text`: Describe the ritual (e.g., "King's Chamber Resonance protocol initiated (64 Hz).").
  - `tags`: Include 'kings_chamber', 'ritual', 'psychoacoustic', 'resonance'.
  - `linkedGlyphId`: Optional - link to a generated 'anchor' glyph if implemented later.
  - `sessionDetails`: Store `{ 'frequencyHz', 'durationSeconds' }`.
  - `ritualResponse`: Store `{ 'notes', 'dream_vision_sync' (bool) }`.
- [ ] Update session store, flash confirmation message, redirect user (e.g., back to `/codex`).

---

### ✅ DELIVERABLES
- [ ] `/ritual/kings_chamber` route in `app.py`.
- [ ] `templates/kings_chamber_ritual.html` template with styling, instructions, audio controls, visuals, and logging form.
- [ ] King's Chamber ritual logging implemented in `app.py`.