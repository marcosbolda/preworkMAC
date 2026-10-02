# Sound for the Vili film: one palette, one room, placed from the comp's __events().
import sys, os, json, asyncio
sys.path.insert(0, os.path.expanduser("~/.claude/skills/onetake/scripts"))
from sfx_palette import *
from playwright.async_api import async_playwright
async def events():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto("file://" + os.path.abspath("comp.html")); await pg.evaluate("window.__ready")
        ev = await pg.evaluate("window.__events()"); await b.close(); return ev
EV = asyncio.run(events()); json.dump(EV, open("events.json", "w"), indent=1)
S = Score(dur=18, T60=1.0)
# C major pentatonic, climbing through the day
NOTES = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.66, 1318.5]
for e in EV:
    t, k = e["t"], e["kind"]
    if k == "pay":
        i = e["i"]; g = 0.32 if i == 0 else 0.22
        S.place(bubble(420 + 30 * i, 0.22), t, g, send=0.3)
        S.place(glass(1568, 0.5, 0.6), t + 0.03, g * 0.35, send=0.45)
    elif k == "invoice":
        i = e["i"]; g = 0.3 if i == 0 else 0.2
        S.place(wood(230, 0.09), t - 0.02, g * 1.2)
        S.place(glass(NOTES[i], 1.1 if i == 0 else 0.7, 0.8), t, g, send=0.55)
    elif k == "whoosh":
        S.place(air(0.6, 200, 2600, 1.3, 0.55), t, 0.45, pan=0.2, send=0.5, pan_to=-0.2)
    elif k == "whoosh_out":
        S.place(air(0.7, 2400, 260, 1.2, 0.4), t, 0.4, pan=-0.2, send=0.5, pan_to=0.2)
    elif k == "summary":
        for f in (523.25, 659.25, 783.99, 987.77): S.place(glass(f, 2.2, 0.7), t, 0.16, send=0.7)
        S.place(sub(62, 0.8), t, 0.45)
    elif k == "head":
        S.place(sub(55, 0.9), t, 0.4); S.place(air(0.5, 300, 1800, 1.2, 0.3), t - 0.15, 0.25, send=0.4)
    elif k == "pill":
        S.place(bubble(600, 0.2), t, 0.3, send=0.3)
    elif k == "hit":
        S.place(sub(70, 0.35), t, 0.55); S.place(wood(160, 0.1), t, 0.5)
    elif k == "logo":
        for f in (392.0, 523.25, 659.25, 783.99): S.place(glass(f, 2.6, 0.6), t, 0.18, send=0.75)
        S.place(sub(49, 1.2), t, 0.5)
    elif k == "letter":
        S.place(wood(260 + 40 * e["i"], 0.07), t, 0.25)
S.write("sfx.wav")
