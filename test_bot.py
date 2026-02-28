import asyncio
import os
from playwright.async_api import async_playwright
import config
from utils import human_type

async def test_mobile_emulation():
    print("[TEST] Iniciando teste de EMULAÇÃO MOBILE...")
    
    async with async_playwright() as p:
        try:
            iphone_13 = p.devices["iPhone 13"]
            width, height = iphone_13["viewport"]["width"], iphone_13["viewport"]["height"]
            
            print(f"[TEST] Abrindo janela no formato {width}x{height}...")
            
            # Using Comet browser with persistent context
            context = await p.chromium.launch_persistent_context(
                user_data_dir=config.USER_DATA_DIR,
                executable_path=config.COMET_EXE_PATH,
                headless=False,
                args=[
                    f"--window-size={width},{height}",
                    "--disable-blink-features=AutomationControlled"
                ],
                **iphone_13
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            print("[TEST] Acessando mbasic.facebook.com...")
            await page.goto("https://mbasic.facebook.com", timeout=60000)
            
            print(f"[SUCCESS] Conectado! URL: {page.url}")
            print("[INFO] Verifique se a janela aberta está no formato de celular.")
            
            await asyncio.sleep(10) # Give user time to see
            await browser.close()
            
        except Exception as e:
            print(f"[CRITICAL TEST ERROR] {e}")

if __name__ == "__main__":
    asyncio.run(test_mobile_emulation())
