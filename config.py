import os

# Configuration for the Facebook Bot (Mobile Emulation enabled in bot.py)

# Content variations for posts (Rotation)
POST_TEXTS = [
    "Olá pessoal, estou passando para compartilhar uma oportunidade incrível!",
    "Bom dia! Alguém aqui já conhece essa novidade? Vale a pena conferir.",
    "Fala pessoal desse grupo! Estou com uma dica valiosa hoje.",
    "Dê uma olhada nisso que encontrei, achei a cara deste grupo!",
    "Novidades fresquinhas para vocês. Espero que gostem do conteúdo."
]

# Search keywords for groups
GROUP_KEYWORDS = [
    "marketing digital",
    "vendas online",
    "oportunidades",
    "tecnologia"
]

# Delay settings (in seconds)
POST_DELAY_RANGE = (300, 900)  # 5 to 15 minutes between posts
NOISE_DELAY_RANGE = (60, 180)   # 1 to 3 minutes of noise/scrolling

# Browser settings
# Using the Comet browser (Perplexity) as requested
COMET_EXE_PATH = os.path.join(os.environ['LOCALAPPDATA'], r"Perplexity\Comet\Application\comet.exe")
USER_DATA_DIR = os.path.join(os.environ['LOCALAPPDATA'], r"Perplexity\Comet\User Data")
PROFILE_DIRECTORY = "Default"

# Image path for posting (place your image in the bot folder)
IMAGE_PATH = "post_image.jpg" 
