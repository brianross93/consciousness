import { useState, useEffect, useMemo } from 'react';

// Fisher-Yates shuffle
function shuffle(array) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function QuestionCard({ question, onAnswer, questionNumber }) {
  const [selectedOption, setSelectedOption] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Shuffle options when question changes (correct answer position is randomized)
  const shuffledOptions = useMemo(() => {
    return shuffle(question.options);
  }, [question.id, question.options]);

  // Reset selection when question changes
  useEffect(() => {
    setSelectedOption(null);
    setIsSubmitting(false);
  }, [question.id]);

  const handleOptionClick = (option) => {
    if (isSubmitting) return;
    setSelectedOption(option);
  };

  const handleSubmit = () => {
    if (!selectedOption || isSubmitting) return;
    setIsSubmitting(true);
    
    // Brief delay for visual feedback
    setTimeout(() => {
      onAnswer(selectedOption);
    }, 150);
  };

  // Question type badge
  const typeLabels = {
    sequence: 'Pattern',
    analogy: 'Analogy',
    logic: 'Logic',
    letter: 'Sequence'
  };

  const difficultyColors = {
    easy: 'var(--accent-green)',
    moderate: 'var(--accent-yellow)',
    hard: 'var(--accent-magenta)'
  };

  return (
    <div className="card fade-in">
      {/* Question Type & Difficulty Badges */}
      <div style={{ 
        display: 'flex', 
        gap: '0.5rem', 
        marginBottom: '1.5rem' 
      }}>
        <span style={{
          padding: '0.25rem 0.75rem',
          background: 'var(--bg-tertiary)',
          borderRadius: '4px',
          fontSize: '0.75rem',
          color: 'var(--text-muted)',
          textTransform: 'uppercase',
          letterSpacing: '0.05em'
        }}>
          {typeLabels[question.type] || question.type}
        </span>
        <span style={{
          padding: '0.25rem 0.75rem',
          background: 'var(--bg-tertiary)',
          borderRadius: '4px',
          fontSize: '0.75rem',
          color: difficultyColors[question.difficulty] || 'var(--text-muted)',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          borderLeft: `2px solid ${difficultyColors[question.difficulty] || 'var(--text-muted)'}`
        }}>
          {question.difficulty}
        </span>
      </div>

      {/* Question Prompt */}
      <h2 style={{ 
        fontSize: '1.25rem', 
        fontWeight: 500,
        marginBottom: '2rem',
        lineHeight: 1.5,
        color: 'var(--text-primary)'
      }}>
        {question.prompt}
      </h2>

      {/* Options (shuffled so correct answer position varies) */}
      <div style={{ marginBottom: '1.5rem' }}>
        {shuffledOptions.map((option, index) => (
          <button
            key={index}
            className={`btn btn-option ${selectedOption === option ? 'selected' : ''}`}
            onClick={() => handleOptionClick(option)}
            disabled={isSubmitting}
            style={{
              opacity: isSubmitting && selectedOption !== option ? 0.5 : 1
            }}
          >
            <span style={{ 
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '24px',
              height: '24px',
              marginRight: '0.75rem',
              background: selectedOption === option ? 'var(--accent-cyan)' : 'var(--bg-secondary)',
              color: selectedOption === option ? 'var(--bg-primary)' : 'var(--text-muted)',
              borderRadius: '4px',
              fontSize: '0.75rem',
              fontWeight: 600
            }}>
              {String.fromCharCode(65 + index)}
            </span>
            {option}
          </button>
        ))}
      </div>

      {/* Submit Button */}
      <button
        className="btn btn-primary"
        onClick={handleSubmit}
        disabled={!selectedOption || isSubmitting}
        style={{ width: '100%' }}
      >
        {isSubmitting ? 'Submitting...' : 'Submit Answer'}
      </button>

      {/* Keyboard hint */}
      <p style={{ 
        marginTop: '1rem',
        textAlign: 'center',
        fontSize: '0.75rem',
        color: 'var(--text-muted)'
      }}>
        Select an option, then click Submit
      </p>
    </div>
  );
}

export default QuestionCard;

