import sys, json, subprocess, numpy as np, wave
sys.path.insert(0, '/root/.claude/skills/onetake/scripts')
from sfx_palette import *
from playwright.sync_api import sync_playwright
import os
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+os.path.abspath('comp.html')); pg.evaluate('window.__ready'); ev=pg.evaluate('window.__events()'); b.close()
DUR=25.0
s=Score(dur=DUR)
notes=[392,440,494,523,587,659]
for e in ev:
    k,t=e[0],e[1]
    if k=='pop': s.place(bubble(480,0.25),t=t,gain=0.5,send=0.4)
    elif k=='land': s.place(wood(150,0.14),t=t,gain=0.55,send=0.3); s.place(sub(58,0.5),t=t,gain=0.35)
    elif k=='split': [s.place(bubble(f,0.2),t=t+i*0.06,gain=0.38,pan=p,send=0.4) for i,(f,p) in enumerate([(420,-.3),(470,.1),(640,.4)])]
    elif k=='merge': s.place(bubble(380,0.25),t=t+0.12,gain=0.4,send=0.4)
    elif k=='stop': s.place(wood(170+e[2]*12,0.12),t=t,gain=0.45,pan=(-.25 if e[2]%2==0 else .25),send=0.3); s.place(glass(notes[e[2]],0.7,0.5),t=t,gain=0.09,send=0.5)
    elif k=='hop': s.place(air(0.35,400,1800,1.2,0.6),t=t,gain=0.25,send=0.4)
    elif k=='thud': s.place(sub(52,0.7),t=t,gain=0.6); s.place(wood(120,0.16),t=t,gain=0.5,send=0.3)
    elif k=='whoosh': s.place(air(1.2,180,2400,1.3,0.5),t=t,gain=0.4,send=0.5)
    elif k=='list': s.place(air(0.6,300,2000,1.4,0.45),t=t,gain=0.22,send=0.5)
    elif k=='tick': s.place(wood(260,0.08),t=t,gain=0.22,send=0.3)
    elif k=='fly': s.place(air(0.7,250,3000,1.3,0.7),t=t,gain=0.35,send=0.5)
    elif k=='home': s.place(glass(784,1.4,0.7),t=t,gain=0.16,send=0.6); s.place(sub(62,0.8),t=t,gain=0.4)
s.write('sfx.wav')
# mix: VO (take c) delayed 0.4 s over the sfx, loudness-normalised
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','vo/c.mp3','-i','sfx.wav','-filter_complex',
  '[0:a]aresample=48000,adelay=400|400,apad,volume=1.0[v];[1:a]volume=0.55[s];[v][s]amix=inputs=2:duration=longest:normalize=0,atrim=0:25,loudnorm=I=-16:TP=-4:LRA=11,aresample=48000[o]',
  '-map','[o]','-ac','2','mix.wav'],check=True)
print(len(ev),'events')
