import React from 'react';
import { useCodexStore } from '../context/codexStore';
import { SparklesIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom'; // Optional: if clicking glyphs navigates

// Helper function to format date (optional)
const formatDate = (isoString) => {
  if (!isoString) return '';
  return new Date(isoString).toLocaleDateString(undefined, { 
    year: 'numeric', month: 'short', day: 'numeric' 
  });
};

// Individual Glyph Card Component
const GlyphCard = ({ glyph }) => {
  const navigate = useNavigate(); // Optional

  const handleGlyphClick = () => {
    // Optional: Navigate to a detailed glyph view page later
    // navigate(`/glyph/${glyph.id}`); 
    console.log("Clicked glyph:", glyph.id);
  };

  return (
    <div 
      className={`relative border rounded-lg overflow-hidden shadow-md group cursor-pointer transition-all duration-300 flex flex-col 
        ${glyph.dream 
          ? 'border-purple-400/60 hover:border-purple-400 dream-glyph-card' 
          : 'border-zinc-300 dark:border-zinc-700 hover:border-zinc-500 dark:hover:border-zinc-500 bg-white dark:bg-zinc-800/50'}
      `}
      title={glyph.dream ? "Dream Glyph: Emerged autonomously during symbolic drift or silence." : `Glyph: ${glyph.intention}`}
      onClick={handleGlyphClick} // Optional navigation/interaction
    >
      {/* Dream Indicator Icon */}
      {glyph.dream && (
        <div className="absolute top-1.5 right-1.5 z-10 bg-black/30 backdrop-blur-sm rounded-full p-0.5">
          <SparklesIcon className="h-4 w-4 text-purple-300" title="Dream Glyph"/>
        </div>
      )}

      {/* Glyph Image Area */}
      <div className={`aspect-square w-full flex items-center justify-center p-2 
        ${glyph.dream ? 'bg-gradient-to-br from-zinc-900 via-purple-900/30 to-zinc-900' : 'bg-zinc-100 dark:bg-zinc-700/50'}
      `}>
         {glyph.imageUrl.startsWith('<svg') ? (
            <div dangerouslySetInnerHTML={{ __html: glyph.imageUrl }} className="w-full h-full object-contain p-2"/>
          ) : (
            <img src={glyph.imageUrl} alt={`Glyph ${glyph.id}`} className="object-contain w-full h-full max-h-40" />
         )}
      </div>

      {/* Metadata Area */}
      <div className="p-3 text-xs flex-grow flex flex-col justify-between bg-white dark:bg-zinc-800">
        <p className="font-medium text-zinc-800 dark:text-zinc-200 mb-1 truncate" title={glyph.intention}>" {glyph.intention} "</p>
        <div className="text-zinc-500 dark:text-zinc-400 space-y-0.5">
            <p>Source: <span className="font-mono text-xs px-1 py-0.5 rounded bg-zinc-100 dark:bg-zinc-700">{glyph.entropySource}</span></p>
            <p>Date: {formatDate(glyph.date)}</p>
        </div>
      </div>
       {/* Optional: Add hover effect to show linked logs here */}
    </div>
  );
};

export default function CodexArchive() {
  // Fetch all glyphs, sort newest first
  const glyphs = useCodexStore((state) => 
    [...state.glyphs].sort((a, b) => new Date(b.date) - new Date(a.date))
  );

  return (
    <div className="min-h-screen bg-white dark:bg-black text-zinc-900 dark:text-zinc-100 p-4 md:p-8 flex flex-col transition-colors duration-500">
       <header className="mb-8 text-center">
         {/* Consistent header styling - maybe add Codex name here too? */}
         <h1 className="text-3xl font-serif text-zinc-800 dark:text-zinc-200">Codex Archive</h1>
         <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">Your complete symbolic history.</p>
         {/* Optional: Add Filter Buttons Here */}
       </header>

       <main className="flex-grow">
         {glyphs.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
                {glyphs.map(glyph => (
                    <GlyphCard key={glyph.id} glyph={glyph} />
                ))}
            </div>
         ) : (
            <div className="text-center py-10">
                <p className="text-zinc-500">Your Codex is empty. Begin a <a href="/ritual" className="text-indigo-500 hover:underline">ritual</a> to generate your first glyph.</p>
            </div>
         )}
       </main>

       {/* Footer or other elements can go here */}
    </div>
  );
} 