import { useState, useEffect, useCallback } from 'react';
import { useAudio } from './hooks/useAudio';
import WelcomeScreen from './components/WelcomeScreen';
import ExperimentController from './components/ExperimentController';
import ResultsDashboard from './components/ResultsDashboard';
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

function App() {
  const [view, setView] = useState('WELCOME'); // WELCOME, TESTING, RESULTS
  const [phaseOrder, setPhaseOrder] = useState([1, 2, 3, 4]);
  const [results, setResults] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const audio = useAudio();

  // Generate randomized phase order on mount (5 phases now)
  useEffect(() => {
    setPhaseOrder(shuffle([1, 2, 3, 4, 5]));
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
    
    // Store results in localStorage for aggregation
    const storedResults = JSON.parse(localStorage.getItem('resonanceResults') || '[]');
    storedResults.push({
      sessionId,
      timestamp: new Date().toISOString(),
      phaseOrder,
      results: experimentResults
    });
    localStorage.setItem('resonanceResults', JSON.stringify(storedResults));
    
    setView('RESULTS');
  }, [audio, sessionId, phaseOrder]);

  const handleRestart = useCallback(() => {
    setPhaseOrder(shuffle([1, 2, 3, 4, 5]));
    setSessionId(Date.now());
    setResults(null);
    setView('WELCOME');
  }, []);

  return (
    <div className="app">
      {view === 'WELCOME' && (
        <WelcomeScreen onStart={handleStart} />
      )}
      
      {view === 'TESTING' && (
        <ExperimentController
          questions={questions}
          phaseOrder={phaseOrder}
          audio={audio}
          onComplete={handleComplete}
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
    </div>
  );
}

export default App;

