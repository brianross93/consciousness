import React, { useState, useEffect, useRef } from 'react';

const TinnitusMatcher = ({ onBack }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [coarseHz, setCoarseHz] = useState(10000); // Base frequency
  const [fineHz, setFineHz] = useState(0);         // Fine tuning (+/- 50Hz)
  const [matchedFrequency, setMatchedFrequency] = useState(null);
  
  // Refs for Web Audio API
  const audioCtxRef = useRef(null);
  const oscRef = useRef(null);
  const gainRef = useRef(null);

  // Calculate total frequency
  const totalHz = coarseHz + fineHz;

  // Initialize Audio Logic
  useEffect(() => {
    if (isPlaying) {
      // 1. Create Context
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtxRef.current = new AudioContext();
      
      // 2. Create Oscillator
      oscRef.current = audioCtxRef.current.createOscillator();
      oscRef.current.type = 'sine';
      oscRef.current.frequency.value = totalHz;

      // 3. Create Gain (Volume Control - Safety First!)
      gainRef.current = audioCtxRef.current.createGain();
      gainRef.current.gain.value = 0.05; // Keep it VERY quiet (5%)

      // 4. Connect and Start
      oscRef.current.connect(gainRef.current);
      gainRef.current.connect(audioCtxRef.current.destination);
      oscRef.current.start();
    } else {
      // Cleanup
      if (oscRef.current) {
        try { oscRef.current.stop(); } catch(e) {}
        oscRef.current.disconnect();
      }
      if (audioCtxRef.current) {
        audioCtxRef.current.close();
      }
    }

    return () => {
      if (oscRef.current) try { oscRef.current.stop(); } catch(e) {}
    };
  }, [isPlaying]);

  // Live Update Frequency without restarting
  useEffect(() => {
    if (oscRef.current && isPlaying && audioCtxRef.current) {
      oscRef.current.frequency.setValueAtTime(totalHz, audioCtxRef.current.currentTime);
    }
  }, [totalHz, isPlaying]);

  const handleMarkMatch = () => {
    setMatchedFrequency(totalHz);
    // Save to localStorage for future reference
    const matches = JSON.parse(localStorage.getItem('tinnitusMatches') || '[]');
    matches.push({
      frequency: totalHz,
      timestamp: new Date().toISOString(),
      coarse: coarseHz,
      fine: fineHz
    });
    localStorage.setItem('tinnitusMatches', JSON.stringify(matches));
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6 flex flex-col items-center justify-center">
      <div className="max-w-md w-full bg-gray-900 rounded-2xl shadow-2xl p-8 border border-gray-800">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-cyan-400">Heterodyne Tinnitus Matcher</h2>
          {onBack && (
            <button 
              onClick={onBack}
              className="text-gray-400 hover:text-white text-sm"
            >
              ← Back
            </button>
          )}
        </div>
        
        <p className="text-gray-400 text-sm mb-6">
          Slowly adjust until the external tone "locks in" with your tinnitus — 
          you'll hear a distinct wobble or cancellation when frequencies match.
        </p>
        
        {/* Frequency Display */}
        <div className="text-5xl font-mono text-center text-emerald-400 mb-2">
          {totalHz.toLocaleString()}
        </div>
        <div className="text-center text-gray-500 text-sm mb-8">Hz</div>

        {/* Coarse Slider (8kHz - 14kHz) */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <label className="text-sm text-gray-400">Coarse Tune</label>
            <span className="text-xs text-gray-500">8,000 - 14,000 Hz (100Hz steps)</span>
          </div>
          <input 
            type="range" 
            min="8000" 
            max="14000" 
            step="100"
            value={coarseHz} 
            onChange={(e) => setCoarseHz(Number(e.target.value))}
            className="w-full h-3 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-cyan-500"
          />
          <div className="flex justify-between text-xs text-gray-600 mt-1">
            <span>8k</span>
            <span>10k</span>
            <span>12k</span>
            <span>14k</span>
          </div>
        </div>

        {/* Fine Slider (+/- 50Hz) */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <label className="text-sm text-gray-400">Fine Tune</label>
            <span className="text-xs text-gray-500">±50 Hz (1Hz precision)</span>
          </div>
          <input 
            type="range" 
            min="-50" 
            max="50" 
            step="1" 
            value={fineHz} 
            onChange={(e) => setFineHz(Number(e.target.value))}
            className="w-full h-3 bg-blue-900 rounded-lg appearance-none cursor-pointer accent-blue-400"
          />
          <div className="flex justify-between text-xs text-gray-600 mt-1">
            <span>-50</span>
            <span className="text-blue-400">0</span>
            <span>+50</span>
          </div>
        </div>

        {/* Control Buttons */}
        <div className="space-y-3">
          <button 
            onClick={() => setIsPlaying(!isPlaying)}
            className={`w-full py-4 rounded-xl font-bold text-lg transition-all duration-200 ${
              isPlaying 
                ? 'bg-red-600 hover:bg-red-700 shadow-lg shadow-red-900/50' 
                : 'bg-emerald-600 hover:bg-emerald-700 shadow-lg shadow-emerald-900/50'
            }`}
          >
            {isPlaying ? '■ STOP TONE' : '▶ START TEST'}
          </button>

          {isPlaying && (
            <button 
              onClick={handleMarkMatch}
              className="w-full py-3 rounded-xl font-medium bg-purple-600 hover:bg-purple-700 transition-colors"
            >
              📍 Mark This Frequency as Match
            </button>
          )}
        </div>

        {/* Matched Frequency Display */}
        {matchedFrequency && (
          <div className="mt-6 p-4 bg-purple-900/30 border border-purple-700 rounded-lg text-center">
            <div className="text-sm text-purple-300">Matched Frequency</div>
            <div className="text-2xl font-mono text-purple-400">{matchedFrequency.toLocaleString()} Hz</div>
          </div>
        )}

        {/* Safety Warning */}
        <div className="mt-6 p-4 bg-red-900/20 border border-red-800 rounded-lg">
          <p className="text-xs text-red-400 text-center">
            ⚠️ <strong>Safety:</strong> Keep volume low. Do not run for &gt; 1 minute continuously.
            If you're experiencing a spike, wait until tomorrow.
          </p>
        </div>

        {/* Theory Explanation */}
        <div className="mt-6 text-xs text-gray-500">
          <details>
            <summary className="cursor-pointer hover:text-gray-400">How does this work?</summary>
            <p className="mt-2 leading-relaxed">
              This uses the <strong>heterodyne principle</strong>: when two similar frequencies meet, 
              they create a "beat frequency" equal to their difference. When the external tone exactly 
              matches your tinnitus frequency, you'll perceive either cancellation, enhancement, 
              or a distinctive wobble/warble effect. The coarse slider gets you in the ballpark; 
              the fine slider gives you 1Hz precision to find the exact lock-in point.
            </p>
          </details>
        </div>
      </div>
    </div>
  );
};

export default TinnitusMatcher;

