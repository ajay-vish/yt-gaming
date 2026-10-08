"""
Sound Synthesizer: Generates crisp, realistic UI sound effects for YouTube Studio subscriber counter.
Synthesizes high quality 44.1kHz WAV files with pure Python (no external dependencies required).
"""

import math
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 44100

def generate_tick_wav(out_path: Path):
    """Generates a subtle, satisfying wooden/bubble pop tick sound (duration ~40ms)."""
    duration = 0.045
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    
    freq_start = 1400.0
    freq_end = 450.0
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        # Frequency sweep downward
        freq = freq_start + (freq_end - freq_start) * progress
        # Exponential volume decay
        decay = math.exp(-progress * 9.0)
        # Sine wave
        val = math.sin(2 * math.pi * freq * t) * decay * 0.75
        int_val = int(val * 32767)
        samples.append(struct.pack("<h", max(-32768, min(32767, int_val))))
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(samples))
    print(f"Generated tick sound: {out_path}")

def generate_milestone_chime(out_path: Path):
    """Generates a rich, triumphant victory chime chord for milestone achievement (~2.5s)."""
    duration = 2.6
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    
    # Celestial celebratory chord: C5 (523.25), E5 (659.25), G5 (783.99), C6 (1046.50) + harmonics
    frequencies = [523.25, 659.25, 783.99, 1046.50, 1567.98]
    weights = [0.28, 0.25, 0.22, 0.18, 0.07]
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        
        # Smooth fast attack, long shimmering decay
        attack = min(1.0, t / 0.015)
        decay = math.exp(-progress * 2.8)
        shimmer = 1.0 + 0.08 * math.sin(2 * math.pi * 6.0 * t)
        
        val = 0.0
        for f, w in zip(frequencies, weights):
            val += math.sin(2 * math.pi * f * t) * w
            
        sample_val = val * attack * decay * shimmer * 0.95
        int_val = int(sample_val * 32767)
        samples.append(struct.pack("<h", max(-32768, min(32767, int_val))))
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(samples))
    print(f"Generated milestone chime: {out_path}")

def generate_riser_sound(out_path: Path):
    """Generates an anticipation riser / whoosh before the final milestone hits (~1.2s)."""
    duration = 1.2
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        # Exponential frequency rise
        freq = 200.0 + (900.0 - 200.0) * (progress ** 2.2)
        # Crescendo
        amp = (progress ** 1.8) * 0.4
        val = math.sin(2 * math.pi * freq * t) * amp
        int_val = int(val * 32767)
        samples.append(struct.pack("<h", max(-32768, min(32767, int_val))))
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(samples))
    print(f"Generated riser sound: {out_path}")

def generate_shutter_sound(out_path: Path):
    """Generates a realistic camera snapshot / shutter sound effect (~85ms)."""
    duration = 0.085
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # First mechanical click at t=0, second at t=0.038
        click1 = math.exp(-t * 220) * math.sin(2 * math.pi * 1800 * t) if t < 0.035 else 0.0
        t2 = t - 0.038
        click2 = math.exp(-t2 * 180) * math.sin(2 * math.pi * 1200 * t2) if t2 >= 0 else 0.0
        # Gentle white noise transient
        noise = (math.sin(t * 89234.1) % 1.0 - 0.5) * math.exp(-t * 60) * 0.2
        val = (click1 * 0.7 + click2 * 0.65 + noise) * 0.95
        int_val = int(val * 32767)
        samples.append(struct.pack("<h", max(-32768, min(32767, int_val))))
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(samples))
    print(f"Generated shutter sound: {out_path}")

def build_all_sounds():
    base_dir = Path(__file__).resolve().parent.parent / "assets" / "sounds"
    generate_tick_wav(base_dir / "tick.wav")
    generate_milestone_chime(base_dir / "milestone_ding.wav")
    generate_riser_sound(base_dir / "riser.wav")
    generate_shutter_sound(base_dir / "shutter.wav")

if __name__ == "__main__":
    build_all_sounds()
