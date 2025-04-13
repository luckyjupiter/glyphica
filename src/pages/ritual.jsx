import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { performRitual } from '../lib/ritualEngine';

export default function LogRitual() {
  const navigate = useNavigate();
  const [intention, setIntention] = useState('');
  const [entropySource, setEntropySource] = useState('simulated'); // Default, maybe dropdown later
  const [isLoading, setIsLoading] = useState(false);
  const [ritualResult, setRitualResult] = useState(null);
  const [error, setError] = useState(null);

  const handleRitualSubmit = async (e) => {
    e.preventDefault();
    if (!intention.trim()) return;

    setIsLoading(true);
    setError(null);
    setRitualResult(null);

    try {
      const result = await performRitual({ intention, entropySource });
      setRitualResult(result);
    } catch (err) {
      console.error("Ritual failed:", err);
      setError('Failed to perform ritual. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleConfirm = () => {
    navigate('/home'); // Navigate back to Sanctum Home
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-900 to-black text-zinc-100 p-4 md:p-8 flex items-center justify-center transition-colors duration-500">
      <div className="w-full max-w-lg bg-zinc-800/50 backdrop-blur-sm rounded-xl shadow-2xl p-6 md:p-10 border border-zinc-700">

        {!ritualResult && !isLoading && (
          <form onSubmit={handleRitualSubmit} className="space-y-6">
            <h1 className="text-3xl font-serif text-center text-indigo-300 mb-6">Begin Ritual</h1>

            <div>
              <label htmlFor="intention" className="block text-sm font-medium text-zinc-300 mb-2">Set Your Intention</label>
              <input
                id="intention"
                type="text"
                value={intention}
                onChange={(e) => setIntention(e.target.value)}
                className="w-full px-4 py-3 text-lg bg-zinc-900/70 border border-zinc-700 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-200 text-white placeholder-zinc-500"
                placeholder="e.g., Embrace the unknown..."
                required
                autoFocus
              />
            </div>

            {/* Entropy Source - Kept simple for now */}
            <div className="text-sm text-center text-zinc-400">
              Entropy Source: <span className="font-medium text-zinc-300">{entropySource}</span>
              {/* TODO: Add dropdown selector here later */}
            </div>

            <button
              type="submit"
              className="w-full px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-zinc-900 transition duration-300 disabled:opacity-50"
              disabled={isLoading || !intention.trim()}
            >
              Begin Ritual
            </button>
          </form>
        )}

        {isLoading && (
          <div className="text-center py-10">
            <p className="text-xl text-indigo-300 animate-pulse">Generating glyph...</p>
            {/* Optional: Add a more elaborate loading animation */}
          </div>
        )}

        {error && (
          <div className="text-center text-red-400 py-10">
            <p>{error}</p>
            <button onClick={() => { setError(null); setIsLoading(false); }} className="mt-4 px-4 py-2 text-sm border border-zinc-600 rounded hover:bg-zinc-700 transition">Try Again</button>
          </div>
        )}

        {ritualResult && !isLoading && (
          <div className="text-center space-y-6">
            <h2 className="text-2xl font-serif text-indigo-300">Ritual Complete</h2>
            <div className="w-40 h-40 mx-auto border-2 border-indigo-500/50 flex items-center justify-center bg-zinc-900 rounded-lg shadow-lg shadow-indigo-500/20">
              {/* Render the resulting glyph */}
              {ritualResult.imageUrl.startsWith('<svg') ? (
                 <div dangerouslySetInnerHTML={{ __html: ritualResult.imageUrl }} />
               ) : (
                 <img src={ritualResult.imageUrl} alt={`Glyph ${ritualResult.glyphId}`} className="object-contain w-full h-full" />
               )}
            </div>
            <div className="text-zinc-300 space-y-1 text-sm">
                <p><span className="text-zinc-500">Intention:</span> {ritualResult.intention}</p>
                <p><span className="text-zinc-500">Glyph ID:</span> {ritualResult.glyphId.split('_')[1].substring(0, 6)}</p>
                 <p><span className="text-zinc-500">Timestamp:</span> {new Date(ritualResult.timestamp).toLocaleString()}</p>
                <p className="italic text-indigo-200 pt-2">{ritualResult.message}</p>
            </div>
            {/* Optional: Add AI prompt button here */}
            <button
              onClick={handleConfirm}
              className="w-full mt-4 px-6 py-3 bg-zinc-600 text-white font-semibold rounded-lg hover:bg-zinc-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zinc-500 focus:ring-offset-zinc-900 transition duration-300"
            >
              Return to Sanctum
            </button>
          </div>
        )}
      </div>
    </div>
  );
} 