import React, { useState, useEffect, useMemo } from 'react';
import { queryAgent } from '../lib/openrouter';
import { useCodexStore } from '../context/codexStore';
import { getSymbolTimeline } from '../lib/symbolEngine';
import { getGlyphCoordinates } from '../lib/lambdoma';

export default function AgentChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Fetch relevant state from Zustand store
  const { codex, glyphs, logs } = useCodexStore();

  // Calculate derived context state using useMemo for efficiency
  const codexContext = useMemo(() => {
    // Check if glyphs is defined and is an array
    if (!Array.isArray(glyphs)) {
      console.warn("Glyphs data is not available or not an array.");
      return {
        codexName: codex?.name || 'Operator',
        lastGlyph: null,
        driftTag: 'N/A',
        resonanceLevel: 0,
        coordinates: { x: '-', y: '-' }
      };
    }
    const timeline = getSymbolTimeline(); // Assumes getSymbolTimeline handles potentially empty glyphs
    const lastGlyph = glyphs.length > 0 ? glyphs[glyphs.length - 1] : null;
    let context = {
        codexName: codex?.name || 'Operator',
        lastGlyph: null,
        driftTag: 'N/A',
        resonanceLevel: 0,
        coordinates: { x: '-', y: '-' }
    };

    if (lastGlyph) {
        const lastTimelineEntry = timeline.find(t => t.id === lastGlyph.id);
        if (lastTimelineEntry) {
            const coords = getGlyphCoordinates(lastGlyph, lastTimelineEntry.driftTag, lastTimelineEntry.resonanceLevel);
            context.lastGlyph = lastGlyph;
            context.driftTag = lastTimelineEntry.driftTag;
            context.resonanceLevel = lastTimelineEntry.resonanceLevel;
            context.coordinates = coords;
        } else {
            // Fallback if timeline entry not found (should ideally not happen if timeline is up-to-date)
            context.lastGlyph = lastGlyph;
             // Attempt basic coordinate calc if possible
            if (lastGlyph.intention) { // Check if intention exists
                context.coordinates = getGlyphCoordinates(lastGlyph, 'unknown', 0); // Use default values
            }
        }
    }
    return context;
  // Ensure codex object itself is a dependency if name can change
  }, [codex, glyphs, logs]); 

  // Initial greeting
  useEffect(() => {
      // Avoid adding duplicate initial message if messages already exist (e.g., from previous state)
      if (messages.length === 0) { 
        setMessages([{ role: 'assistant', content: 'Operator. The Mirror awaits your query.' }]);
      }
  // Run only once on mount
  }, []); // Empty dependency array

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = { role: 'user', content: input };
    // Use functional update to ensure we have the latest messages state
    setMessages(prev => [...prev, userMessage]);
    const currentMessages = messages.length > 0 ? [...messages, userMessage] : [userMessage]; // Use updated state

    setInput('');
    setLoading(true);

    // --- Construct Context Preamble --- 
    let contextString = `Operator: ${codexContext.codexName}\n`;
    if (codexContext.lastGlyph) {
        const lg = codexContext.lastGlyph;
        contextString += `Last glyph: "${lg.intention}" (ID: ${lg.id.substring(0,10)}..., ${lg.dream ? 'Dream' : 'Ritual'}, Entropy: ${lg.entropySource})\n`;
        contextString += `State: Resonance=${codexContext.resonanceLevel}, Drift=${codexContext.driftTag}, Lambdoma=[${codexContext.coordinates.x},${codexContext.coordinates.y}]\n`;
    } else {
        contextString += "State: Codex is nascent. No glyphs yet.\n";
    }
    // --- End Context Preamble --- 
    
    const messagesForApi = [
        { role: 'system', name: 'codex_context', content: contextString }, 
        // Pass the messages state as it was *before* adding the potential AI response
        ...currentMessages.slice(-10) 
    ];

    try {
        const reply = await queryAgent(messagesForApi);
        setMessages(prev => [...prev, { role: 'assistant', content: reply || "...silence..." }]);
    } catch (error) { 
        console.error("Error querying agent:", error);
        setMessages(prev => [...prev, { role: 'assistant', content: "My apologies, Operator. A disturbance in the signal." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    // Adjusted height and layout
    <div className="border border-border-subtle rounded-lg bg-background-dark/70 backdrop-blur-md shadow-xl max-w-2xl mx-auto flex flex-col h-[calc(100vh-10rem)] md:h-[calc(100vh-12rem)]"> 
      {/* Context Display Area */}
      <div className="flex-shrink-0 p-2 px-3 text-xs text-text-muted font-mono border-b border-border-subtle flex justify-between items-center flex-wrap gap-x-3 gap-y-1">
        <span>Op: {codexContext.codexName}</span>
        {codexContext.lastGlyph ? (
          <> 
            <span className="truncate" title={codexContext.lastGlyph.intention}>Last: "{codexContext.lastGlyph.intention.substring(0, 15)}..." {codexContext.lastGlyph.dream ? '(Dream)':''}</span>
            <span>Res: {codexContext.resonanceLevel}</span>
            <span>Drift: {codexContext.driftTag}</span>
          </>
        ) : (
            <span>Codex Nascent</span>
        )}
      </div>

      {/* Chat Message Area - Use flex-grow to take remaining space */} 
      <div className="flex-grow space-y-3 overflow-y-auto p-3 pr-2" style={{ scrollbarWidth: 'thin', scrollbarColor: `rgba(160, 160, 160, 0.3) transparent` }}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`px-3 py-1.5 rounded-lg max-w-[85%] text-sm leading-relaxed shadow-sm 
              ${msg.role === 'user' 
                ? 'bg-indigo-600 text-white' 
                : 'bg-gray-700/60 text-text-base'}
            `}>
              <span style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</span>
            </div>
          </div>
        ))}
        {loading && (
            <div className="flex justify-start">
                 <div className="px-3 py-1.5 rounded-lg bg-gray-700/60 text-text-muted animate-pulse text-sm">...</div>
             </div>
        )}
      </div>

      {/* Input Area - Use flex-shrink-0 */} 
      <div className="flex-shrink-0 flex p-2 border-t border-border-subtle">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !loading && sendMessage()} 
          className="flex-1 border border-border-subtle px-3 py-2 rounded-l-lg bg-gray-900/80 text-text-base focus:outline-none focus:ring-1 focus:ring-accent-dream focus:border-accent-dream placeholder-text-muted text-sm"
          placeholder="Speak to the Mirror..."
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          className="bg-indigo-600 text-white px-4 py-2 rounded-r-lg disabled:opacity-50 transition-colors duration-200 hover:bg-indigo-500 focus:outline-none focus:ring-1 focus:ring-accent-dream"
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
} 