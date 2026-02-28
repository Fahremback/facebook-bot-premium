import customtkinter as ctk
import asyncio
import threading
import os
from bot import FacebookBot
from persistence import save_settings, load_settings

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Facebook Automation Bot - Premium")
        self.geometry("900x750")
        
        self.bot = None
        self.loop = None
        self.bot_thread = None

        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Settings) ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="Configurações de Login", font=("Inter", 16, "bold")).pack(pady=10)
        self.login_entry = ctk.CTkEntry(self.sidebar, placeholder_text="E-mail / Telefone")
        self.login_entry.pack(fill="x", padx=20, pady=5)
        self.pass_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Senha", show="*")
        self.pass_entry.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.sidebar, text="Busca de Grupos", font=("Inter", 16, "bold")).pack(pady=10)
        self.keyword_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ex: Marketing Digital")
        self.keyword_entry.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.sidebar, text="Conteúdo da Postagem", font=("Inter", 16, "bold")).pack(pady=10)
        self.text_area = ctk.CTkTextbox(self.sidebar, height=100)
        self.text_area.pack(fill="x", padx=20, pady=5)
        self.btn_image = ctk.CTkButton(self.sidebar, text="Selecionar Imagem", command=self.select_image)
        self.btn_image.pack(fill="x", padx=20, pady=5)
        self.image_label = ctk.CTkLabel(self.sidebar, text="Nenhuma imagem selecionada", font=("Inter", 10))
        self.image_label.pack()
        self.image_path = ""

        # --- Main Area (Controls & Logs) ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.main_frame, text="Controle de Performance", font=("Inter", 20, "bold")).pack(pady=15)

        # Sliders
        self.create_slider("Frequência de Postagem (minutos)", 5, 60, 15)
        self.create_slider("Frequência de Busca de Grupos (minutos)", 10, 120, 30)
        self.create_slider("Taxa de Erro Humano (%)", 0, 20, 5)
        self.create_slider("Tempo Total de Execução (horas)", 1, 24, 4)

        self.btn_safe = ctk.CTkButton(self.main_frame, text="Usar Configurações Seguras", fg_color="green", command=self.set_safe_config)
        self.btn_safe.pack(pady=10)

        # Log Area
        self.log_area = ctk.CTkTextbox(self.main_frame, height=250)
        self.log_area.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Start/Stop Buttons
        self.btn_start = ctk.CTkButton(self.main_frame, text="INICIAR BOT", height=50, font=("Inter", 18, "bold"), command=self.start_bot)
        self.btn_start.pack(side="left", expand=True, padx=20, pady=20)
        
        self.btn_stop = ctk.CTkButton(self.main_frame, text="PARAR BOT", height=50, font=("Inter", 18, "bold"), fg_color="red", state="disabled", command=self.stop_bot)
        self.btn_stop.pack(side="right", expand=True, padx=20, pady=20)

        # Load saved settings
        self.load_persisted_settings()

    def create_slider(self, label, min_val, max_val, default):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill="x", padx=50, pady=5)
        ctk.CTkLabel(frame, text=label).pack(side="left")
        
        value_label = ctk.CTkLabel(frame, text=str(default), width=30)
        value_label.pack(side="right")

        var = ctk.IntVar(value=default)
        def update_label(val): value_label.configure(text=str(int(val)))

        slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, variable=var, 
                              number_of_steps=max_val-min_val, command=update_label)
        slider.pack(side="right", fill="x", expand=True, padx=10)
        
        if "Postagem" in label: 
            self.freq_var = var
            self.freq_label = value_label
        elif "Busca" in label:
            self.search_freq_var = var
            self.search_freq_label = value_label
        elif "Erro" in label: 
            self.error_var = var
            self.error_label = value_label
        elif "Execução" in label: 
            self.duration_var = var
            self.duration_label = value_label

    def select_image(self):
        file = ctk.filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.png *.jpeg")])
        if file:
            self.image_path = file
            self.image_label.configure(text=os.path.basename(file))

    def set_safe_config(self):
        self.freq_var.set(20)
        self.freq_label.configure(text="20")
        
        self.search_freq_var.set(45)
        self.search_freq_label.configure(text="45")
        
        self.error_var.set(8)
        self.error_label.configure(text="8")
        
        self.duration_var.set(6)
        self.duration_label.configure(text="6")
        
        self.log("Configurações seguras aplicadas!")

    def load_persisted_settings(self):
        data = load_settings()
        if data:
            if "login" in data: self.login_entry.insert(0, data["login"])
            if "password" in data: self.pass_entry.insert(0, data["password"])
            if "group_keyword" in data: self.keyword_entry.insert(0, data["group_keyword"])
            if "post_text" in data: self.text_area.insert("1.0", data["post_text"])
            if "image_path" in data:
                self.image_path = data["image_path"]
                self.image_label.configure(text=os.path.basename(self.image_path))
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
            "post_text": self.text_area.get("1.0", "end-1c"),
            "image_path": self.image_path,
            "frequency": self.freq_var.get() * 60,
            "search_frequency": self.search_freq_var.get() * 60,
            "error_rate": self.error_var.get(),
            "duration": self.duration_var.get() * 3600
        }
        
        # Save settings for next time
        save_settings(settings)

        self.btn_start.configure(state="disabled")
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

    def stop_bot(self):
        if self.bot:
            self.bot.is_running = False
            self.log("[SISTEMA] Parando bot após o ciclo atual...")
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")

if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()
