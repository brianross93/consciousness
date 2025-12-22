import { useState, useEffect, useCallback } from 'react';
import { useAudioEnhanced, CONDITIONS } from './hooks/useAudioEnhanced';
import WelcomeScreen from './components/WelcomeScreen';
import ExperimentController from './components/ExperimentController';
import ResultsDashboard from './components/ResultsDashboard';
import TinnitusMatcher from './components/TinnitusMatcher';
import questions from './data/questions.json';

// Fisher-Yates shuffle
function shuffle(array) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// Number of phases (8 conditions for frequency specificity testing)
const NUM_PHASES = 8;

function App() {
  const [view, setView] = useState('WELCOME');
  const [phaseOrder, setPhaseOrder] = useState([]);
  const [results, setResults] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const audio = useAudioEnhanced();

  // Generate randomized phase order on mount
  useEffect(() => {
    // Phases 1-8 correspond to the 8 conditions
    const phases = Array.from({ length: NUM_PHASES }, (_, i) => i + 1);
    setPhaseOrder(shuffle(phases));
    setSessionId(Date.now());
  }, []);

  // Cleanup audio on unmount
  useEffect(() => {
    return () => audio.cleanup();
  }, [audio]);

  const handleStart = useCallback(() => {
    audio.initAudio();
    setView('TESTING');
  }, [audio]);

  const handleComplete = useCallback((experimentResults) => {
    audio.stopAll();
    setResults(experimentResults);
    
    // Store results with condition metadata
    const storedResults = JSON.parse(localStorage.getItem('resonanceResultsV2') || '[]');
    storedResults.push({
      sessionId,
      timestamp: new Date().toISOString(),
      phaseOrder,
      conditions: CONDITIONS,
      results: experimentResults,
      version: 2 // Version 2 = frequency specificity test
    });
    localStorage.setItem('resonanceResultsV2', JSON.stringify(storedResults));
    
    setView('RESULTS');
  }, [audio, sessionId, phaseOrder]);

  const handleRestart = useCallback(() => {
    const phases = Array.from({ length: NUM_PHASES }, (_, i) => i + 1);
    setPhaseOrder(shuffle(phases));
    setSessionId(Date.now());
    setResults(null);
    setView('WELCOME');
  }, []);

  const handleOpenTinnitusMatcher = useCallback(() => {
    setView('TINNITUS');
  }, []);

  const handleBackFromTinnitus = useCallback(() => {
    setView('WELCOME');
  }, []);

  return (
    <div className="app">
      {view === 'WELCOME' && (
        <WelcomeScreen 
          onStart={handleStart} 
          onOpenTinnitusMatcher={handleOpenTinnitusMatcher}
        />
      )}
      
      {view === 'TESTING' && (
        <ExperimentController
          questions={questions}
          phaseOrder={phaseOrder}
          audio={audio}
          onComplete={handleComplete}
          numPhases={NUM_PHASES}
        />
      )}
      
      {view === 'RESULTS' && results && (
        <ResultsDashboard
          results={results}
          phaseOrder={phaseOrder}
          audio={audio}
          onRestart={handleRestart}
        />
      )}

      {view === 'TINNITUS' && (
        <TinnitusMatcher onBack={handleBackFromTinnitus} />
      )}
    </div>
  );
}

export default App;
