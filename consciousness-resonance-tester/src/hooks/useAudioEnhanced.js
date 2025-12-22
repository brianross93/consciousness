import { useRef, useCallback, useState } from 'react';

/**
 * Enhanced Audio Engine for Frequency Specificity Testing
 * 
 * Tests the hypothesis that gamma entrainment is FREQUENCY-SPECIFIC,
 * not just "any rhythmic stimulus helps"
 * 
 * CONDITIONS (8 total):
 * 1. Silence - baseline
 * 2. Pink Noise - non-specific distraction control
 * 3. 40 Hz Binaural - TARGET (gamma entrainment)
 * 4. 38 Hz Binaural - Near-miss LOW (should interfere)
 * 5. 42 Hz Binaural - Near-miss HIGH (should interfere)
 * 6. 80 Hz Binaural - Octave harmonic (2× gamma)
 * 7. 20 Hz Binaural - Subharmonic (gamma ÷ 2, theta/beta boundary)
 * 8. 53 Hz Binaural - Unrelated frequency (not harmonically related)
 * 
 * HYPOTHESES:
 * - If gamma-specific: 40 Hz > all others
 * - If harmonics matter: 40 ≈ 80 ≈ 20 > 38, 42, 53
 * - If any rhythm helps: All binaural ≈ each other > silence
 * - If frequency irrelevant: All conditions similar
 */

// Condition definitions with metadata for analysis
export const CONDITIONS = {
  1: { 
    id: 1, 
    name: 'Silence', 
    type: 'control',
    frequency: null,
    description: 'Complete silence. Baseline measurement.',
    hypothesis: 'baseline'
  },
  2: { 
    id: 2, 
    name: 'Pink Noise', 
    type: 'control',
    frequency: 'broadband',
    description: 'Filtered noise. Tests if any sound is distracting.',
    hypothesis: 'distraction_control'
  },
  3: { 
    id: 3, 
    name: '40 Hz Binaural', 
    type: 'target',
    frequency: 40,
    baseFreq: 200,
    description: 'Target gamma frequency. Should enhance binding.',
    hypothesis: 'entrainment'
  },
  4: { 
    id: 4, 
    name: '38 Hz Binaural', 
    type: 'near_miss',
    frequency: 38,
    baseFreq: 200,
    description: 'Near-miss LOW. Should interfere with natural gamma.',
    hypothesis: 'interference'
  },
  5: { 
    id: 5, 
    name: '42 Hz Binaural', 
    type: 'near_miss',
    frequency: 42,
    baseFreq: 200,
    description: 'Near-miss HIGH. Should interfere with natural gamma.',
    hypothesis: 'interference'
  },
  6: { 
    id: 6, 
    name: '80 Hz Binaural', 
    type: 'harmonic',
    frequency: 80,
    baseFreq: 200,
    description: 'First overtone (2× gamma). Tests harmonic relationship.',
    hypothesis: 'harmonic'
  },
  7: { 
    id: 7, 
    name: '20 Hz Binaural', 
    type: 'harmonic',
    frequency: 20,
    baseFreq: 200,
    description: 'Subharmonic (gamma ÷ 2). Beta/theta boundary.',
    hypothesis: 'harmonic'
  },
  8: { 
    id: 8, 
    name: '53 Hz Binaural', 
    type: 'unrelated',
    frequency: 53,
    baseFreq: 200,
    description: 'Unrelated frequency. Not harmonically related to 40 Hz.',
    hypothesis: 'unrelated'
  }
};

// Group conditions for analysis
export const CONDITION_GROUPS = {
  control: [1, 2],
  target: [3],
  near_miss: [4, 5],
  harmonic: [6, 7],
  unrelated: [8]
};

// Perceptually-balanced gain settings
const GAIN_SETTINGS = {
  silence: 0,
  pinkNoise: 0.15,
  binaural: 0.5
};

export function useAudioEnhanced() {
  const audioContextRef = useRef(null);
  const nodesRef = useRef([]);
  const [currentCondition, setCurrentCondition] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);

  // Initialize AudioContext
  const initAudio = useCallback(() => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioContextRef.current;
  }, []);

  // Stop all audio
  const stopAll = useCallback(() => {
    nodesRef.current.forEach(node => {
      try {
        if (node.stop) node.stop();
        if (node.disconnect) node.disconnect();
      } catch (e) {
        // Node may already be stopped
      }
    });
    nodesRef.current = [];
    setIsPlaying(false);
  }, []);

  // Play silence (just stop everything)
  const playSilence = useCallback(() => {
    stopAll();
    setCurrentCondition(1);
  }, [stopAll]);

  // Play pink noise
  const playPinkNoise = useCallback((volume = GAIN_SETTINGS.pinkNoise) => {
    stopAll();
    const ctx = initAudio();
    
    const bufferSize = 2 * ctx.sampleRate;
    const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    
    // Pink noise generation (Paul Kellet's algorithm)
    let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      b3 = 0.86650 * b3 + white * 0.3104856;
      b4 = 0.55000 * b4 + white * 0.5329522;
      b5 = -0.7616 * b5 - white * 0.0168980;
      output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.11;
      b6 = white * 0.115926;
    }
    
    const source = ctx.createBufferSource();
    source.buffer = noiseBuffer;
    source.loop = true;
    
    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 2000;
    filter.Q.value = 0.5;
    
    const gainNode = ctx.createGain();
    gainNode.gain.value = volume;
    
    const compressor = ctx.createDynamicsCompressor();
    compressor.threshold.value = -24;
    compressor.knee.value = 30;
    compressor.ratio.value = 12;
    compressor.attack.value = 0.003;
    compressor.release.value = 0.25;
    
    source.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(compressor);
    compressor.connect(ctx.destination);
    source.start();
    
    nodesRef.current = [source, filter, gainNode, compressor];
    setIsPlaying(true);
    setCurrentCondition(2);
  }, [stopAll, initAudio]);

  // Play binaural beat at specified frequency
  const playBinaural = useCallback((beatFrequency, baseFrequency = 200, volume = GAIN_SETTINGS.binaural) => {
    stopAll();
    const ctx = initAudio();
    
    const merger = ctx.createChannelMerger(2);
    
    // Left ear: base frequency
    const oscLeft = ctx.createOscillator();
    oscLeft.type = 'sine';
    oscLeft.frequency.value = baseFrequency;
    
    // Right ear: base + beat frequency
    const oscRight = ctx.createOscillator();
    oscRight.type = 'sine';
    oscRight.frequency.value = baseFrequency + beatFrequency;
    
    // Gains with fade-in
    const gainLeft = ctx.createGain();
    gainLeft.gain.value = 0;
    gainLeft.gain.linearRampToValueAtTime(volume, ctx.currentTime + 1.0);
    
    const gainRight = ctx.createGain();
    gainRight.gain.value = 0;
    gainRight.gain.linearRampToValueAtTime(volume, ctx.currentTime + 1.0);
    
    oscLeft.connect(gainLeft);
    gainLeft.connect(merger, 0, 0);
    
    oscRight.connect(gainRight);
    gainRight.connect(merger, 0, 1);
    
    const compressor = ctx.createDynamicsCompressor();
    compressor.threshold.value = -30;
    compressor.knee.value = 0;
    compressor.ratio.value = 20;
    compressor.attack.value = 0.001;
    compressor.release.value = 0.1;
    
    const limiter = ctx.createGain();
    limiter.gain.value = 0.6;
    
    merger.connect(compressor);
    compressor.connect(limiter);
    limiter.connect(ctx.destination);
    
    oscLeft.start();
    oscRight.start();
    
    nodesRef.current = [oscLeft, oscRight, gainLeft, gainRight, merger, compressor, limiter];
    setIsPlaying(true);
  }, [stopAll, initAudio]);

  // Set audio for a specific phase/condition
  const setPhaseAudio = useCallback((phase) => {
    const condition = CONDITIONS[phase];
    if (!condition) {
      playSilence();
      return;
    }

    setCurrentCondition(phase);

    switch (phase) {
      case 1: // Silence
        playSilence();
        break;
      case 2: // Pink Noise
        playPinkNoise();
        break;
      case 3: // 40 Hz
        playBinaural(40, 200);
        break;
      case 4: // 38 Hz
        playBinaural(38, 200);
        break;
      case 5: // 42 Hz
        playBinaural(42, 200);
        break;
      case 6: // 80 Hz
        playBinaural(80, 200);
        break;
      case 7: // 20 Hz
        playBinaural(20, 200);
        break;
      case 8: // 53 Hz
        playBinaural(53, 200);
        break;
      default:
        playSilence();
    }
  }, [playSilence, playPinkNoise, playBinaural]);

  // Get condition info
  const getConditionLabel = useCallback((phase) => {
    return CONDITIONS[phase]?.name || 'Unknown';
  }, []);

  const getConditionDescription = useCallback((phase) => {
    return CONDITIONS[phase]?.description || '';
  }, []);

  const getConditionInfo = useCallback((phase) => {
    return CONDITIONS[phase] || null;
  }, []);

  // Cleanup
  const cleanup = useCallback(() => {
    stopAll();
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
  }, [stopAll]);

  return {
    initAudio,
    stopAll,
    playSilence,
    playPinkNoise,
    playBinaural,
    setPhaseAudio,
    getConditionLabel,
    getConditionDescription,
    getConditionInfo,
    cleanup,
    currentCondition,
    isPlaying,
    CONDITIONS,
    CONDITION_GROUPS
  };
}

