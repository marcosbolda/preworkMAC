# Effects for the Ciudad Salud reel, placed from the comp's __events(); then the music bed under them.
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
S = Score(dur=31, T60=1.2)
SCALE = [392.0, 440.0, 523.25, 587.33, 659.25, 783.99, 880.0]
for e in EV:
    t, k = e["t"], e["kind"]
    if k == "draw": S.place(air(1.6, 300, 1400, 1.0, 0.6), t, 0.25, send=0.6)
    elif k == "letters":
        for i in range(6): S.place(wood(240 + 20 * i, 0.07), t + i * 0.055 + 0.08, 0.18)
    elif k == "salud": S.place(glass(783.99, 1.6, 0.6), t, 0.18, send=0.7); S.place(glass(523.25, 1.6, 0.6), t, 0.14, send=0.7)
    elif k == "whoosh": S.place(air(0.6, 250, 2200, 1.2, 0.5), t, 0.35, send=0.5)
    elif k == "tab": S.place(bubble(480 + 90 * e["i"], 0.2), t, 0.25, send=0.3)
    elif k == "land": S.place(sub(60, 0.6), t, 0.35); S.place(wood(200, 0.1), t, 0.3)
    elif k == "card": S.place(glass(SCALE[(e["pi"] + 2 * e["ai"]) % 7], 0.6, 0.5), t, 0.12, send=0.5); S.place(wood(260, 0.06), t, 0.12)
    elif k == "fold": S.place(air(0.45, 1800, 300, 1.2, 0.4), t, 0.25, send=0.4)
    elif k == "slide": S.place(air(0.5, 400, 2400, 1.3, 0.5), t, 0.3, pan=0.4, pan_to=-0.4, send=0.4)
    elif k == "new":
        for f in (659.25, 783.99, 1046.5): S.place(glass(f, 1.4, 0.7), t, 0.14, send=0.7)
    elif k == "push": S.place(air(0.5, 300, 1600, 1.2, 0.5), t, 0.2, send=0.4)
    elif k == "pull": S.place(air(0.5, 1600, 300, 1.2, 0.5), t, 0.2, send=0.4)
    elif k == "end":
        for f in (392.0, 523.25, 659.25, 783.99): S.place(glass(f, 2.6, 0.6), t, 0.15, send=0.75)
        S.place(sub(49, 1.2), t, 0.4)
S.write("sfx.wav")
