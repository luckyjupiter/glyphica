# app.py
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import datetime
import json
# --- Import Glyphica Logic Modules ---
from symbol_engine import generate_glyph
from ritual_engine import perform_ritual
from dream_engine import should_dream, generate_dream
from ai_guide import get_guide_response
# --- Import Resonance Logic ---
from resonance_logic import combine_ratios, get_derived_chakra, get_glyph_chakra, get_glyph_ratio
# --- Import Oracle Engine ---
from oracle_engine import generate_oracle_reading
# --- Import Lambdoma Matrix Logic ---
from lambdoma_matrix import get_lambdoma_matrix
# --- Import Healing Data & Engine ---
from healing_data import SYMPTOM_TO_HARMONICS
from healing_engine import get_healing_session_parameters

# --- Placeholder for glyph generation --- 
def generate_placeholder_glyph(intention):
    print(f"Simulating glyph for: {intention}")
    svg_id = f"glyph_{abs(hash(intention)) % 10000}"
    svg = f'<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg" style="background-color: #f0f0f0;"><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="10">{svg_id}</text></svg>'
    return {"id": svg_id, "imageUrl": svg}
# --- End Placeholder ---

app = Flask(__name__)
# Set a secret key for session management (needed for flash messages or user sessions later)
app.secret_key = os.urandom(24)

# Archetype data (move to a data file later)
ARCHETYPES = [
  { "name": 'Seeker', "description": 'Drawn to meaning through movement and mystery.', "icon": "🧭" },
  { "name": 'Witness', "description": 'Observes the symbolic layers beneath all form.', "icon": "👁️" },
  { "name": 'Weaver', "description": 'Links dreams, signs, and synchronicities into pattern.', "icon": "🕸️" },
  { "name": 'Trickster', "description": 'Bends symbols with playful subversion.', "icon": "🎭" },
]

# --- Codex Store Initialization (Runs before each request) ---
@app.before_request
def initialize_codex_store():
    # Check if the store exists in the session for this request
    if 'codex_store' not in session:
        print("Initializing codex_store in session...") # Log for debugging
        session['codex_store'] = {
            'codex': {
                'name': None,
                'archetype': None,
                'foundingGlyphId': None,
                'createdAt': None,
            },
            'glyphs': [],
            'logs': [],
            'context': { # Add context sub-dictionary
                'llm': {} # Placeholder for LLM context/history
            }
        }
        session.modified = True # Ensure session is saved
    # Initialize onboarding state if not present
    if 'onboarding_step' not in session:
        session['onboarding_step'] = 0
        session['onboarding_data'] = {}
    # Ensure context.llm exists if store was already initialized pre-pivot
    if 'context' not in session['codex_store']:
         session['codex_store']['context'] = {'llm': {}}
         session.modified = True
    elif 'llm' not in session['codex_store']['context']:
         session['codex_store']['context']['llm'] = {}
         session.modified = True

# --- Routes --- 
@app.route('/', methods=['GET', 'POST'])
def index():
    # store = session['codex_store'] # Store not needed if we always redirect
    # Always redirect to home, bypassing onboarding entirely
    return redirect(url_for('home'))
    
    # --- All the original onboarding logic below is now bypassed --- 
    # # If already onboarded, redirect to home
    # if store['codex']['createdAt']:
    #     session['onboarding_step'] = 0 # Reset onboarding if they revisit
    #     session['onboarding_data'] = {}
    #     return redirect(url_for('home'))

    # if request.method == 'POST':
    #     current_step = session.get('onboarding_step', 0)
    #     onboarding_data = session.get('onboarding_data', {})

    #     if current_step == 0: # Submitted from Welcome screen
    #         session['onboarding_step'] = 1
    #     elif current_step == 1: # Submitted Codex Name
    #         if request.form.get('action') == 'back':
    #             session['onboarding_step'] = 0
    #         else:
    #             codex_name = request.form.get('codex_name')
    #             if codex_name and codex_name.strip():
    #                 onboarding_data['name'] = codex_name.strip()
    #                 session['onboarding_step'] = 2
    #             else:
    #                 flash("Please provide a name for your Codex.", "error")
    #     elif current_step == 2: # Submitted Archetype
    #         if request.form.get('action') == 'back':
    #             # Clear the potentially saved name if going back from archetype selection
    #             onboarding_data.pop('name', None)
    #             session['onboarding_step'] = 1
    #         else:
    #             archetype_name = request.form.get('archetype')
    #             if archetype_name in [a['name'] for a in ARCHETYPES]:
    #                 onboarding_data['archetype'] = archetype_name
    #                 session['onboarding_step'] = 3
    #             else:
    #                 flash("Please select a valid archetype.", "error")
    #     elif current_step == 3: # Submitted Intention for Founding Glyph
    #         if request.form.get('action') == 'back':
    #             # Clear the potentially saved archetype if going back from intention
    #             onboarding_data.pop('archetype', None)
    #             session['onboarding_step'] = 2
    #         else:
    #             intention = request.form.get('intention')
    #             if intention and intention.strip():
    #                 # --- Finalize Onboarding --- 
    #                 timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    #                 # Generate founding glyph using symbol_engine
    #                 glyph_data = generate_glyph(intention, source="Founding Ritual")
    #                 # glyph_data now contains id, imageUrl, date, intention, entropySource, dream

    #                 # Prepare glyph and log for storage
    #                 new_glyph = glyph_data # Use the whole dict from generate_glyph
    #                 glyph_id = new_glyph['id'] # Get id for log linking
    #                 timestamp = new_glyph['date'] # Use consistent timestamp

    #                 new_log = {
    #                      'id': f'log_{timestamp}',
    #                      'text': f'Codex "{onboarding_data["name"]}" initialized with archetype {onboarding_data["archetype"]} and intention: "{intention}"',
    #                      'tags': ['onboarding', 'codex_init', 'glyph_generation'],
    #                      'linkedGlyphId': glyph_id,
    #                      'timestamp': timestamp
    #                  }

    #                 # Update the main store
    #                 store['codex']['name'] = onboarding_data['name']
    #                 store['codex']['archetype'] = onboarding_data['archetype']
    #                 store['codex']['foundingGlyphId'] = glyph_id
    #                 store['codex']['createdAt'] = timestamp
    #                 store['glyphs'].append(new_glyph)
    #                 store['logs'].append(new_log)
                    
    #                 # Clear onboarding state and save session
    #                 session['onboarding_step'] = 0 
    #                 session['onboarding_data'] = {}
    #                 session.modified = True 
    #                 flash("Your Codex is initialized.", "success")
    #                 return redirect(url_for('home'))
    #             else:
    #                 flash("Please set your first intention.", "error")
        
    #     # Save intermediate onboarding data and step
    #     session['onboarding_data'] = onboarding_data
    #     session['onboarding_step'] = current_step 
    #     session.modified = True 

    # # For GET requests or after POST updates step
    # current_step = session.get('onboarding_step', 0)
    # return render_template('onboarding.html', step=current_step, archetypes=ARCHETYPES)

@app.route('/home')
def home():
    """Render the Sanctum Home page."""
    store = session['codex_store'] # Guaranteed to exist by before_request
    session_updated = False
    # if not store['codex']['createdAt']:
    #     return redirect(url_for('index')) 
    
    # --- Check for Dreaming Codex --- 
    if should_dream(store):
        dream_glyph, dream_log = generate_dream(store)
        store['glyphs'].append(dream_glyph)
        store['logs'].append(dream_log)
        # Maybe add a flash message?
        flash("The Codex stirred in its sleep, generating a new dream glyph.", "info")
        session_updated = True

    # Later: Fetch latest glyph, logs, etc. from store and pass to template
    latest_glyph = store['glyphs'][-1] if store['glyphs'] else None
    recent_logs = store['logs'][-5:] # Example: last 5 logs

    if session_updated:
        session.modified = True # Save changes if dream occurred

    # Pass show_nav=True to the base template
    return render_template('home.html', 
                           codex_name=store['codex']['name'],
                           display_glyph=latest_glyph,
                           recent_logs=recent_logs,
                           show_nav=True)

# --- Add routes later --- 
# Placeholder for /about route
@app.route('/about')
def about():
     # Need to check if initialized to show nav correctly
     store = session['codex_store']
     show_nav = store['codex']['createdAt'] is not None
     return render_template('about.html', show_nav=show_nav) 

# Placeholder for /codex route
@app.route('/codex')
def codex():
     store = session['codex_store']
     # if not store['codex']['createdAt']:
     #     return redirect(url_for('index'))
     # Sort glyphs newest first for display
     display_glyphs = sorted(store['glyphs'], key=lambda g: g['date'], reverse=True)
     return render_template('codex.html', glyphs=display_glyphs, show_nav=True) 

# Placeholder for /ritual route
@app.route('/ritual', methods=['GET', 'POST'])
def ritual():
     store = session['codex_store']
     # if not store['codex']['createdAt']:
     #     return redirect(url_for('index'))

     if request.method == 'POST':
         intention = request.form.get('intention')
         if intention and intention.strip():
             timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
             # Perform ritual using ritual_engine
             new_glyph, new_log = perform_ritual(intention, store)

             # Update the store in the session
             store['glyphs'].append(new_glyph)
             store['logs'].append(new_log)
             # Optionally clear LLM context after ritual, or keep it?
             # store['context']['llm']['history'] = [] # Example: clear history
             session.modified = True

             flash(f'Ritual complete. New glyph generated for "{intention}".', 'success')
             return redirect(url_for('home')) # Redirect to home to see the result
         else:
             flash("Please provide an intention for the ritual.", "error")
             # Fall through to render the template again on GET or invalid POST

     return render_template('ritual.html', show_nav=True)

# --- AI Guide Route --- 
@app.route('/guide', methods=['GET', 'POST'])
def guide():
     """Handles interaction with the AI Guide."""
     store = session['codex_store']
     # if not store['codex']['createdAt']:
     #     return redirect(url_for('index'))

     # Ensure history list exists
     if 'history' not in store['context']['llm'] or not isinstance(store['context']['llm']['history'], list):
         store['context']['llm']['history'] = []
         session.modified = True

     if request.method == 'POST':
         user_message = request.form.get('message')
         if user_message and user_message.strip():
             # Add user message to history
             store['context']['llm']['history'].append({"role": "user", "content": user_message})
             
             # Get response from AI Guide
             # Pass the *entire store* as ai_guide needs context beyond just history
             ai_response = get_guide_response(user_message, store)
             
             # Add AI response to history
             store['context']['llm']['history'].append({"role": "assistant", "content": ai_response})
             
             session.modified = True
             # Redirect back to GET to prevent form resubmission
             return redirect(url_for('guide'))
         else:
             flash("Please enter a message for the Guide.", "error")

     # For GET requests, just render the template with the history
     chat_history = store['context']['llm'].get('history', [])
     return render_template('guide.html', chat_history=chat_history, show_nav=True)

# --- Oracle Route --- 
@app.route('/oracle', methods=['GET', 'POST'])
def oracle():
    """Handles the Oracle intention input and displays the reading."""
    store = session.get('codex_store', {})
    # if not store.get('codex', {}).get('createdAt'):
    #     return redirect(url_for('index')) # Ensure user is onboarded

    oracle_reading = None

    if request.method == 'POST':
        intention = request.form.get('intention')
        if intention and intention.strip():
            reading_result = generate_oracle_reading(intention)
            
            if reading_result:
                oracle_reading = reading_result
                new_glyph = oracle_reading['glyph']
                timestamp = new_glyph['date'] # Use glyph's timestamp
                glyph_id = new_glyph['id']

                # Create a log entry for the oracle ritual
                new_log = {
                    'id': f'log_oracle_{timestamp}',
                    'text': f'Oracle invoked with intention: "{intention}". Glyph {glyph_id} generated.',
                    'tags': ['oracle', 'glyph_generation', 'interpretation'],
                    'linkedGlyphId': glyph_id,
                    'timestamp': timestamp,
                    'interpretation': oracle_reading.get('interpretation'),
                    'suggestion': oracle_reading.get('ritualSuggestion')
                }

                # Update the store in the session
                store.setdefault('glyphs', []).append(new_glyph)
                store.setdefault('logs', []).append(new_log)
                session.modified = True
                flash(f'Oracle reading complete for "{intention}".', 'info')
                # We stay on the page to show the result, passing oracle_reading
            else:
                flash("The Oracle could not generate a reading at this time.", "error")
        else:
            flash("Please provide an intention for the Oracle.", "error")

    # Pass the reading (if generated) to the template
    return render_template('oracle.html', 
                           oracle_reading=oracle_reading,
                           show_nav=True)

# --- Hero Ritual Player Route --- 
@app.route('/hero_ritual/<glyph_id>', methods=['GET', 'POST'])
def hero_ritual(glyph_id):
    """Displays a specific glyph for psychoacoustic/visual entrainment and collects user feedback."""
    store = session.get('codex_store', {})
    # if not store.get('codex', {}).get('createdAt'):
    #     return redirect(url_for('index'))

    target_glyph = next((g for g in store.get('glyphs', []) if g['id'] == glyph_id), None)

    if not target_glyph:
        flash(f"Glyph with ID {glyph_id} not found.", "error")
        return redirect(url_for('codex')) # Redirect to codex view if glyph doesn't exist

    if request.method == 'POST':
        # --- Handle Subconscious Response Logging (Task 4) --- 
        notes = request.form.get('ritual_notes', '')
        mode = request.form.get('ritual_mode') # e.g., focus, draw, vision
        emotional_tag = request.form.get('emotional_tag')
        
        # TODO: Implement logSubconsciousResponse logic here or call it from another module
        log_id_to_update = None
        # Try find the log associated with this glyph's generation
        for log in reversed(store.get('logs', [])):
            if log.get('linkedGlyphId') == glyph_id and 'glyph_generation' in log.get('tags', []):
                 log_id_to_update = log['id']
                 # Add response details
                 log['ritualResponse'] = {
                      'notes': notes,
                      'mode': mode,
                      'emotionalTag': emotional_tag,
                      'responseTimestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
                 }
                 print(f"Updating log {log_id_to_update} with ritual response for glyph {glyph_id}")
                 break # Found the most recent generation log
        
        if not log_id_to_update:
             # If no generation log found (e.g., older glyph), create a new log?
             # Or maybe just flash a message?
             print(f"Warning: Could not find original generation log for glyph {glyph_id} to attach response.")
             # For now, don't create a new log, just skip updating
             flash("Could not link response to original log entry.", "warning")
        
        session.modified = True 
        flash("Ritual reflection logged.", "success")
        return redirect(url_for('codex')) # Redirect back to the codex after logging
        # --- End Task 4 Logic --- 

    # For GET requests, just render the template with the glyph
    return render_template('hero_ritual.html', 
                           glyph=target_glyph,
                           show_nav=True)

# --- Debug Resonance Route --- 
@app.route('/debug/resonance', methods=['GET'])
def debug_resonance():
    """Debug tool to test resonance between two glyphs."""
    store = session.get('codex_store', {})
    all_glyphs = store.get('glyphs', [])
    # Sort for consistent display in dropdown
    all_glyphs_sorted = sorted(all_glyphs, key=lambda g: g['date'], reverse=True)

    glyph_id_1 = request.args.get('glyph_id_1')
    glyph_id_2 = request.args.get('glyph_id_2')

    glyph1 = None
    glyph2 = None
    combined_ratio_result = None
    derived_chakra_result = None

    if glyph_id_1 and glyph_id_2:
        glyph1 = next((g for g in all_glyphs if g['id'] == glyph_id_1), None)
        glyph2 = next((g for g in all_glyphs if g['id'] == glyph_id_2), None)

        if glyph1 and glyph2:
            ratio1 = get_glyph_ratio(glyph1)
            ratio2 = get_glyph_ratio(glyph2)
            chakra1 = get_glyph_chakra(glyph1)
            chakra2 = get_glyph_chakra(glyph2)

            if ratio1 and ratio2:
                combined_ratio_result = combine_ratios(ratio1, ratio2)
            if chakra1 and chakra2:
                derived_chakra_result = get_derived_chakra(chakra1, chakra2)
        else:
            flash("One or both selected glyph IDs not found.", "error")
            # Reset glyphs if not found to avoid partial display
            glyph1 = None 
            glyph2 = None

    return render_template('debug_resonance.html', 
                           all_glyphs=all_glyphs_sorted, 
                           glyph1=glyph1, 
                           glyph2=glyph2,
                           combined_ratio=combined_ratio_result,
                           derived_chakra=derived_chakra_result,
                           show_nav=True) # Assuming debug tools need nav

# --- Lambdoma Keyboard Route --- 
@app.route('/lambdoma')
def lambdoma_keyboard():
    """Displays the interactive Lambdoma Keyboard."""
    store = session.get('codex_store', {})
    # if not store.get('codex', {}).get('createdAt'):
    #     return redirect(url_for('index'))
        
    # Allow grid size selection (default 16, allow 8)
    try:
        req_size = int(request.args.get('size', 16))
        grid_size = 8 if req_size == 8 else 16 # Only allow 8 or 16 for now
    except ValueError:
        grid_size = 16
        
    # TODO: Add base_freq selection later
    base_freq = 256.0

    # Generate the matrix data (can add config options later)
    matrix_data = get_lambdoma_matrix(grid_size=grid_size, base_freq=base_freq)
    
    return render_template('lambdoma_keyboard.html', 
                           matrix=matrix_data,
                           grid_size=grid_size, # Pass validated grid size
                           show_nav=True)

# --- Healing Selector Route --- 
@app.route('/healing')
def healing_selector():
    """Displays the list of ailments for the user to choose from."""
    store = session.get('codex_store', {})
    # --- TEMPORARY BYPASS ---
    # if not store.get('codex', {}).get('createdAt'):
    #     return redirect(url_for('index'))
    # --- END BYPASS ---

    # Get ailment names and descriptions for the selector
    ailment_options = []
    for name, data in SYMPTOM_TO_HARMONICS.items():
        ailment_options.append({
            "name": name,
            "description": data.get("description", "No description available.")
        })

    return render_template('healing_selector.html', 
                           ailments=ailment_options, 
                           show_nav=True)

# --- Entrainment Session Route --- 
@app.route('/entrainment_session', methods=['GET', 'POST'])
def entrainment_session():
    """Displays the healing entrainment session player and handles reflection logging."""
    store = session.get('codex_store', {})
    # --- TEMPORARY BYPASS ---
    # if not store.get('codex', {}).get('createdAt'):
    #     return redirect(url_for('index'))
    # --- END BYPASS ---

    if request.method == 'POST':
        # --- Task 5: Handle Reflection Logging --- 
        ailment = request.form.get('ailment_name') # Get from hidden form field
        session_params_json = request.form.get('session_params')
        session_params = json.loads(session_params_json) if session_params_json else {}
        
        notes = request.form.get('ritual_notes', '')
        mode = request.form.get('ritual_mode') 
        emotional_tag = request.form.get('emotional_tag')
        
        if not ailment or not session_params:
             flash("Error logging reflection: Session data missing.", "error")
             return redirect(url_for('healing_selector'))
             
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        new_log = {
            'id': f'log_heal_{timestamp}',
            'text': f'Healing session for \"{ailment}\" completed.',
            'tags': ['healing_session', ailment, session_params.get('chakra', 'Unknown')],
            'linkedGlyphId': None, # TODO: Optionally link a relevant glyph?
            'timestamp': timestamp,
            'sessionDetails': {
                'ailment': ailment,
                'frequencyHz': session_params.get('frequency'),
                'ratio': session_params.get('ratio'),
                'note': session_params.get('note'),
                'chakra': session_params.get('chakra'),
                'affirmation': session_params.get('affirmation')
            },
            'ritualResponse': {
                'notes': notes,
                'mode': mode,
                'emotionalTag': emotional_tag,
                'responseTimestamp': timestamp
            }
        }
        
        store.setdefault('logs', []).append(new_log)
        session.modified = True
        flash("Healing session reflection logged.", "success")
        return redirect(url_for('codex')) # Redirect to codex after logging
        # --- End Task 5 Logic --- 

    # --- GET Request: Display the session page --- 
    ailment_name = request.args.get('ailment')
    if not ailment_name:
        flash("No ailment selected.", "error")
        return redirect(url_for('healing_selector'))
        
    session_parameters = get_healing_session_parameters(ailment_name)
    
    if not session_parameters:
        flash(f"Could not find healing protocol for '{ailment_name}'.", "error")
        return redirect(url_for('healing_selector'))

    return render_template('entrainment_session.html', 
                           params=session_parameters,
                           show_nav=True)

# --- King's Chamber Ritual Route --- 
@app.route('/ritual/kings_chamber', methods=['GET', 'POST'])
def kings_chamber_ritual():
    """Displays the King's Chamber Resonance Ritual interface and handles logging."""
    store = session.get('codex_store', {})
    # --- TEMPORARY BYPASS --- 
    # if not store.get('codex', {}).get('createdAt'):
    #     return redirect(url_for('index'))
    # --- END BYPASS --- 

    if request.method == 'POST':
        # --- Task 2: Handle Logging --- 
        notes = request.form.get('ritual_notes', '')
        dream_sync = 'dream_vision_sync' in request.form # Checkbox value
        frequency_played = request.form.get('frequency_played') # Get from hidden field
        duration_played = request.form.get('duration_played') # Get from hidden field
        
        if not frequency_played or not duration_played:
             flash("Error logging reflection: Session data missing.", "error")
             # Redirect back to the ritual page itself on error?
             return redirect(url_for('kings_chamber_ritual'))
             
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        new_log = {
            'id': f'log_kcr_{timestamp}',
            'text': f'King\'s Chamber Resonance protocol completed ({frequency_played} Hz). ',
            'tags': ['kings_chamber', 'ritual', 'psychoacoustic', 'resonance', f'freq_{frequency_played}'],
            'linkedGlyphId': None, # TODO: Link generated glyph?
            'timestamp': timestamp,
            'sessionDetails': {
                'frequencyHz': float(frequency_played),
                'durationSeconds': int(duration_played)
            },
            'ritualResponse': {
                'notes': notes,
                'dream_vision_sync': dream_sync,
                'responseTimestamp': timestamp
            }
        }
        
        store.setdefault('logs', []).append(new_log)
        session.modified = True
        flash("King's Chamber Resonance reflection logged.", "success")
        return redirect(url_for('codex')) # Redirect to codex after logging
        # --- End Task 2 Logic --- 

    # --- GET Request: Display the ritual page --- 
    return render_template('kings_chamber_ritual.html', show_nav=True)

# --- Main Execution --- 
if __name__ == '__main__':
    # Correct way to call run on the Flask app instance
    app.run(debug=True, port=5001) 