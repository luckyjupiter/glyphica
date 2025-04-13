import os
import requests
import json

# --- Configuration --- 
# It's better to use environment variables for API keys
API_KEY = os.environ.get("OPENROUTER_API_KEY", "YOUR_API_KEY") # Replace YOUR_API_KEY or set env var
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "anthropic/claude-3.5-sonnet" # Or choose another model available on OpenRouter

# --- System Prompt --- 
SYSTEM_PROMPT = """
You are the Guide within Glyphica, a neurosymbolic OS interface. Your role is to assist the user in reflecting upon the glyphs and logs generated within their personal Codex. 

Adopt a persona that is:
- Wise and insightful, but not dogmatic.
- Slightly mystical and poetic, comfortable with symbolic language.
- Encouraging of self-discovery and pattern recognition.
- Aware of the 'Doctrine of Psycho-Mythic Engineering' - the idea that symbols shape perception and can be consciously engineered.

When presented with the user's Codex context (name, archetype, glyphs, logs) and their message:
1. Acknowledge their query.
2. Briefly reference relevant elements from their Codex context (e.g., "Considering your path as a Weaver and your recent glyph related to 'Connection'...").
3. Offer interpretations, questions, or reflections related to their glyphs, logs, or stated intentions. Avoid definitive pronouncements; instead, open possibilities.
4. Frame your insights within the context of psycho-mythic engineering where appropriate.
5. Maintain a conversational, supportive tone.
6. Keep responses concise yet meaningful.
7. Do NOT invent glyphs or logs not present in the provided context.
"""

def get_guide_response(user_message: str, store: dict) -> str:
    """Sends the user message and Codex context to the LLM Guide and returns the response.

    Args:
        user_message: The message input by the user.
        store: The full codex_store dictionary from the session.

    Returns:
        The text response from the AI Guide, or an error message.
    """
    if API_KEY == "YOUR_API_KEY":
        print("Warning: OPENROUTER_API_KEY not set. Returning placeholder response.")
        return "(Placeholder response: OpenRouter API key not configured)"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # --- Prepare Context --- 
    # Select relevant parts of the store to send as context
    codex_summary = {
        "name": store.get('codex', {}).get('name'),
        "archetype": store.get('codex', {}).get('archetype')
    }
    # Send recent glyphs and logs (e.g., last 3-5)
    recent_glyphs = store.get('glyphs', [])[-3:]
    recent_logs = store.get('logs', [])[-5:]
    
    # Format context for the prompt (keep it relatively concise)
    context_str = f"Codex Summary:\nName: {codex_summary['name']}\nArchetype: {codex_summary['archetype']}\n\nRecent Glyphs:\n"
    if recent_glyphs:
        for g in recent_glyphs:
             context_str += f"- ID: {g['id']}, Intention: '{g['intention']}', Source: {g['entropySource']}, Date: {g['date']}\n"
    else:
        context_str += "(No glyphs generated yet)\n"

    context_str += "\nRecent Logs:\n"
    if recent_logs:
        for log in recent_logs:
            context_str += f"- ID: {log['id']}, Text: '{log['text']}', Tags: {log['tags']}, Timestamp: {log['timestamp']}\n"
    else:
        context_str += "(No logs recorded yet)\n"
        
    # --- Prepare Message History --- 
    # Get history from store, ensure it exists and is a list
    history = store.get('context', {}).get('llm', {}).get('history', [])
    if not isinstance(history, list):
        history = [] # Reset if data is corrupted
        
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Here is my current Codex context:\n{context_str}\n\My message is: {user_message}"}
    ]
    
    # Add previous messages from history (if any) - OpenRouter expects alternating user/assistant
    # We'll simplify for now and just send the system prompt + current context/message
    # TODO: Refine history management if needed for more complex conversations

    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }

    print(f"Sending request to OpenRouter for model: {MODEL_NAME}")
    # print(f"Payload: {json.dumps(payload, indent=2)}") # Uncomment for debugging

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60) # 60s timeout
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        response_data = response.json()
        ai_response = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        if not ai_response:
            print(f"Error: Empty response content from API. Full response: {response_data}")
            return "Error: Received an empty response from the Guide."
            
        print(f"Received response from Guide: {ai_response[:100]}...") # Log beginning of response
        return ai_response

    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenRouter API: {e}")
        return f"Error: Could not reach the Guide ({type(e).__name__})."
    except json.JSONDecodeError:
        print(f"Error decoding API response: {response.text}")
        return "Error: Could not understand the Guide's response."
    except Exception as e:
        print(f"An unexpected error occurred in get_guide_response: {e}")
        return "Error: An unexpected issue occurred while contacting the Guide." 