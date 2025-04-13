import { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Assuming react-router-dom
import { useCodexStore } from '../context/codexStore';
// import { generateGlyph } from '../lib/glyphGen'; // Placeholder for actual glyph generation

const archetypes = [
  { name: 'Seeker', description: 'Drawn to meaning through movement and mystery.' },
  { name: 'Witness', description: 'Observes the symbolic layers beneath all form.' },
  { name: 'Weaver', description: 'Links dreams, signs, and synchronicities into pattern.' },
  { name: 'Trickster', description: 'Bends symbols with playful subversion.' },
];

// Placeholder for glyph generation
const generateFoundingGlyph = async (intention) => {
  console.log(`Simulating glyph generation for intention: ${intention}`);
  // const glyphData = await generateGlyph(intention, 'Simulated'); // Actual call later
  await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate async generation
  return {
    id: `glyph-${Date.now()}`,
    intention: intention,
    entropySource: 'Simulated',
    svgData: '<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="grey" /></svg>', // Placeholder SVG
    createdAt: new Date().toISOString(),
  };
};

export default function OnboardingRitual() {
  const [step, setStep] = useState(0);
  const [codexName, setCodexName] = useState('');
  const [selectedArchetype, setSelectedArchetype] = useState(null);
  const [intention, setIntention] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [foundingGlyph, setFoundingGlyph] = useState(null);

  const setCodex = useCodexStore((state) => state.setCodex);
  const addGlyph = useCodexStore((state) => state.addGlyph);
  const navigate = useNavigate(); // For react-router-dom

  const handleBeginRitual = () => setStep(1);

  const handleNameSubmit = (e) => {
    e.preventDefault();
    if (codexName.trim()) {
      setStep(2);
    }
  };

  const handleArchetypeSelect = (archetype) => {
    setSelectedArchetype(archetype);
    setStep(3);
  };

  const handleIntentionSubmit = async (e) => {
    e.preventDefault();
    if (intention.trim()) {
      setIsGenerating(true);
      const generatedGlyph = await generateFoundingGlyph(intention);
      setFoundingGlyph(generatedGlyph);
      setCodex(codexName, selectedArchetype.name, generatedGlyph.id);
      addGlyph(generatedGlyph);
      setIsGenerating(false);
      setStep(4);
    }
  };

  const handleEnterSanctum = () => {
    // Navigate to the home page (assuming /home route)
    navigate('/home');
  };

  const renderStep = () => {
    switch (step) {
      case 0: // Welcome
        return (
          <div className="text-center max-w-md mx-auto space-y-8 flex flex-col items-center">
            <h1 className="text-5xl font-serif font-medium tracking-tight mb-12">GLYPHICA.</h1>
            
            <h2 className="text-3xl font-sans font-light">Welcome, Operator.</h2>
            
            <p className="text-xl font-sans font-light text-zinc-600 dark:text-zinc-400">Glyphica responds to intention.</p>
            <p className="text-xl font-sans font-light text-zinc-600 dark:text-zinc-400">Are you ready to begin your Codex?</p>

            <button
              onClick={handleBeginRitual}
              className="mt-10 px-8 py-3 border border-zinc-800 dark:border-zinc-200 text-zinc-800 dark:text-zinc-200 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors duration-200 text-lg font-sans"
            >
              Begin Ritual
            </button>
          </div>
        );
      case 1: // Name Codex
        return (
          <form onSubmit={handleNameSubmit} className="text-center space-y-6 max-w-md mx-auto">
            <label htmlFor="codexName" className="block text-2xl font-serif mb-6">What shall your Codex be called?</label>
            <input
              id="codexName"
              type="text"
              value={codexName}
              onChange={(e) => setCodexName(e.target.value)}
              className="w-full px-4 py-3 text-center text-xl font-sans bg-transparent border-b-2 border-zinc-400 dark:border-zinc-600 focus:border-black dark:focus:border-white outline-none transition-colors duration-300 placeholder-zinc-400 dark:placeholder-zinc-500"
              placeholder="e.g., The Lunar Chronicle"
              required
              autoFocus
            />
            <p className="text-sm font-sans text-zinc-500 dark:text-zinc-400 italic mt-3">This name is sacred. You may change it later, but its essence will echo.</p>
            <button type="submit" className="mt-6 invisible">Next</button>
          </form>
        );
      case 2: // Choose Archetype
        return (
          <div className="text-center max-w-4xl mx-auto">
            <h2 className="text-2xl font-serif mb-10">Which symbolic archetype guides you now?</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {archetypes.map((arch) => (
                <button
                  key={arch.name}
                  onClick={() => handleArchetypeSelect(arch)}
                  className="p-6 border border-zinc-200 dark:border-zinc-800 rounded-lg text-left hover:border-black dark:hover:border-white hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-all duration-200 space-y-2 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-black"
                >
                  <h3 className="text-xl font-semibold font-serif">{arch.name}</h3>
                  <p className="text-zinc-600 dark:text-zinc-400 text-sm font-sans">{arch.description}</p>
                </button>
              ))}
            </div>
          </div>
        );
      case 3: // Generate Founding Glyph (Intention Input)
        return (
          <form onSubmit={handleIntentionSubmit} className="text-center space-y-4">
            <label htmlFor="intention" className="block text-2xl font-serif mb-4">Set your first intention.</label>
             <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">It may be a word, phrase, or emoji.</p>
            <input
              id="intention"
              type="text"
              value={intention}
              onChange={(e) => setIntention(e.target.value)}
              className="w-full max-w-sm mx-auto px-4 py-3 text-center text-xl bg-transparent border-b-2 border-zinc-400 dark:border-zinc-600 focus:border-zinc-800 dark:focus:border-zinc-200 outline-none transition-colors duration-300"
              placeholder="e.g., Clarity in transition ✨"
              required
              autoFocus
              disabled={isGenerating}
            />
             <button type="submit" className="mt-6 invisible">Generate</button> {/* Hidden submit */}
             {isGenerating && <p className="mt-4 text-lg text-zinc-500 animate-pulse">Generating your founding glyph...</p>}
          </form>
        );
       case 4: // Display Founding Glyph
        return (
          <div className="text-center space-y-6">
            <h2 className="text-2xl font-serif mb-4">Your Founding Glyph</h2>
            {/* Render the actual glyph SVG */}
            <div
                className="w-32 h-32 mx-auto border border-zinc-300 dark:border-zinc-700 flex items-center justify-center bg-zinc-50 dark:bg-zinc-800 rounded-lg shadow-inner"
                dangerouslySetInnerHTML={{ __html: foundingGlyph?.svgData || '' }}
            ></div>
            <div className="text-zinc-600 dark:text-zinc-400 space-y-1 text-sm">
                <p><strong>Founding Glyph:</strong> #{foundingGlyph?.id.split('-')[1].substring(0, 6)}</p>
                <p><strong>Intention:</strong> {foundingGlyph?.intention}</p>
                <p><strong>Entropy Source:</strong> {foundingGlyph?.entropySource}</p>
                <p><strong>Codex Initialized:</strong> {new Date(foundingGlyph?.createdAt).toLocaleString()}</p>
            </div>
            <button
              onClick={handleEnterSanctum}
              className="mt-8 px-6 py-3 bg-zinc-800 dark:bg-zinc-200 text-white dark:text-black font-semibold rounded-lg hover:bg-zinc-700 dark:hover:bg-zinc-300 transition-colors duration-300"
            >
              Enter the Sanctum
            </button>
          </div>
        );
      default:
        return <div>Error: Invalid step</div>;
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white dark:bg-black text-zinc-900 dark:text-zinc-100 p-8 transition-colors duration-500">
      <div className="w-full max-w-3xl">
        {renderStep()}
      </div>
    </div>
  );
} 