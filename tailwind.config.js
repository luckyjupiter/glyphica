const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  content: [
    './templates/**/*.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
        serif: ['EB Garamond', ...defaultTheme.fontFamily.serif],
      },
      colors: {
        primary: '#eaeaea', // Main text/heading color on dark background
        background: {
          dark: '#0e0e11', // Base dark background
        },
        text: {
          base: '#f5f5f5', // Slightly off-white for readability
          muted: '#a0a0a0', // For less important text
        },
        accent: {
          ritual: '#d6a756',        // Gold-toned for encoded intention
          dream: '#b388ff',         // Violet glow for autonomous emergence
          // Add other accents as needed (e.g., for resonance, drift)
        },
        border: {
          subtle: '#2c2c2c', // Subtle borders on dark background
        },
        // Direct color usage if needed
        indigo: {
          // Keep some indigo for consistency with previous buttons unless changed
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
        },
      },
      boxShadow: {
        dream: '0 0 12px 3px rgba(179, 136, 255, 0.4)', // Corresponds to accent.dream
      },
      animation: {
        pulseGlow: 'pulseGlow 3s ease-in-out infinite',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 12px 3px rgba(179, 136, 255, 0.4)' }, // accent.dream at 40% opacity
          '50%': { boxShadow: '0 0 18px 6px rgba(179, 136, 255, 0.6)' }, // accent.dream at 60% opacity
        },
      },
    },
  },
  plugins: [],
}; 