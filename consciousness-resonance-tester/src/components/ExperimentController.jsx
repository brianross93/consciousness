import { useState, useEffect, useCallback, useMemo } from 'react';
import QuestionCard from './QuestionCard';

// Fisher-Yates shuffle
function shuffle(array) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// Stratified sampling: 4 easy, 3 moderate, 3 hard per phase (5 phases)
function stratifiedSample(questions) {
  const easy = shuffle(questions.easy);
  const moderate = shuffle(questions.moderate);
  const hard = shuffle(questions.hard);
  
  const phases = {};
  
  for (let phase = 1; phase <= 5; phase++) {
    const phaseQuestions = [
      // 4 easy questions
      ...easy.splice(0, 4),
      // 3 moderate questions
      ...moderate.splice(0, 3),
      // 3 hard questions
      ...hard.splice(0, 3)
    ];
    // Shuffle within phase so difficulty order is random
    phases[phase] = shuffle(phaseQuestions);
  }
  
  return phases;
}

function ExperimentController({ questions, phaseOrder, audio, onComplete }) {
  // Stratified sampling: 4 easy + 3 moderate + 3 hard per phase
  const questionAssignments = useMemo(() => {
    return stratifiedSample(questions);
  }, [questions]);

  // State
  const [stage, setStage] = useState('PRACTICE'); // PRACTICE, PHASE_INTRO, PHASE_TEST
  const [currentPhaseIndex, setCurrentPhaseIndex] = useState(0);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [questionStartTime, setQuestionStartTime] = useState(null);
  
  // Results accumulator (5 phases now)
  const [results, setResults] = useState({
    practice: { correct: 0, times: [], questions: [] },
    phases: {
      1: { correct: 0, times: [], questions: [] },
      2: { correct: 0, times: [], questions: [] },
      3: { correct: 0, times: [], questions: [] },
      4: { correct: 0, times: [], questions: [] },
      5: { correct: 0, times: [], questions: [] }
    }
  });

  // Current phase number (from randomized order)
  const currentPhase = phaseOrder[currentPhaseIndex];

  // Current questions based on stage
  const currentQuestions = useMemo(() => {
    if (stage === 'PRACTICE') {
      return questions.practice;
    }
    // Use the stratified question assignments for this phase
    return questionAssignments[currentPhase] || [];
  }, [stage, currentPhase, questions.practice, questionAssignments]);

  const currentQuestion = currentQuestions[currentQuestionIndex];
  const totalQuestionsInStage = currentQuestions.length;

  // Progress calculation
  const overallProgress = useMemo(() => {
    const practiceQuestions = questions.practice.length;
    const phaseQuestions = 10 * 5; // 5 phases, 10 each
    const totalQuestions = practiceQuestions + phaseQuestions;
    
    let completed = 0;
    if (stage === 'PRACTICE') {
      completed = currentQuestionIndex;
    } else {
      completed = practiceQuestions + (currentPhaseIndex * 10) + currentQuestionIndex;
    }
    
    return (completed / totalQuestions) * 100;
  }, [stage, currentPhaseIndex, currentQuestionIndex, questions.practice.length]);

  // Start timer when question appears
  useEffect(() => {
    setQuestionStartTime(Date.now());
  }, [currentQuestionIndex, stage, currentPhaseIndex]);

  // Handle audio for phases
  useEffect(() => {
    if (stage === 'PHASE_TEST') {
      audio.setPhaseAudio(currentPhase);
    } else {
      audio.stopAll();
    }
  }, [stage, currentPhase, audio]);

  // Handle answer submission
  const handleAnswer = useCallback((selectedAnswer) => {
    const responseTime = (Date.now() - questionStartTime) / 1000; // seconds
    const isCorrect = selectedAnswer === currentQuestion.correct;

    // Update results
    setResults(prev => {
      const newResults = JSON.parse(JSON.stringify(prev)); // Deep clone
      
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

    // Move to next question or stage
    const isLastQuestion = currentQuestionIndex >= totalQuestionsInStage - 1;
    
    if (!isLastQuestion) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      // End of current question set
      if (stage === 'PRACTICE') {
        // Move to first phase intro
        setStage('PHASE_INTRO');
        setCurrentQuestionIndex(0);
      } else if (currentPhaseIndex < 4) {
        // Move to next phase intro (5 phases total, index 0-4)
        setCurrentPhaseIndex(prev => prev + 1);
        setStage('PHASE_INTRO');
        setCurrentQuestionIndex(0);
      } else {
        // Experiment complete - pass final results
        // Need to include the last answer in the results
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
    results, onComplete
  ]);

  // Start phase after intro
  const startPhase = useCallback(() => {
    setStage('PHASE_TEST');
  }, []);

  // Render phase intro screen
  if (stage === 'PHASE_INTRO') {
    return (
      <div className="container fade-in" style={{ paddingTop: '4rem' }}>
        <div className="card" style={{ textAlign: 'center', maxWidth: '500px', margin: '0 auto' }}>
          <div className="phase-indicator" style={{ justifyContent: 'center', marginBottom: '2rem' }}>
            <span className="phase-dot"></span>
            <span>Phase {currentPhaseIndex + 1} of 5</span>
          </div>

          <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>
            {audio.getConditionLabel(currentPhase)}
          </h2>

          <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
            {currentPhase === 1 && 'Complete silence. Focus on the questions.'}
            {currentPhase === 2 && 'Background white noise will play. Try to focus through it.'}
            {currentPhase === 3 && 'A 74 Hz tone will play. This is near the 2nd harmonic of gamma (80 Hz).'}
            {currentPhase === 4 && 'A sweeping 70-90 Hz tone will play. It oscillates around gamma×2.'}
            {currentPhase === 5 && 'A binaural beat will play (200Hz left, 240Hz right). Your brain will perceive a 40Hz beat.'}
          </p>

          <div style={{ 
            background: 'var(--bg-tertiary)', 
            padding: '1rem', 
            borderRadius: '8px',
            marginBottom: '2rem',
            fontFamily: 'IBM Plex Mono',
            fontSize: '0.875rem',
            color: 'var(--text-muted)'
          }}>
            10 questions (4 easy • 3 moderate • 3 hard)
          </div>

          <button 
            className="btn btn-primary" 
            onClick={startPhase}
            style={{ width: '100%' }}
          >
            Begin Phase {currentPhaseIndex + 1}
          </button>
        </div>
      </div>
    );
  }

  // Render question
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
            <span>Phase {currentPhaseIndex + 1} / 5</span>
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
          <span>{audio.getConditionLabel(currentPhase)}</span>
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
