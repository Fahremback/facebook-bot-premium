# 🚀 Facebook Automation Bot - Premium Edition 🦾

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Playwright](https://img.shields.io/badge/Playwright-Automation-green?style=for-the-badge&logo=playwright)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows)

Uma solução de automação para Facebook de **baixa detecção**, focada em mimetizar o comportamento humano real através do navegador **Comet (Perplexity)**.

---

## ✨ Funcionalidades Principais

*   **📱 Emulação Mobile Real:** Simula um iPhone 13 com suporte a toque e viewport vertical.
*   **🖱️ Movimentação Humana:** Cliques com jitter (tremor) e movimentação de mouse não linear.
*   **⌨️ Digitação Realista:** Digitação caractere por caractere com atrasos variáveis e pausas de "pensamento".
*   **🔄 Timers Independentes:** Frequências separadas para entrar em grupos e para fazer postagens.
*   **🎭 Ruído Comportamental & Taxa de Erro:** Sistema de "erro humano" que pula ações ocasionalmente para parecer um usuário real distraído.
*   **🖼️ Proteção Anti-Hash:** Altera metadados e pixels das imagens automaticamente antes de cada postagem.
*   **💾 Persistência de Dados:** Salva e carrega suas configurações automaticamente em `settings.json`.
*   **🖥️ Interface Moderna:** Controle total via GUI intuitiva (Dark Mode) com labels dinâmicos.

---

## 🛠️ Tecnologias Utilizadas

- **Playwright:** Automação de navegador de última geração com suporte a dispositivos móveis.
- **CustomTkinter:** Interface gráfica moderna, estilosa e responsiva.
- **Pillow:** Processamento inteligente de imagens para evitar detecção de conteúdo repetitivo.
- **Comet Browser:** Integração nativa com o navegador AI da Perplexity.

---

## 🚀 Como Começar

### 1. Pré-requisitos
Certifique-se de ter o Python 3.8+ instalado e as bibliotecas necessárias:

```bash
pip install playwright customtkinter pillow
playwright install chromium
```

### 2. Configuração do Navegador
O bot utiliza o navegador **Comet**. Importante:
1. O executável deve estar em: `C:\Users\fahre\AppData\Local\Perplexity\Comet\Application\comet.exe`.
2. O bot usará seu perfil real da Perplexity/Comet.
3. **Feche o Comet** antes de iniciar o bot para evitar conflitos de perfil.

### 3. Execução
Basta rodar o arquivo da interface principal:

```bash
python gui.py
```

---

## ⚙️ Configurações Sugeridas

| Parâmetro | Sugestão Segura | Por que? |
| :--- | :--- | :--- |
| **Postagem** | 20-40 min | Evita bloqueios por "atividade suspeita". |
| **Busca de Grupos** | 30-60 min | Entrar em muitos grupos rápido é sinal de bot. |
| **Taxa de Erro** | 8-12% | Simula um humano que às vezes para de navegar. |

---

## ⚠️ Aviso Legal
Este bot foi desenvolvido para fins educacionais e de produtividade pessoal. O uso excessivo ou para spam pode violar os termos de serviço da Meta (Facebook). Use com responsabilidade e moderação.

---

<p align="center">
  Desenvolvido com ❤️ por <b>Antigravity AI</b>
</p>
