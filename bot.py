import asyncio
import os
import random
from playwright.async_api import async_playwright
import config
from utils import human_type, random_sleep, scramble_image, clean_temp_images, human_click

class FacebookBot:
    def __init__(self, settings=None, logger=None):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.settings = settings or {}
        self.logger = logger or print
        self.is_running = False

    async def start(self):
        self.playwright = await async_playwright().start()
        iphone_13 = self.playwright.devices["iPhone 13"]
        width, height = iphone_13["viewport"]["width"], iphone_13["viewport"]["height"]
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=config.USER_DATA_DIR,
            executable_path=config.COMET_EXE_PATH,
            headless=False,
            device_scale_factor=iphone_13["device_scale_factor"],
            is_mobile=iphone_13["is_mobile"],
            has_touch=iphone_13["has_touch"],
            viewport=iphone_13["viewport"],
            user_agent=iphone_13["user_agent"],
            args=[
                "--disable-blink-features=AutomationControlled",
                f"--window-size={width},{height}",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()
            
        await self.page.goto("https://mbasic.facebook.com")
        self.logger(f"[BOT] Navegador iniciado no Modo Mobile")
        self.is_running = True

    async def login(self):
        # Check if already logged in (look for search bar or feed indicators)
        if await self.page.query_selector("input[name='query'], a[href*='/home.php']"):
            self.logger("[LOGIN] Sessão ativa detectada. Pulando login automático.")
            return

        if "login" in self.page.url or await self.page.query_selector("input[name='email']"):
            self.logger("[LOGIN] Tentando fazer login...")
            email = self.settings.get("login", "")
            password = self.settings.get("password", "")
            
            if email and password:
                await human_type(self.page, "input[name='email']", email)
                await human_type(self.page, "input[name='pass']", password)
                await self.page.click("input[value='Entrar'], button[name='login']")
                await asyncio.sleep(5)
                # Check again
                if await self.page.query_selector("input[name='query']"):
                    self.logger("[SUCCESS] Login realizado!")
                else:
                    self.logger("[WARNING] O login pode ter falhado ou requer intervenção (2FA/Captcha).")
            else:
                self.logger("[WARNING] Credenciais não fornecidas ou incompletas.")

    async def behavioral_noise(self):
        self.logger("[NOISE] Gerando ruído comportamental...")
        await self.page.goto("https://mbasic.facebook.com")
        for _ in range(random.randint(2, 4)):
            await self.page.mouse.wheel(0, random.randint(300, 700))
            await asyncio.sleep(random.uniform(2, 4))
            likes = await self.page.query_selector_all("a:has-text('Curtir')")
            if likes and random.random() > 0.8:
                await human_click(self.page, random.choice(likes))
                await asyncio.sleep(random.uniform(2, 4))

    async def search_and_join_groups(self):
        keyword = self.settings.get("group_keyword", "")
        if not keyword: return
        self.logger(f"[SEARCH] Procurando: {keyword}")
        await self.page.goto(f"https://mbasic.facebook.com/search/groups/?q={keyword}")
        join_btn = await self.page.query_selector("button:has-text('Participar')")
        if join_btn:
            await human_click(self.page, join_btn)
            self.logger("[JOIN] Solicitado.")
            await asyncio.sleep(5)

    async def post_to_group(self, group_url):
        self.logger(f"[POST] Acessando: {group_url}")
        await self.page.goto(group_url)
        
        message = self.settings.get("post_text", "")
        image_path = self.settings.get("image_path", "")

        # 1. Foto primeiro se houver
        if image_path and os.path.exists(image_path):
            self.logger("[POST] Iniciando upload de imagem...")
            photo_btn = await self.page.query_selector("input[name='view_photo']")
            if photo_btn:
                await human_click(self.page, photo_btn)
                file_input = await self.page.wait_for_selector("input[type='file']")
                temp_img = scramble_image(image_path)
                await file_input.set_input_files(temp_img)
                await self.page.click("input[value='Pré-visualizar']")
                # No mbasic, após a foto, você pode adicionar o texto
                if message:
                    await human_type(self.page, "textarea[name='xc_message']", message)
                await self.page.click("input[value='Publicar']")
                self.logger("[SUCCESS] Foto e texto postados.")
                clean_temp_images()
                return

        # 2. Somente texto
        if message:
            text_area = await self.page.query_selector("textarea[name='xc_message']")
            if text_area:
                await human_type(self.page, "textarea[name='xc_message']", message)
                await self.page.click("input[value='Publicar']")
                self.logger("[SUCCESS] Texto postado.")

    async def run_cycle(self):
        if not self.is_running: return
        try:
            await self.behavioral_noise()
            
            # 1. Search/Join (Configurable via keyword)
            if self.settings.get("group_keyword") and random.random() > 0.7:
                await self.search_and_join_groups()
            
            # 2. Post (Only if content is provided)
            if self.settings.get("post_text") or self.settings.get("image_path"):
                self.logger("[MAIN] Conteúdo de postagem detectado. Iniciando ciclo de postagem.")
                await self.page.goto("https://mbasic.facebook.com/groups/?category=membership")
                group_links = await self.page.query_selector_all("a[href*='/groups/']")
                urls = [await g.get_attribute("href") for g in group_links if "/groups/" in await g.get_attribute("href")]
                clean_urls = list(set([f"https://mbasic.facebook.com{u.split('?')[0]}" for u in urls if u.startswith("/")]))
                
                if clean_urls:
                    await self.post_to_group(random.choice(clean_urls))
                else:
                    self.logger("[WARNING] Nenhum grupo encontrado para postar.")
            else:
                self.logger("[INFO] Nenhum texto ou imagem definido. Ciclo de postagem pulado.")
            
            delay = self.settings.get("frequency", 900)
            self.logger(f"[MAIN] Ciclo concluído. Próximo em {delay}s.")
            for _ in range(delay):
                if not self.is_running: break
                await asyncio.sleep(1)
        except Exception as e:
            self.logger(f"[ERROR] {e}")

if __name__ == "__main__":
    print("Este arquivo deve ser rodado através do gui.py")
