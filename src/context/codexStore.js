import { create } from 'zustand';

export const useCodexStore = create((set, get) => ({
  codex: {
    name: '',
    archetype: '',
    foundingGlyphId: null,
    createdAt: null,
  },
  glyphs: [], // array of glyph objects
  logs: [],   // array of log entries

  setCodex: (name, archetype, foundingGlyphId) => {
    set({
      codex: {
        name,
        archetype,
        foundingGlyphId,
        createdAt: new Date().toISOString(),
      }
    });
  },

  addGlyph: (glyph) => {
    set({ glyphs: [...get().glyphs, glyph] });
  },

  addLog: (log) => {
    set({ logs: [...get().logs, log] });
  },

  getGlyphById: (id) => {
    return get().glyphs.find((g) => g.id === id);
  },

  getLogsByGlyph: (glyphId) => {
    return get().logs.filter((log) => log.linkedGlyphId === glyphId);
  }
})); 