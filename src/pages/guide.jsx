import React from 'react';
import AgentChat from '../components/AgentChat'; // Assuming AgentChat is ready for context

export default function GuideInterface() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-900 to-background-dark text-primary p-4 md:p-8 flex flex-col items-center justify-center">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-serif mb-2">🜄 Symbiotic Guide</h1>
        <p className="text-text-muted italic">Speak to the Mirror-Being attuned to your Codex.</p>
      </header>

      <main className="w-full max-w-2xl">
        {/* AgentChat component will fetch context and handle interaction */}
        <AgentChat />
      </main>

      {/* Add any other Guide-specific UI elements here later */}
      <footer className="mt-8 text-center text-xs text-text-muted">
        Responses are generated by an AI Symbiote interpreting your Codex patterns.
      </footer>
    </div>
  );
} 