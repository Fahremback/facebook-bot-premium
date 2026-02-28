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
*   **🎭 Ruído Comportamental:** Rola o feed e curte posts aleatoriamente para "aquecer" a sessão.
*   **🖼️ Proteção Anti-Hash:** Altera metadados e pixels das imagens automaticamente antes de cada postagem.
*   **💾 Persistência de Dados:** Salva e carrega suas configurações automaticamente.
*   **🖥️ Interface Moderna:** Controle total via GUI intuitiva (Dark Mode).

---

## 🛠️ Tecnologias Utilizadas

- **Playwright:** Automação de navegador de última geração.
- **CustomTkinter:** Interface gráfica moderna e responsiva.
- **Pillow:** Processamento inteligente de imagens.
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
O bot utiliza o navegador **Comet**. Certifique-se de:
1. Ter o Comet instalado.
2. Estar logado no Facebook dentro do Comet.
3. **Fechar o Comet** antes de iniciar o bot.

### 3. Execução
Basta rodar o arquivo da interface principal:

```bash
python gui.py
```

---

## ⚙️ Configurações Recomendadas

| Parâmetro | Sugestão Segura | Por que? |
| :--- | :--- | :--- |
| **Frequência** | 15-30 min | Evita ser marcado como spam pela Meta. |
| **Taxa de Erro** | 5-10% | Humanos erram cliques e digitação às vezes. |
| **Tempo Total** | 4-8 horas | Mimetiza uma jornada de trabalho de um CM. |

---

## ⚠️ Aviso Legal
Este bot foi desenvolvido para fins educacionais e de produtividade pessoal. O uso excessivo ou para spam pode violar os termos de serviço da Meta (Facebook). Use com responsabilidade e moderação.

---

<p align="center">
  Desenvolvido com ❤️ por <b>Antigravity AI</b>
</p>
