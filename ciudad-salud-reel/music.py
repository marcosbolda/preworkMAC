# Original music bed for the Vili reel (synthesised here, so it is free of third-party rights).
# 120 BPM in C major, on a grid that puts a beat on every payment of the burst; mixed under sfx.wav.
import numpy as np, wave
from scipy import signal
SR = 48000; DUR = 31.0; N = int(SR * DUR); rng = np.random.default_rng(3)
BEAT = 0.6; T0 = 0.0
def lp(x, f, o=2): b, a = signal.butter(o, f / (SR / 2)); return signal.lfilter(b, a, x)
def hp(x, f, o=2): b, a = signal.butter(o, f / (SR / 2), 'high'); return signal.lfilter(b, a, x)
def tt(n): return np.arange(n) / SR
def saw(f, n, det=0.0):
    t = tt(n); return sum(2 * ((t * f * (1 + d)) % 1) - 1 for d in (-det, 0, det)) / 3
L = np.zeros(N); R = np.zeros(N)
def put(x, t, g=1.0, pan=0.0):
    i = int(t * SR); x = x[:max(0, N - i)]
    if i < 0: x = x[-i:]; i = 0
    L[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 - pan)); R[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 + pan))
def kick():
    n = int(0.35 * SR); t = tt(n); ph = np.cumsum(2 * np.pi * (50 + 110 * np.exp(-t * 38)) / SR)
    return np.tanh(1.6 * np.sin(ph) * np.exp(-t * 9))
def hat(op=False):
    n = int((0.16 if op else 0.05) * SR); return hp(rng.standard_normal(n), 7000) * np.exp(-tt(n) * (18 if op else 70))
def clap():
    n = int(0.22 * SR); x = lp(hp(rng.standard_normal(n), 900), 5000); e = np.exp(-tt(n) * 22)
    for d in (0.0, 0.011, 0.022): e += 0.6 * np.exp(-np.maximum(0, tt(n) - d) * 160) * (tt(n) >= d)
    return x * e * 0.5
def pluck(f, dur=0.35):
    n = int(dur * SR); t = tt(n); x = saw(f, n, 0.004); env = np.exp(-t * 9)
    cut = 900 + 3500 * np.exp(-t * 14); y = np.zeros(n); B = 400
    for i in range(0, n, B): y[i:i + B] = lp(x[max(0, i - 800):i + B], cut[i])[-len(x[i:i + B]):]
    return y * env
def pad(freqs, dur, att=0.6, rel=0.8, cut=1400):
    n = int(dur * SR); t = tt(n); x = sum(saw(f, n, 0.006) for f in freqs) / len(freqs)
    env = np.minimum(1, t / att) * np.minimum(1, (dur - t) / rel).clip(0); return lp(x, cut) * env
def bass(f, dur):
    n = int(dur * SR); t = tt(n); x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return np.tanh(1.3 * x) * np.minimum(1, t / 0.01) * np.exp(-t * 2.2)
CH = {'C': [261.63, 329.63, 392.0], 'Am': [220.0, 261.63, 329.63], 'F': [174.61, 220.0, 261.63], 'G': [196.0, 246.94, 293.66]}
ROOT = {'C': 65.41, 'Am': 55.0, 'F': 87.31, 'G': 98.0}
PROG = ['C', 'Am', 'F', 'G']
def chord_at(t): return PROG[int(np.floor((t - T0) / (4 * BEAT))) % 4]
beats = [T0 + k * BEAT for k in range(int((DUR - T0) / BEAT) + 1)]
def full(t): return 5.6 <= t < 26.2
def light(t): return (0.6 <= t < 5.6) or (26.2 <= t < 30.0)
for k, b in enumerate(beats):
    if b < 0: continue
    c = chord_at(b); tones = CH[c] + [CH[c][0] * 2]
    if full(b) or light(b):
        put(hat(), b + BEAT / 2, 0.05 if light(b) else 0.07, 0.3)
        put(pluck(tones[(2 * k) % 4] * 2, 0.5), b, 0.07, -0.25)
        if full(b): put(pluck(tones[(2 * k + 1) % 4] * 2, 0.4), b + BEAT / 2, 0.05, 0.25)
        if k % 2 == 0 and b >= 3.0: put(kick(), b, 0.28 if full(b) else 0.18); put(bass(ROOT[c], 1.1), b, 0.22)
        if full(b) and k % 4 == 2: put(clap(), b, 0.12, 0.1)
put(pad([261.63, 329.63, 392.0, 493.88], 3.4, 1.2, 0.6, 1000), 0.0, 0.15)
for t0 in (5.6, 12.8, 20.0):
    put(pad([220.0, 261.63, 329.63, 392.0], 7.2, 1.5, 1.5, 900), t0, 0.07)
put(pad([130.81, 261.63, 329.63, 392.0, 587.33], 4.4, 0.1, 2.0, 1500), 26.6, 0.18)
put(bass(65.41, 2.0), 26.6, 0.3)
# little riser into the first payment and into the call
for t0, t1 in ((2.6, 3.2), (25.6, 26.45)):
    n = int((t1 - t0) * SR); t = tt(n) / (t1 - t0); x = hp(rng.standard_normal(n), 2000) * t ** 2 * 0.08; put(x, t0, 1.0)
M = np.stack([L, R], 1)
# fade the tail
M[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))[:, None]
M /= np.abs(M).max() + 1e-9
def rd(p):
    with wave.open(p) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2) / 32768
    return x
S = rd('sfx.wav')[:N]; S = np.pad(S, ((0, N - len(S)), (0, 0)))
# duck the music under the effects
env = lp(np.abs(S).max(1), 8); duck = 1 - 0.3 * np.clip(env / (env.max() + 1e-9) * 2.5, 0, 1)
mix = S * 1.0 + M[:N] * 0.55 * duck[:, None]
mix /= np.abs(mix).max(); mix *= 10 ** (-3.5 / 20)
with wave.open('mix.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((M[:N] * 0.6 * 32767).astype(np.int16).tobytes())
print('wrote mix.wav and music.wav')
