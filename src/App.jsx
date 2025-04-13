import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useCodexStore } from './context/codexStore';

// Import Page Components
import OnboardingRitual from './pages/index';
import SanctumHome from './pages/home';
import LogRitual from './pages/ritual';
import CodexArchive from './pages/codex';
import AboutGlyphica from './pages/about';
import GuideInterface from './pages/guide';
// Import other pages when they are created
// import GlyphView from './pages/glyph/[id]';

// Import Navigation Component
import Navigation from './components/Navigation';

// A wrapper to protect routes that require an initialized codex
function ProtectedRoute({ children }) {
  const isInitialized = useCodexStore((state) => !!state.codex.createdAt);
  // Simple check: If codex has a creation date, assume it's initialized.
  // More robust checks might be needed later.

  if (!isInitialized) {
    // Redirect them to the onboarding page if not initialized
    // You can replace this logic based on how you want to handle uninitialized users
    return <Navigate to="/" replace />;
  }

  return children;
}

// Helper to conditionally render Navigation
function Layout() {
  const location = useLocation();
  const showNav = location.pathname !== '/'; // Don't show nav on onboarding
  const isInitialized = useCodexStore((state) => !!state.codex.createdAt);

  // Only show nav if not onboarding AND codex is initialized
  const shouldShowNav = showNav && isInitialized;

  return (
    <div className="relative min-h-screen">
       {/* Reserve space for bottom nav if shown */}
       <main className={`${shouldShowNav ? 'pb-16' : ''}`}>
         <Routes>
            {/* Public Routes */}
            <Route path="/" element={<OnboardingRitual />} />
            <Route path="/about" element={<AboutGlyphica />} />

            {/* Protected Routes - require initialized codex */}
            <Route 
              path="/home" 
              element={ <ProtectedRoute> <SanctumHome /> </ProtectedRoute> }
            />
            <Route 
              path="/ritual" 
              element={ <ProtectedRoute> <LogRitual /> </ProtectedRoute> }
            />
            <Route 
              path="/codex" 
              element={ <ProtectedRoute> <CodexArchive /> </ProtectedRoute> }
            />
            <Route 
                path="/guide" 
                element={<ProtectedRoute><GuideInterface /></ProtectedRoute>} 
            />

            {/* Add routes for other pages here as they are built */}
            {/* <Route path="/glyph/:id" element={<ProtectedRoute><GlyphView /></ProtectedRoute>} /> */}
            
            {/* Optional: Catch-all - Redirect to home if initialized, else onboarding */}
            <Route 
                path="*" 
                element={ 
                    isInitialized 
                    ? <Navigate to="/home" replace /> 
                    : <Navigate to="/" replace /> 
                }
            />
          </Routes>
       </main>
       {shouldShowNav && <Navigation />} 
    </div>
  );
}

function App() {
  return (
    <Router>
      <Layout /> 
    </Router>
  );
}

export default App; 