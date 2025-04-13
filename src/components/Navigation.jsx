import React from 'react';
import { NavLink } from 'react-router-dom';

const navItems = [
  { path: '/home', glyph: '🜁', label: 'Sanctum', tooltip: 'Enter the quiet. Containment precedes insight.' },
  { path: '/ritual', glyph: '🜂', label: 'Ritual', tooltip: 'Make intention visible.' },
  { path: '/codex', glyph: '🜃', label: 'Codex', tooltip: 'Your myth, encoded.' },
  { path: '/guide', glyph: '🜄', label: 'Guide', tooltip: 'Speak to the Mirror.' }, // Assuming /guide will be created
  { path: '/about', glyph: '⊙', label: 'About', tooltip: 'Remember the architecture.' },
];

export default function Navigation() {
  return (
    <nav className="fixed bottom-0 left-0 w-full bg-background-dark/80 backdrop-blur-sm border-t border-border-subtle z-50 flex justify-around items-center h-16">
      {navItems.map(({ path, glyph, label, tooltip }) => (
        <NavLink
          key={path}
          to={path}
          className={({ isActive }) =>
            `flex items-center justify-center h-full px-4 
             text-3xl font-serif transition-all duration-300 ease-in-out transform 
             focus:outline-none group relative 
             ${isActive 
               ? 'text-primary scale-110 opacity-100' // Active state: white, slightly larger
               : 'text-text-muted opacity-70 hover:text-primary hover:opacity-100 hover:scale-105' // Inactive state: muted, fades/scales on hover
            }`
          }
          aria-label={label} // For accessibility
          // title={tooltip} // Simple browser tooltip (can be replaced with custom)
        >
          {glyph}
          {/* Custom Tooltip on Hover - More complex, but aligns with Doctrine */}
           <span 
             className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 
                        px-2 py-1 bg-gray-900 text-text-muted text-xs font-sans rounded-md 
                        opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap pointer-events-none">
             {tooltip}
           </span>
        </NavLink>
      ))}
    </nav>
  );
} 