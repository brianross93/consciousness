import { useRef, useCallback, useState } from 'react';

/**
 * Audio Engine Hook for Consciousness Resonance Testing
 * 
 * Generates precise audio conditions using Web Audio API:
 * 1. Silence - baseline (no audio)
 * 2. White Noise - thermal/random distraction control (filtered for comfort)
 * 3. 74Hz Isochronic Tone - fixed near-gamma interference (2nd harmonic)
 * 4. 70-90Hz Oscillation - swept gamma interference (2nd harmonic range)
 * 5. 40Hz Binaural Entrainment - gamma synchronization
 * 
 * LOUDNESS NORMALIZATION (Fletcher-Munson):
 * Lower frequencies require more power to match perceived loudness of higher frequencies.
 * We cut the loud (high) frequencies rather than boost quiet (low) ones to prevent clipping.
 */

// Perceptually-balanced gain settings based on Fletcher-Munson equal-loudness contours
// ~6dB cut on binaural (200/240Hz) vs bass tones (74Hz) compensates for frequency response
const GAIN_SETTINGS = {
  silence: 0,
  pinkNoise: 0.15,    // Pink noise is naturally "full" - moderate level
  lowTone: 1.0,       // 74Hz & 70-90Hz sweep need max power for bass perception
  binaural: 0.5       // 200/240Hz cut by 50% (~6dB) to match bass perception
};

export function useAudio() {
  const audioContextRef = useRef(null);
  const nodesRef = useRef([]);
  const [currentCondition, setCurrentCondition] = useState('silence');
  const [isPlaying, setIsPlaying] = useState(false);

  // Initialize AudioContext (must be called after user interaction)
  const initAudio = useCallback(() => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioContextRef.current;
  }, []);

  // Stop all current audio
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
    setCurrentCondition('silence');
  }, []);

  // Condition 1: Silence
  const playSilence = useCallback(() => {
    stopAll();
    setCurrentCondition('silence');
    // No audio nodes needed
  }, [stopAll]);

  // Condition 2: Pink Noise (filtered, perceptually balanced)
  const playWhiteNoise = useCallback((volume = GAIN_SETTINGS.pinkNoise) => {
    stopAll();
    const ctx = initAudio();
    
    // Create noise buffer (2 seconds, looped)
    const bufferSize = 2 * ctx.sampleRate;
    const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    
    // Generate pink noise (softer than white noise - rolls off high frequencies)
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
    
    // Add low-pass filter to make it even softer
    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 2000; // Cut harsh high frequencies
    filter.Q.value = 0.5;
    
    const gainNode = ctx.createGain();
    gainNode.gain.value = volume;
    
    // Add compressor to prevent any clipping
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
    setCurrentCondition('white-noise');
  }, [stopAll, initAudio]);

  // Condition 3: 74Hz Tone (2nd harmonic of 37Hz - easier for headphones)
  // Jams near 80Hz (which is 40Hz × 2), maintaining the "off-resonance" interference
  // Uses max gain (1.0) because bass frequencies need more power for equal perceived loudness
  const playTone = useCallback((frequency = 74, volume = GAIN_SETTINGS.lowTone) => {
    stopAll();
    const ctx = initAudio();
    
    const oscillator = ctx.createOscillator();
    oscillator.type = 'sine';
    oscillator.frequency.value = frequency;
    
    // Pre-gain with fade-in
    const preGain = ctx.createGain();
    preGain.gain.value = 0;
    preGain.gain.linearRampToValueAtTime(volume, ctx.currentTime + 0.5);
    
    // Compressor for safety
    const compressor = ctx.createDynamicsCompressor();
    compressor.threshold.value = -24;
    compressor.knee.value = 10;
    compressor.ratio.value = 12;
    compressor.attack.value = 0.003;
    compressor.release.value = 0.25;
    
    oscillator.connect(preGain);
    preGain.connect(compressor);
    compressor.connect(ctx.destination);
    oscillator.start();
    
    nodesRef.current = [oscillator, preGain, compressor];
    setIsPlaying(true);
    setCurrentCondition('74hz-tone');
  }, [stopAll, initAudio]);

  // Condition 4: 70-90Hz Oscillation (2nd harmonic range - easier for headphones)
  // Sweeps around 80Hz (40Hz × 2), maintaining the "off-resonance" sweep effect
  // Uses max gain (1.0) because bass frequencies need more power for equal perceived loudness
  const playOscillation = useCallback((minHz = 70, maxHz = 90, sweepRate = 0.5, volume = GAIN_SETTINGS.lowTone) => {
    stopAll();
    const ctx = initAudio();
    
    const centerFreq = (minHz + maxHz) / 2; // 80Hz
    const freqWidth = (maxHz - minHz) / 2;  // +/- 10Hz
    
    // Main oscillator (carrier)
    const oscillator = ctx.createOscillator();
    oscillator.type = 'sine';
    oscillator.frequency.value = centerFreq;
    
    // LFO to modulate frequency
    const lfo = ctx.createOscillator();
    lfo.type = 'sine';
    lfo.frequency.value = sweepRate;
    
    // Gain node to scale LFO output to frequency range
    const lfoGain = ctx.createGain();
    lfoGain.gain.value = freqWidth;
    
    // Connect LFO -> lfoGain -> oscillator.frequency
    lfo.connect(lfoGain);
    lfoGain.connect(oscillator.frequency);
    
    // Pre-gain with fade-in
    const preGain = ctx.createGain();
    preGain.gain.value = 0;
    preGain.gain.linearRampToValueAtTime(volume, ctx.currentTime + 0.5);
    
    // Compressor for safety
    const compressor = ctx.createDynamicsCompressor();
    compressor.threshold.value = -24;
    compressor.knee.value = 10;
    compressor.ratio.value = 12;
    compressor.attack.value = 0.003;
    compressor.release.value = 0.25;
    
    oscillator.connect(preGain);
    preGain.connect(compressor);
    compressor.connect(ctx.destination);
    
    oscillator.start();
    lfo.start();
    
    nodesRef.current = [oscillator, lfo, lfoGain, preGain, compressor];
    setIsPlaying(true);
    setCurrentCondition('oscillation');
  }, [stopAll, initAudio]);

  // Condition 5: 40Hz Binaural Beat Entrainment
  // Left ear: 200Hz, Right ear: 240Hz → Brain perceives 40Hz beat
  // Uses 0.5 gain (~6dB cut) because 200Hz is perceptually louder than 74Hz bass
  const playEntrainment = useCallback((beatFrequency = 40, baseFrequency = 200, volume = GAIN_SETTINGS.binaural) => {
    stopAll();
    const ctx = initAudio();
    
    // Create stereo channel merger
    const merger = ctx.createChannelMerger(2);
    
    // Left ear oscillator (base frequency)
    const oscLeft = ctx.createOscillator();
    oscLeft.type = 'sine';
    oscLeft.frequency.value = baseFrequency; // 200Hz
    
    // Right ear oscillator (base + beat frequency)
    const oscRight = ctx.createOscillator();
    oscRight.type = 'sine';
    oscRight.frequency.value = baseFrequency + beatFrequency; // 240Hz
    
    // Individual gain controls for each ear
    const gainLeft = ctx.createGain();
    gainLeft.gain.value = 0;
    gainLeft.gain.linearRampToValueAtTime(volume, ctx.currentTime + 1.0);
    
    const gainRight = ctx.createGain();
    gainRight.gain.value = 0;
    gainRight.gain.linearRampToValueAtTime(volume, ctx.currentTime + 1.0);
    
    // Connect left oscillator to left channel (0)
    oscLeft.connect(gainLeft);
    gainLeft.connect(merger, 0, 0);
    
    // Connect right oscillator to right channel (1)
    oscRight.connect(gainRight);
    gainRight.connect(merger, 0, 1);
    
    // Hard limiter compressor
    const compressor = ctx.createDynamicsCompressor();
    compressor.threshold.value = -30;
    compressor.knee.value = 0;
    compressor.ratio.value = 20;
    compressor.attack.value = 0.001;
    compressor.release.value = 0.1;
    
    // Final output limiter
    const limiter = ctx.createGain();
    limiter.gain.value = 0.6;
    
    merger.connect(compressor);
    compressor.connect(limiter);
    limiter.connect(ctx.destination);
    
    oscLeft.start();
    oscRight.start();
    
    nodesRef.current = [oscLeft, oscRight, gainLeft, gainRight, merger, compressor, limiter];
    setIsPlaying(true);
    setCurrentCondition('40hz-binaural');
  }, [stopAll, initAudio]);

  // Set condition by phase number
  const setPhaseAudio = useCallback((phase) => {
    switch (phase) {
      case 1:
        playSilence();
        break;
      case 2:
        playWhiteNoise();
        break;
      case 3:
        playTone(37);
        break;
      case 4:
        playOscillation();
        break;
      case 5:
        playEntrainment(40);
        break;
      default:
        playSilence();
    }
  }, [playSilence, playWhiteNoise, playTone, playOscillation, playEntrainment]);

  // Get human-readable condition name
  const getConditionLabel = useCallback((phase) => {
    const labels = {
      1: 'Silence (Baseline)',
      2: 'Pink Noise (Control)',
      3: '74 Hz Tone (γ×2 Interference)',
      4: '70-90 Hz Sweep (γ×2 Interference)',
      5: '40 Hz Binaural (Entrainment)'
    };
    return labels[phase] || 'Unknown';
  }, []);

  // Cleanup on unmount
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
    playWhiteNoise,
    playTone,
    playOscillation,
    playEntrainment,
    setPhaseAudio,
    getConditionLabel,
    cleanup,
    currentCondition,
    isPlaying
  };
}
