import asyncio, os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await (await b.new_context(viewport={'width':7560,'height':1350})).new_page()
        await pg.goto('file://'+os.path.abspath('carrusel.html')); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='panorama.png')
        for i in range(7): await pg.screenshot(path=f'placa_{i+1}.png',clip={'x':i*1080,'y':0,'width':1080,'height':1350})
        await b.close()
asyncio.run(main())
