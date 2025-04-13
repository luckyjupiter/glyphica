import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCodexStore } from '../context/codexStore';
import { PlusCircleIcon } from '@heroicons/react/24/solid'; // Example icon
import { SparklesIcon } from '@heroicons/react/24/outline'; // Icon for dream glyph

import { shouldDream } from '../lib/symbolEngine'; // Import dream trigger check
import { generateCodexDream } from '../lib/dreamEngine'; // Import dream generator

// Placeholder component for the feed item
const MirrorFeedItem = ({ log }) => (
  <div className="py-2 px-3 border-b border-zinc-200 dark:border-zinc-700 flex items-center space-x-3 text-sm">
    {/* Placeholder Icon - maybe differentiate dream logs later? */}
    <span className="text-zinc-400">{log.tags?.includes('dream') ? <SparklesIcon className="h-4 w-4 text-purple-400"/> : '🌀'}</span>
    <span className="flex-1 text-zinc-700 dark:text-zinc-300 truncate italic={log.tags?.includes('dream')}">{log.text}</span>
    <span className="text-zinc-500 dark:text-zinc-400">{new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
  </div>
);

// Placeholder for Resonance Meter
const ResonanceMeter = () => (
  <div className="h-10 w-full bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 rounded-full opacity-30 animate-pulse">
    {/* Basic animated gradient placeholder */}
  </div>
);

export default function SanctumHome() {
  const navigate = useNavigate();
  const { codex, glyphs, logs } = useCodexStore((state) => ({
    codex: state.codex,
    glyphs: state.glyphs,
    logs: state.logs,
  }));
  const [isDreaming, setIsDreaming] = useState(false); // State to prevent rapid re-triggering

  // Effect to check for dream conditions on mount and when glyphs/logs change
  useEffect(() => {
    const checkAndDream = async () => {
      // Prevent triggering if already processing or if last glyph was a dream
      if (isDreaming || (glyphs.length > 0 && glyphs[glyphs.length - 1].dream)) {
        return;
      }

      if (shouldDream()) {
        setIsDreaming(true);
        try {
          await generateCodexDream();
          // No need to manually update state, Zustand handles subscription
        } catch (error) {
          console.error("Failed to generate codex dream:", error);
        } finally {
          // Add a small delay before allowing another dream check if needed
          setTimeout(() => setIsDreaming(false), 5000); 
        }
      }
    };

    checkAndDream();
  // Rerun effect when glyphs or logs change - might be too frequent, consider debouncing later
  }, [glyphs, logs, isDreaming]); 

  // Get the most recent glyph, or the founding glyph if available
  const latestGlyph = glyphs.length > 0 ? glyphs[glyphs.length - 1] : null;
  const foundingGlyph = glyphs.find(g => g.id === codex.foundingGlyphId);
  const displayGlyph = latestGlyph || foundingGlyph;

  // Get recent logs for the feed (e.g., last 10)
  const recentLogs = logs.slice(-10).reverse();

  const handlePortalClick = () => {
    navigate('/ritual'); // Navigate to the Log Ritual page
  };

  return (
    <div className="min-h-screen bg-white dark:bg-black text-zinc-900 dark:text-zinc-100 p-4 md:p-8 flex flex-col transition-colors duration-500 relative pb-24"> {/* Added padding-bottom for portal button */}
      {/* Header - Optional, could show Codex Name */}
      <header className="mb-8 text-center">
        <h1 className="text-2xl font-serif text-zinc-600 dark:text-zinc-400">{codex.name || 'Your Codex'}</h1>
      </header>

      {/* Main Content Area */}
      <main className="flex-grow flex flex-col items-center space-y-8 md:space-y-12">

        {/* Today's Glyph Section */}
        <section className="text-center w-full max-w-md">
          <h2 className="text-sm uppercase tracking-widest text-zinc-500 mb-4">Glyph of the Moment</h2>
          {displayGlyph ? (
            <div 
              className={`w-48 h-48 md:w-64 md:h-64 mx-auto border flex items-center justify-center rounded-lg shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer relative 
                ${displayGlyph.dream 
                  ? 'border-purple-400/50 border-2 dream-glyph' 
                  : 'border-zinc-300 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800'}
              `}
              title={displayGlyph.dream ? "This glyph surfaced on its own. You did not call it. It arrived anyway." : "Latest glyph"}
            >
               {displayGlyph.dream && (
                 <SparklesIcon className="absolute top-2 right-2 h-5 w-5 text-purple-400 opacity-70" title="Dream Glyph"/>
               )}
               {displayGlyph.imageUrl.startsWith('<svg') ? (
                 <div dangerouslySetInnerHTML={{ __html: displayGlyph.imageUrl }} className="w-full h-full flex items-center justify-center"/>
               ) : (
                 <img src={displayGlyph.imageUrl} alt={`Glyph ${displayGlyph.id}`} className="object-contain w-full h-full" />
               )}
             </div>
           ) : (
             <div className="w-48 h-48 md:w-64 md:h-64 mx-auto border border-dashed border-zinc-300 dark:border-zinc-700 flex items-center justify-center bg-zinc-50 dark:bg-zinc-800 rounded-lg">
               <p className="text-zinc-500">No glyphs yet.</p>
             </div>
           )}
            {/* Placeholder for brief resonance analysis on tap */}
            {displayGlyph && <p className="text-xs text-zinc-400 mt-2 italic">Tap glyph for analysis (coming soon)</p>}
         </section>

         {/* Resonance Meter Section */}
         <section className="w-full max-w-lg">
           <h2 className="text-sm uppercase tracking-widest text-zinc-500 mb-3 text-center">Resonance</h2>
           <ResonanceMeter />
         </section>

         {/* Mirror Feed Section */}
         <section className="w-full max-w-lg">
           <h2 className="text-sm uppercase tracking-widest text-zinc-500 mb-3 text-center">Mirror Feed</h2>
           <div className="bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-lg shadow-inner max-h-60 overflow-y-auto">
             {recentLogs.length > 0 ? (
               recentLogs.map(log => <MirrorFeedItem key={log.id} log={log} />)
             ) : (
               <p className="p-4 text-center text-zinc-500">No entries yet.</p>
             )}
           </div>
         </section>

       </main>

       {/* Portal Button - Fixed Bottom Center */}
       <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 z-10">
         <button
           onClick={handlePortalClick}
           className="p-3 bg-indigo-600 rounded-full text-white shadow-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-black transition-all duration-300 transform hover:scale-110"
           aria-label="Start New Ritual"
         >
           <PlusCircleIcon className="h-8 w-8" /> {/* Example Icon */}
         </button>
       </div>
     </div>
   );
 } 