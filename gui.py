import customtkinter as ctk
import asyncio
import threading
import os
from bot import FacebookBot
from persistence import save_settings, load_settings, load_history

# Configuração de tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Facebook Automation Bot - Premium Edition")
        self.geometry("1100x800")
        self.minsize(950, 700)
        
        self.bot = None
        self.loop = None
        self.bot_thread = None

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Cores customizadas para design moderno
        self.colors = {
            "bg_card": "#212121",        # Fundo dos cartões
            "text_muted": "#8a8a8a",     # Texto secundário
            "accent": "#3b8ed0",         # Azul padrão do tema
            "success": "#2FA572",        # Verde moderno
            "danger": "#E04F5F",         # Vermelho moderno
            "warning": "#E8B931"         # Amarelo/Laranja
        }

        # ==========================================
        # SIDEBAR (COLUNA ESQUERDA)
        # ==========================================
        self.sidebar = ctk.CTkScrollableFrame(self, width=320, corner_radius=0, fg_color="#181818")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo / Título da Sidebar
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🤖 AutoBot PRO", font=("Inter", 24, "bold"), text_color=self.colors["accent"])
        self.logo_label.pack(pady=(20, 30))

        # --- CARD 1: Login ---
        self.frame_login = self.create_card(self.sidebar, "🔑 Credenciais")
        self.login_entry = ctk.CTkEntry(self.frame_login, placeholder_text="E-mail / Telefone", height=38)
        self.login_entry.pack(fill="x", pady=(0, 10))
        self.pass_entry = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", show="•", height=38)
        self.pass_entry.pack(fill="x", pady=(0, 5))

        # --- CARD 2: Alvos ---
        self.frame_target = self.create_card(self.sidebar, "🎯 Busca de Grupos")
        self.keyword_entry = ctk.CTkEntry(self.frame_target, placeholder_text="Ex: Marketing; Vendas; Empregos", height=38)
        self.keyword_entry.pack(fill="x", pady=(0, 10))
        
        self.search_new_groups_var = ctk.BooleanVar(value=True)
        self.checkbox_search = ctk.CTkCheckBox(
            self.frame_target, text="Buscar Novos Grupos", 
            variable=self.search_new_groups_var,
            font=("Inter", 13)
        )
        self.checkbox_search.pack(anchor="w", pady=(5, 5))

        # --- CARD 3: Conteúdo ---
        self.frame_content = self.create_card(self.sidebar, "📝 Conteúdo da Postagem")
        self.text_area = ctk.CTkTextbox(self.frame_content, height=120, border_width=1, border_color="#333333")
        self.text_area.pack(fill="x", pady=(0, 10))
        
        self.btn_image = ctk.CTkButton(
            self.frame_content, text="📸 Selecionar Imagem", 
            command=self.select_image, fg_color="transparent", 
            border_width=1, text_color="white", hover_color="#333333", height=35
        )
        self.btn_image.pack(fill="x", pady=(0, 5))
        
        self.image_label = ctk.CTkLabel(self.frame_content, text="Nenhuma imagem selecionada", font=("Inter", 11), text_color=self.colors["text_muted"])
        self.image_label.pack()
        self.image_path = ""

        # ==========================================
        # MAIN AREA (COLUNA DIREITA)
        # ==========================================
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1) # Faz o log expandir

        # Cabeçalho Principal
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(self.header_frame, text="Painel de Controle", font=("Inter", 28, "bold")).pack(side="left")
        
        self.btn_safe = ctk.CTkButton(
            self.header_frame, text="🛡️ Configuração Segura", 
            fg_color=self.colors["bg_card"], border_color=self.colors["success"], 
            border_width=1, hover_color="#2b3e34", command=self.set_safe_config
        )
        self.btn_safe.pack(side="right")

        # --- CARD 4: Performance (Sliders) ---
        self.frame_performance = ctk.CTkFrame(self.main_frame, fg_color=self.colors["bg_card"], corner_radius=10)
        self.frame_performance.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Grid para colocar 2 sliders lado a lado
        self.frame_performance.grid_columnconfigure((0, 1), weight=1)
        
        self.create_slider(self.frame_performance, "Frequência de Postagem (minutos)", 5, 60, 15, 0, 0)
        self.create_slider(self.frame_performance, "Busca de Grupos (minutos)", 1, 120, 2, 0, 1)
        self.create_slider(self.frame_performance, "Taxa de Erro Humano (%)", 0, 20, 5, 1, 0)
        self.create_slider(self.frame_performance, "Tempo Total de Execução (horas)", 1, 24, 4, 1, 1)

        # --- CARD 5: Terminal / Logs ---
        self.frame_log = ctk.CTkFrame(self.main_frame, fg_color=self.colors["bg_card"], corner_radius=10)
        self.frame_log.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        
        ctk.CTkLabel(self.frame_log, text="Terminal de Atividades", font=("Inter", 14, "bold"), text_color=self.colors["text_muted"]).pack(anchor="w", padx=15, pady=(10, 0))
        self.log_area = ctk.CTkTextbox(self.frame_log, font=("Consolas", 13), fg_color="#0d0d0d", text_color="#00FF00")
        self.log_area.pack(fill="both", expand=True, padx=15, pady=15)

        # --- Controles de Ação ---
        self.frame_actions = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_actions.grid(row=3, column=0, sticky="ew")
        
        self.btn_start = ctk.CTkButton(
            self.frame_actions, text="▶ INICIAR OPERAÇÃO", height=55, 
            font=("Inter", 16, "bold"), fg_color=self.colors["success"], hover_color="#228056",
            command=self.start_bot
        )
        self.btn_start.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_stop = ctk.CTkButton(
            self.frame_actions, text="⏹ PARAR BOT", height=55, 
            font=("Inter", 16, "bold"), fg_color=self.colors["danger"], hover_color="#a83a45",
            state="disabled", command=self.stop_bot
        )
        self.btn_stop.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # Carregar configurações salvas
        self.load_persisted_settings()

    # ==========================================
    # FUNÇÕES DE UI HELPER
    # ==========================================
    def create_card(self, parent, title):
        card = ctk.CTkFrame(parent, fg_color=self.colors["bg_card"], corner_radius=10)
        card.pack(fill="x", padx=15, pady=10)
        lbl = ctk.CTkLabel(card, text=title, font=("Inter", 14, "bold"))
        lbl.pack(anchor="w", padx=15, pady=(15, 10))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", padx=15, pady=(0, 15))
        return content

    def create_slider(self, parent, label_text, min_val, max_val, default, row, col):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=row, column=col, sticky="ew", padx=20, pady=15)
        
        # Cabeçalho do slider (Texto na esquerda, Valor na direita)
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(header, text=label_text, font=("Inter", 13)).pack(side="left")
        value_label = ctk.CTkLabel(header, text=str(default), font=("Inter", 14, "bold"), text_color=self.colors["accent"])
        value_label.pack(side="right")

        var = ctk.IntVar(value=default)
        def update_label(val): value_label.configure(text=str(int(val)))

        slider = ctk.CTkSlider(
            container, from_=min_val, to=max_val, variable=var, 
            number_of_steps=max_val-min_val, command=update_label,
            button_color=self.colors["accent"], progress_color=self.colors["accent"]
        )
        slider.pack(fill="x")
        
        # Atribuir variáveis originais para manter a compatibilidade
        if "Postagem" in label_text: 
            self.freq_var = var
            self.freq_label = value_label
        elif "Busca" in label_text:
            self.search_freq_var = var
            self.search_freq_label = value_label
        elif "Erro" in label_text: 
            self.error_var = var
            self.error_label = value_label
        elif "Execução" in label_text: 
            self.duration_var = var
            self.duration_label = value_label

    # ==========================================
    # LÓGICA DO BOT (MANTIDA INTACTA)
    # ==========================================
    def select_image(self):
        file = ctk.filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.png *.jpeg")])
        if file:
            self.image_path = file
            # Mostra nome abreviado se for muito longo
            name = os.path.basename(file)
            self.image_label.configure(text=name if len(name) < 30 else f"...{name[-25:]}", text_color=self.colors["success"])

    def set_safe_config(self):
        self.freq_var.set(20)
        self.freq_label.configure(text="20")
        
        self.search_freq_var.set(5)
        self.search_freq_label.configure(text="5")
        
        self.error_var.set(8)
        self.error_label.configure(text="8")
        
        self.duration_var.set(6)
        self.duration_label.configure(text="6")
        
        self.log("[SISTEMA] Configurações de proteção aplicadas com sucesso.")

    def load_persisted_settings(self):
        data = load_settings()
        if data:
            if "login" in data: self.login_entry.insert(0, data["login"])
            if "password" in data: self.pass_entry.insert(0, data["password"])
            if "group_keyword" in data: self.keyword_entry.insert(0, data["group_keyword"])
            if "search_new_groups" in data: self.search_new_groups_var.set(data["search_new_groups"])
            if "post_text" in data: self.text_area.insert("1.0", data["post_text"])
            if "image_path" in data and os.path.exists(data["image_path"]):
                self.image_path = data["image_path"]
                name = os.path.basename(self.image_path)
                self.image_label.configure(text=name if len(name) < 30 else f"...{name[-25:]}")
            if "frequency" in data:
                val = data["frequency"] // 60
                self.freq_var.set(val)
                self.freq_label.configure(text=str(val))
            if "search_frequency" in data:
                val = data["search_frequency"] // 60
                self.search_freq_var.set(val)
                self.search_freq_label.configure(text=str(val))
            if "error_rate" in data:
                val = data["error_rate"]
                self.error_var.set(val)
                self.error_label.configure(text=str(val))
            self.log("[SISTEMA] Configurações anteriores carregadas.")

    def log(self, text):
        self.log_area.insert("end", f"{text}\n")
        self.log_area.see("end")

    def start_bot(self):
        settings = {
            "login": self.login_entry.get(),
            "password": self.pass_entry.get(),
            "group_keyword": self.keyword_entry.get(),
            "search_new_groups": self.search_new_groups_var.get(),
            "post_text": self.text_area.get("1.0", "end-1c"),
            "image_path": self.image_path,
            "frequency": self.freq_var.get() * 60,
            "search_frequency": self.search_freq_var.get() * 60,
            "error_rate": self.error_var.get(),
            "duration": self.duration_var.get() * 3600
        }
        
        save_settings(settings)

        self.btn_start.configure(state="disabled", text="⏳ EXECUTANDO...")
        self.btn_stop.configure(state="normal")
        self.log("[SISTEMA] Iniciando bot...")
        
        self.bot_thread = threading.Thread(target=self.run_async_bot, args=(settings,))
        self.bot_thread.daemon = True
        self.bot_thread.start()

    def run_async_bot(self, settings):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.bot = FacebookBot(settings, logger=self.log)
        try:
            self.loop.run_until_complete(self.bot.start())
            self.loop.run_until_complete(self.bot.login())
            
            while self.bot.is_running:
                self.loop.run_until_complete(self.bot.run_cycle())
        except Exception as e:
            self.log(f"[ERRO CRÍTICO] {e}")
        finally:
            self.log("[SISTEMA] Bot finalizado.")
            self.reset_buttons()

    def stop_bot(self):
        if self.bot:
            self.bot.is_running = False
            self.log("[SISTEMA] Solicitação de parada recebida. Finalizando após o ciclo atual...")
        self.btn_stop.configure(state="disabled", text="⏳ PARANDO...")

    def reset_buttons(self):
        self.btn_start.configure(state="normal", text="▶ INICIAR OPERAÇÃO")
        self.btn_stop.configure(state="disabled", text="⏹ PARAR BOT")

if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()