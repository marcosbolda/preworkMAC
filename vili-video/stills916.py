import asyncio, io, os, sys
from PIL import Image, ImageDraw
from playwright.async_api import async_playwright
comp, out, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1080,"height":1920})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file://"+os.path.abspath(comp)); await pg.evaluate("window.__ready")
        tiles=[]
        for t in ts:
            await pg.evaluate(f"window.__seek({t})")
            im=Image.open(io.BytesIO(await pg.screenshot())).resize((360,640)); ImageDraw.Draw(im).text((6,6),f"t={t}",fill=(255,255,0)); tiles.append(im)
        await b.close()
    cols=6; rows=(len(tiles)+cols-1)//cols; s=Image.new("RGB",(360*cols,640*rows))
    for i,im in enumerate(tiles): s.paste(im,((i%cols)*360,(i//cols)*640))
    s.save(out); print("errors:", errs[:3] or "none")
asyncio.run(main())
