import { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import QuestionCard from './QuestionCard';
import { CONDITIONS } from '../hooks/useAudioEnhanced';

// Fisher-Yates shuffle
function shuffle(array) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// Questions per phase: 3 easy, 2 moderate, 1 hard = 6 total
// 8 phases × 6 questions = 48 questions needed
const QUESTIONS_PER_PHASE = 6;
const EASY_PER_PHASE = 3;
const MODERATE_PER_PHASE = 2;
const HARD_PER_PHASE = 1;

// Pre-exposure duration in seconds (research suggests 6+ min for full effect)
// 3 minutes pre-exposure + ~3 min questions = ~6 min total per condition
const PRE_EXPOSURE_SECONDS = 180; // 3 minutes

// Stratified sampling for 8 phases
function stratifiedSample(questions, numPhases) {
  const easy = shuffle(questions.easy);
  const moderate = shuffle(questions.moderate);
  const hard = shuffle(questions.hard);
  
  const phases = {};
  
  for (let phase = 1; phase <= numPhases; phase++) {
    const phaseQuestions = [
      ...easy.splice(0, EASY_PER_PHASE),
      ...moderate.splice(0, MODERATE_PER_PHASE),
      ...hard.splice(0, HARD_PER_PHASE)
    ];
    phases[phase] = shuffle(phaseQuestions);
  }
  
  return phases;
}

function ExperimentController({ questions, phaseOrder, audio, onComplete, numPhases = 8 }) {
  // Stratified sampling
  const questionAssignments = useMemo(() => {
    return stratifiedSample(questions, numPhases);
  }, [questions, numPhases]);

  // State
  const [stage, setStage] = useState('PRACTICE'); // PRACTICE, PHASE_INTRO, PRE_EXPOSURE, PHASE_TEST
  const [currentPhaseIndex, setCurrentPhaseIndex] = useState(0);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [questionStartTime, setQuestionStartTime] = useState(null);
  
  // Pre-exposure timer state
  const [preExposureRemaining, setPreExposureRemaining] = useState(PRE_EXPOSURE_SECONDS);
  const timerRef = useRef(null);
  
  // Initialize results for all phases
  const initialPhaseResults = useMemo(() => {
    const phases = {};
    for (let i = 1; i <= numPhases; i++) {
      phases[i] = { correct: 0, times: [], questions: [] };
    }
    return phases;
  }, [numPhases]);

  const [results, setResults] = useState({
    practice: { correct: 0, times: [], questions: [] },
    phases: initialPhaseResults
  });

  // Current phase number (from randomized order)
  const currentPhase = phaseOrder[currentPhaseIndex];

  // Current questions based on stage
  const currentQuestions = useMemo(() => {
    if (stage === 'PRACTICE') {
      return questions.practice;
    }
    return questionAssignments[currentPhase] || [];
  }, [stage, currentPhase, questions.practice, questionAssignments]);

  const currentQuestion = currentQuestions[currentQuestionIndex];
  const totalQuestionsInStage = currentQuestions.length;

  // Progress calculation (now includes pre-exposure time)
  const overallProgress = useMemo(() => {
    const practiceQuestions = questions.practice.length;
    const phaseQuestions = QUESTIONS_PER_PHASE * numPhases;
    const totalQuestions = practiceQuestions + phaseQuestions;
    
    let completed = 0;
    if (stage === 'PRACTICE') {
      completed = currentQuestionIndex;
    } else if (stage === 'PHASE_INTRO' || stage === 'PRE_EXPOSURE') {
      completed = practiceQuestions + (currentPhaseIndex * QUESTIONS_PER_PHASE);
    } else {
      completed = practiceQuestions + (currentPhaseIndex * QUESTIONS_PER_PHASE) + currentQuestionIndex;
    }
    
    return (completed / totalQuestions) * 100;
  }, [stage, currentPhaseIndex, currentQuestionIndex, questions.practice.length, numPhases]);

  // Start timer when question appears
  useEffect(() => {
    if (stage === 'PHASE_TEST' || stage === 'PRACTICE') {
      setQuestionStartTime(Date.now());
    }
  }, [currentQuestionIndex, stage, currentPhaseIndex]);

  // Handle audio for phases
  useEffect(() => {
    if (stage === 'PHASE_TEST' || stage === 'PRE_EXPOSURE') {
      audio.setPhaseAudio(currentPhase);
    } else {
      audio.stopAll();
    }
  }, [stage, currentPhase, audio]);

  // Pre-exposure countdown timer
  useEffect(() => {
    if (stage === 'PRE_EXPOSURE') {
      setPreExposureRemaining(PRE_EXPOSURE_SECONDS);
      
      timerRef.current = setInterval(() => {
        setPreExposureRemaining(prev => {
          if (prev <= 1) {
            clearInterval(timerRef.current);
            setStage('PHASE_TEST');
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      
      return () => {
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }
      };
    }
  }, [stage]);

  // Handle answer submission
  const handleAnswer = useCallback((selectedAnswer) => {
    const responseTime = (Date.now() - questionStartTime) / 1000;
    const isCorrect = selectedAnswer === currentQuestion.correct;

    setResults(prev => {
      const newResults = JSON.parse(JSON.stringify(prev));
      
      if (stage === 'PRACTICE') {
        newResults.practice.correct += isCorrect ? 1 : 0;
        newResults.practice.times.push(responseTime);
        newResults.practice.questions.push({
          id: currentQuestion.id,
          correct: isCorrect,
          time: responseTime
        });
      } else {
        newResults.phases[currentPhase].correct += isCorrect ? 1 : 0;
        newResults.phases[currentPhase].times.push(responseTime);
        newResults.phases[currentPhase].questions.push({
          id: currentQuestion.id,
          correct: isCorrect,
          time: responseTime,
          difficulty: currentQuestion.difficulty
        });
      }
      
      return newResults;
    });

    const isLastQuestion = currentQuestionIndex >= totalQuestionsInStage - 1;
    
    if (!isLastQuestion) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      if (stage === 'PRACTICE') {
        setStage('PHASE_INTRO');
        setCurrentQuestionIndex(0);
      } else if (currentPhaseIndex < numPhases - 1) {
        setCurrentPhaseIndex(prev => prev + 1);
        setStage('PHASE_INTRO');
        setCurrentQuestionIndex(0);
      } else {
        // Complete - include final answer
        const finalResults = JSON.parse(JSON.stringify(results));
        finalResults.phases[currentPhase].correct += isCorrect ? 1 : 0;
        finalResults.phases[currentPhase].times.push(responseTime);
        finalResults.phases[currentPhase].questions.push({
          id: currentQuestion.id,
          correct: isCorrect,
          time: responseTime,
          difficulty: currentQuestion.difficulty
        });
        onComplete(finalResults);
      }
    }
  }, [
    questionStartTime, currentQuestion, stage, currentPhase,
    currentQuestionIndex, totalQuestionsInStage, currentPhaseIndex,
    results, onComplete, numPhases
  ]);

  // Start pre-exposure period
  const startPreExposure = useCallback(() => {
    setStage('PRE_EXPOSURE');
  }, []);

  // Skip pre-exposure (for testing/debugging)
  const skipPreExposure = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    setStage('PHASE_TEST');
  }, []);

  // Get condition info for display
  const conditionInfo = CONDITIONS[currentPhase];

  // Format time as MM:SS
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Render pre-exposure screen
  if (stage === 'PRE_EXPOSURE') {
    const progress = ((PRE_EXPOSURE_SECONDS - preExposureRemaining) / PRE_EXPOSURE_SECONDS) * 100;
    
    return (
      <div className="container fade-in" style={{ paddingTop: '4rem' }}>
        <div className="card" style={{ textAlign: 'center', maxWidth: '550px', margin: '0 auto' }}>
          <div className="phase-indicator" style={{ justifyContent: 'center', marginBottom: '1rem' }}>
            <span className="phase-dot"></span>
            <span>Phase {currentPhaseIndex + 1} of {numPhases}</span>
          </div>

          <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
            Pre-Exposure Period
          </h2>
          
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Relax and listen to the audio. Questions will begin automatically.
          </p>

          {/* Audio condition display */}
          <div style={{
            background: 'var(--bg-tertiary)',
            padding: '1.5rem',
            borderRadius: '12px',
            marginBottom: '2rem'
          }}>
            <div className="audio-status" style={{ justifyContent: 'center', marginBottom: '1rem' }}>
              <div className="audio-wave">
                <span></span><span></span><span></span><span></span><span></span>
              </div>
              <span style={{ fontSize: '1.1rem', fontWeight: 500 }}>
                {conditionInfo?.name}
                {conditionInfo?.frequency && typeof conditionInfo.frequency === 'number' && 
                  ` (${conditionInfo.frequency} Hz)`}
              </span>
            </div>
            
            <p style={{ 
              fontSize: '0.85rem', 
              color: 'var(--text-muted)', 
              margin: 0 
            }}>
              {conditionInfo?.description}
            </p>
          </div>

          {/* Timer display */}
          <div style={{ marginBottom: '2rem' }}>
            <div style={{
              fontSize: '3rem',
              fontFamily: 'IBM Plex Mono',
              fontWeight: 600,
              color: 'var(--accent-cyan)',
              marginBottom: '0.5rem'
            }}>
              {formatTime(preExposureRemaining)}
            </div>
            <p style={{ 
              fontSize: '0.85rem', 
              color: 'var(--text-muted)',
              margin: 0
            }}>
              remaining before questions
            </p>
          </div>

          {/* Progress bar */}
          <div style={{
            background: 'var(--bg-secondary)',
            borderRadius: '4px',
            height: '8px',
            overflow: 'hidden',
            marginBottom: '1.5rem'
          }}>
            <div style={{
              background: 'linear-gradient(90deg, var(--accent-cyan), var(--accent-magenta))',
              height: '100%',
              width: `${progress}%`,
              transition: 'width 1s linear'
            }} />
          </div>

          {/* Why pre-exposure */}
          <div style={{
            background: 'rgba(0, 212, 255, 0.05)',
            padding: '1rem',
            borderRadius: '8px',
            fontSize: '0.8rem',
            color: 'var(--text-muted)',
            textAlign: 'left',
            marginBottom: '1rem'
          }}>
            <strong style={{ color: 'var(--text-secondary)' }}>Why wait?</strong>
            <p style={{ margin: '0.5rem 0 0' }}>
              Research shows neural entrainment takes ~6 minutes to stabilize. 
              This pre-exposure period allows the audio frequency to affect your brain rhythms 
              before we measure cognitive performance.
            </p>
          </div>

          {/* Skip button (small, for testing) */}
          <button 
            onClick={skipPreExposure}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              fontSize: '0.75rem',
              cursor: 'pointer',
              padding: '0.5rem'
            }}
          >
            Skip (testing only)
          </button>
        </div>
      </div>
    );
  }

  // Render phase intro screen
  if (stage === 'PHASE_INTRO') {
    return (
      <div className="container fade-in" style={{ paddingTop: '4rem' }}>
        <div className="card" style={{ textAlign: 'center', maxWidth: '550px', margin: '0 auto' }}>
          <div className="phase-indicator" style={{ justifyContent: 'center', marginBottom: '2rem' }}>
            <span className="phase-dot"></span>
            <span>Phase {currentPhaseIndex + 1} of {numPhases}</span>
          </div>

          <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
            {conditionInfo?.name || `Condition ${currentPhase}`}
          </h2>

          {conditionInfo?.frequency && (
            <div style={{ 
              fontFamily: 'IBM Plex Mono',
              fontSize: '0.875rem',
              color: 'var(--accent-cyan)',
              marginBottom: '1rem'
            }}>
              {typeof conditionInfo.frequency === 'number' 
                ? `${conditionInfo.frequency} Hz binaural beat`
                : conditionInfo.frequency}
            </div>
          )}

          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            {conditionInfo?.description}
          </p>

          {/* Condition type badge */}
          <div style={{
            display: 'inline-block',
            padding: '0.25rem 0.75rem',
            borderRadius: '4px',
            fontSize: '0.75rem',
            fontFamily: 'IBM Plex Mono',
            textTransform: 'uppercase',
            marginBottom: '1.5rem',
            background: conditionInfo?.type === 'target' ? 'rgba(0, 255, 136, 0.2)' :
                       conditionInfo?.type === 'control' ? 'rgba(136, 136, 136, 0.2)' :
                       conditionInfo?.type === 'near_miss' ? 'rgba(255, 136, 0, 0.2)' :
                       conditionInfo?.type === 'harmonic' ? 'rgba(0, 136, 255, 0.2)' :
                       'rgba(136, 0, 255, 0.2)',
            color: conditionInfo?.type === 'target' ? 'var(--accent-green)' :
                   conditionInfo?.type === 'control' ? 'var(--text-muted)' :
                   conditionInfo?.type === 'near_miss' ? 'var(--accent-yellow)' :
                   conditionInfo?.type === 'harmonic' ? 'var(--accent-cyan)' :
                   'var(--accent-purple)'
          }}>
            {conditionInfo?.type?.replace('_', ' ')}
          </div>

          {/* Phase structure */}
          <div style={{ 
            background: 'var(--bg-tertiary)', 
            padding: '1rem', 
            borderRadius: '8px',
            marginBottom: '1.5rem',
            textAlign: 'left'
          }}>
            <div style={{ 
              fontFamily: 'IBM Plex Mono',
              fontSize: '0.85rem',
              color: 'var(--text-secondary)',
              marginBottom: '0.5rem'
            }}>
              Phase structure:
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              <div style={{ marginBottom: '0.25rem' }}>
                1. <strong>{Math.floor(PRE_EXPOSURE_SECONDS / 60)} min</strong> audio pre-exposure (listen & relax)
              </div>
              <div>
                2. <strong>{QUESTIONS_PER_PHASE} questions</strong> ({EASY_PER_PHASE} easy • {MODERATE_PER_PHASE} moderate • {HARD_PER_PHASE} hard)
              </div>
            </div>
          </div>

          <p style={{ 
            fontSize: '0.8rem', 
            color: 'var(--text-muted)',
            marginBottom: '1.5rem'
          }}>
            Total phase time: ~{Math.floor(PRE_EXPOSURE_SECONDS / 60) + 3} minutes
          </p>

          <button 
            className="btn btn-primary" 
            onClick={startPreExposure}
            style={{ width: '100%' }}
          >
            Start Pre-Exposure
          </button>
        </div>
      </div>
    );
  }

  if (!currentQuestion) {
    return <div className="container">Loading...</div>;
  }

  return (
    <div className="container fade-in">
      {/* Progress Bar */}
      <div className="progress-container">
        <div 
          className="progress-bar" 
          style={{ width: `${overallProgress}%` }}
        />
      </div>

      {/* Stage Indicator */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '1.5rem'
      }}>
        {stage === 'PRACTICE' ? (
          <div className="phase-indicator">
            <span className="phase-dot" style={{ background: 'var(--accent-yellow)' }}></span>
            <span>Practice Round</span>
          </div>
        ) : (
          <div className="phase-indicator">
            <span className="phase-dot"></span>
            <span>Phase {currentPhaseIndex + 1} / {numPhases}</span>
          </div>
        )}

        <span style={{ 
          fontFamily: 'IBM Plex Mono', 
          fontSize: '0.875rem',
          color: 'var(--text-muted)'
        }}>
          Q{currentQuestionIndex + 1}/{totalQuestionsInStage}
        </span>
      </div>

      {/* Audio Status */}
      {stage === 'PHASE_TEST' && (
        <div className="audio-status">
          <div className={`audio-wave ${currentPhase === 1 ? 'silent' : ''}`}>
            <span></span><span></span><span></span><span></span><span></span>
          </div>
          <span>
            {conditionInfo?.name}
            {conditionInfo?.frequency && typeof conditionInfo.frequency === 'number' && 
              ` (${conditionInfo.frequency} Hz)`}
          </span>
        </div>
      )}

      {/* Question Card */}
      <QuestionCard
        question={currentQuestion}
        onAnswer={handleAnswer}
        questionNumber={currentQuestionIndex + 1}
      />
    </div>
  );
}

export default ExperimentController;
