import asyncio
from playwright.async_api import async_playwright
import os
from PIL import Image
import io

async def generate_pdf():
    html_path = "file:///C:/Lindan/Cool/ds/uas/shopee-sentiment-analysis/doc/presentasi_revera.html"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Resolusi tengah (1440x810) agar tidak terlalu besar dan tidak terlalu kecil
        context = await browser.new_context(viewport={"width": 1440, "height": 810})
        page = await context.new_page()
        
        print("Membuka presentasi...")
        await page.goto(html_path)
        
        # Tunggu loading awal dan font
        await page.wait_for_timeout(2000)
        
        images = []
        total_slides = 17
        
        for i in range(total_slides):
            print(f"Mengambil screenshot slide {i+1}...")
            # Tunggu animasi selesai
            await page.wait_for_timeout(1200)
            
            screenshot_bytes = await page.screenshot(full_page=False)
            img = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")
            images.append(img)
            
            # Pindah ke slide selanjutnya
            if i < total_slides - 1:
                await page.keyboard.press("ArrowRight")
        
        await browser.close()
        
        # Simpan sebagai PDF
        pdf_path = "C:/Lindan/Cool/ds/uas/shopee-sentiment-analysis/doc/presentasi_revera.pdf"
        print("Menyimpan ke PDF...")
        if len(images) > 0:
            images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=100.0)
            print(f"Selesai! Disimpan di {pdf_path}")
            
if __name__ == "__main__":
    asyncio.run(generate_pdf())
