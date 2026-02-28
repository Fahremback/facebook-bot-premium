import asyncio
import os
import random
from playwright.async_api import async_playwright
import config
from utils import human_type, random_sleep, scramble_image, clean_temp_images, human_click, simulate_error

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
        
        # Manual mobile emulation (Stable for Comet)
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=config.USER_DATA_DIR,
            executable_path=config.COMET_EXE_PATH,
            headless=False,
            user_agent=user_agent,
            viewport={"width": 390, "height": 844},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--window-size=390,844",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--app=https://mbasic.facebook.com"
            ]
        )
        
        # When using --app, the first page is automatically our app target
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        await self.page.bring_to_front()
        
        # Manually enforce mobile properties ON THE PAGE
        await self.page.set_viewport_size({"width": 390, "height": 844})
        client = await self.page.context.new_cdp_session(self.page)
        await client.send('Emulation.setTouchEmulationEnabled', {'enabled': True, 'maxTouchPoints': 5})
        await client.send('Emulation.setEmitTouchEventsForMouse', {'enabled': True})
        
        # Intercept and block redirects to m.facebook.com or www.facebook.com, forcing mbasic
        async def handle_route(route):
            url = route.request.url
            if route.request.resource_type in ["document", "navigation"]:
                if "facebook.com" in url and "mbasic" not in url:
                    new_url = url.replace("m.facebook.com", "mbasic.facebook.com").replace("www.facebook.com", "mbasic.facebook.com")
                    self.logger(f"[REDE] Redirecionamento bloqueado. Forçando mbasic.")
                    await route.continue_(url=new_url)
                else:
                    await route.continue_()
            else:
                await route.continue_()
                
        await self.page.route("**/*facebook.com**", handle_route)
        
        # Navigate to the initial mbasic page explicitly
        await self.page.goto("https://mbasic.facebook.com")
        
        self.logger(f"[BOT] Navegador iniciado no Modo Mobile (App Mode)")
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
        error_rate = self.settings.get("error_rate", 5)
        
        await self.page.goto("https://mbasic.facebook.com")
        
        # Randomly fail to "see" things if error rate is hit
        if simulate_error(error_rate):
            self.logger("[NOISE] Human Jitter: Hoje o 'humano' está distraído, navegando menos.")
            return

        for _ in range(random.randint(2, 4)):
            await self.page.mouse.wheel(0, random.randint(300, 700))
            await asyncio.sleep(random.uniform(2, 4))
            likes = await self.page.query_selector_all("a:has-text('Curtir')")
            if likes and random.random() > 0.8:
                await human_click(self.page, random.choice(likes))
                await asyncio.sleep(random.uniform(2, 4))

    async def search_and_join_groups(self):
        import urllib.parse
        keyword = self.settings.get("group_keyword", "")
        if not keyword: return
        
        safe_keyword = urllib.parse.quote_plus(keyword)
        self.logger(f"[SEARCH] Procurando: {keyword}")
        
        # Navigate using the safe URL encoded keyword
        await self.page.goto(f"https://mbasic.facebook.com/search/groups/?q={safe_keyword}")
        await asyncio.sleep(4) # Wait for results to load fully
        
        # Fallback: If Facebook forces the modern React overlay, it traps us on an empty search page
        search_input = await self.page.query_selector("input[type='search'], input[placeholder*='Pesquisar']")
        if search_input and await search_input.is_visible():
            self.logger("[SEARCH] Interface de busca moderna detectada. Tentando injeção direta via script...")
            
            # Use javascript to forcefully set value and trigger React's internal state
            await self.page.evaluate(f'''(keyword) => {{
                let input = document.querySelector('input[type="search"], input[placeholder*="Pesquisar"]');
                if (input) {{
                    input.value = keyword;
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}''', keyword)
            
            await asyncio.sleep(1)
            await self.page.keyboard.press("Enter")
            await asyncio.sleep(5) # Wait for the actual query to execute
            
            # Optionally, we might need to click on the 'Grupos' tab if it exists
            group_tab = await self.page.query_selector("text=/Grupos/i")
            if group_tab and await group_tab.is_visible():
                try:
                    await group_tab.click(force=True, timeout=3000)
                except Exception as e:
                    self.logger(f"[SEARCH] Aviso ao tentar mudar para a aba Grupos: Ignorado (Timeout).")
                await asyncio.sleep(3)
        
        self.logger("[SEARCH] Buscando botões 'Participar' via injeção profunda de script...")
        
        # Inject script to find the text and click its closest clickable container
        clicked_success = await self.page.evaluate('''async () => {
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
            let nodes = [];
            let node;
            while(node = walker.nextNode()) {
                if(node.nodeValue.toLowerCase().trim() === "participar") {
                    nodes.push(node);
                }
            }
            if (nodes.length > 0) {
                for (let n of nodes) {
                    let parent = n.parentElement;
                    // Try to find the closest button or actionable div
                    let clickable = parent.closest('button, a, [role="button"]') || parent;
                    
                    // Check if it's visible (basic check)
                    let style = window.getComputedStyle(clickable);
                    if (style.display !== 'none' && style.visibility !== 'hidden') {
                        clickable.scrollIntoView({block: 'center', behavior: 'instant'});
                        return new Promise((resolve) => {
                            setTimeout(() => {
                                clickable.click();
                                resolve(true);
                            }, 500);
                        });
                    }
                }
            }
            return false;
        }''')
        
        if clicked_success:
            self.logger("[JOIN] Solicitado entrada no grupo (Clique Injetado via Javascript).")
            await asyncio.sleep(5)
        else:
            self.logger("[SEARCH] Nenhum botão 'Participar' encontrado ou clicável nesta página.")

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
        
        last_search_time = 0
        last_post_time = 0
        
        try:
            while self.is_running:
                now = asyncio.get_event_loop().time()
                
                # 0. Noise interaction (every cycle)
                await self.behavioral_noise()
                
                # 1. Search/Join (Independent timer)
                search_interval = self.settings.get("search_frequency", 1800)
                if self.settings.get("group_keyword") and (now - last_search_time >= search_interval):
                    # Simulate human error: occasionally skip search or wait longer
                    if not simulate_error(self.settings.get("error_rate", 5)):
                        await self.search_and_join_groups()
                        last_search_time = now
                    else:
                        self.logger("[NOISE] 'Erro humano' simulado: pulando busca desta vez para parecer mais natural.")
                        last_search_time = now - (search_interval / 2) # Retry sooner

                # 2. Post (Independent timer)
                post_interval = self.settings.get("frequency", 900)
                if (self.settings.get("post_text") or self.settings.get("image_path")) and (now - last_post_time >= post_interval):
                    if not simulate_error(self.settings.get("error_rate", 5)):
                        self.logger("[MAIN] Ciclo de postagem iniciado.")
                        await self.page.goto("https://mbasic.facebook.com/groups/?category=membership")
                        group_links = await self.page.query_selector_all("a[href*='/groups/']")
                        urls = [await g.get_attribute("href") for g in group_links if "/groups/" in await g.get_attribute("href")]
                        clean_urls = list(set([f"https://mbasic.facebook.com{u.split('?')[0]}" for u in urls if u.startswith("/")]))
                        
                        if clean_urls:
                            await self.post_to_group(random.choice(clean_urls))
                            last_post_time = now
                        else:
                            self.logger("[WARNING] Nenhum grupo encontrado para postar.")
                    else:
                        self.logger("[NOISE] 'Erro humano' simulado: pulando postagem desta vez.")
                        last_post_time = now - (post_interval / 2)

                # Wait 60s before checking timers again
                for _ in range(60):
                    if not self.is_running: break
                    await asyncio.sleep(1)
                    
        except Exception as e:
            self.logger(f"[ERROR] {e}")
            if "closed" in str(e).lower() or "not defined" in str(e).lower():
                self.is_running = False
                self.logger("[SISTEMA] Erro crítico ou navegador fechado. Parando execução para evitar spam.")
            else:
                await asyncio.sleep(5) # Prevent infinite fast loops on generic errors

if __name__ == "__main__":
    print("Este arquivo deve ser rodado através do gui.py")
