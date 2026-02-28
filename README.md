# 🚀 Facebook Automation Bot - Premium Edition 🦾

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Playwright](https://img.shields.io/badge/Playwright-Automation-green?style=for-the-badge&logo=playwright)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows)

Uma solução avançada de automação para Facebook projetada especificamente para contornar os sistemas modernos de **Anti-Bot** e **React UI Traps** da Meta. O robô mimetiza o comportamento de um usuário humano real navegando por um dispositivo mobile através do navegador **Comet (Perplexity)**.

---

## ✨ Funcionalidades Avançadas (Anti-Detecção)

O diferencial deste bot não é apenas clicar, mas *como* ele clica e navega.

*   👁️ **X-Ray OCR (Mapeamento Visual):** Ignora bloqueios e "Divs de armadilha" do HTML/React. Escaneia a tela em tempo real pelas coordenadas de texto (ex: "Participar") para comandar o clique físico exato.
*   ⚡ **Deep React Event Injection:** Contorna a interceptação de cliques do React. Quando o clique físico falha, o bot despacha uma sequência sintética completa de eventos nativos do mouse (`mousedown`, `mouseup`, `click`) diretamente no nó do elemento alvo.
*   🧠 **Memória de Elefante (Cooldown 24h):** Sistema inteligente de persistência (`history.json`) que rastreia grupos onde já houve postagens nas últimas 24 horas, ignorando-os no ciclo atual para evitar alertas de SPAM aos administradores.
*   📝 **Auto-Responder de Questionários:** Identifica quando um grupo exige aprovação na entrada. Preenche automaticamente campos de texto, assinala caixas de "Aceito as regras" e clica nas primeiras opções de *Radio Buttons*.
*   🎭 **Síndrome do Impostor (Ansiedade Humana):** 
    *   **Fuga Tática:** Após clicar em "Participar", não fica paralisado. Ele rola a tela nervosamente para cima e para baixo e foge de volta para o feed inicial.
    *   **Idle Scrolling:** Durante os tempos de espera entre ações, rola a página aleatoriamente imitando um humano ocioso lendo o feed.
*   🎯 **Targeted Posting & Keyword Roulette:** Suporta múltiplas palavras-chave separadas por `;`. O bot pode sortear aletas das palavras para espalhar a busca. Também cruza as palavras-chave com a sua lista de "Meus Grupos", garantindo que um anúncio de vendas só caia num grupo focado nisso.
*   🖼️ **Proteção Anti-Hash Image:** Altera metadados e embaralha pixels imperceptivelmente das imagens antes de cada upload, fazendo o Facebook achar que cada post é uma foto 100% inédita.

---

## 🛠️ Tecnologias Utilizadas

- **Playwright:** Automação profunda com injeções de script direto na engine gráfica do navegador.
- **CustomTkinter:** Interface gráfica moderna, estilosa e responsiva (Dark Theme).
- **Pillow:** Processamento de imagem em tempo de execução para evasão de restrições de hash.
- **Comet Browser:** Integração `launch_persistent_context` emulando propriedades nativas de um iPhone 13.

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
1. O executável deve estar na pasta padrão: `%LOCALAPPDATA%\Perplexity\Comet\Application\comet.exe`.
2. **Feche o Comet** manualmente antes de iniciar o bot para liberar a modificação de perfil.

### 3. Interface e Uso
Ao executar o arquivo principal:
```bash
python gui.py
```

Você verá a interface com opções como:
*   **Múltiplas Buscas:** Insira `Vagas; Empregos; Trabalhos` para buscar grupos alternados.
*   **✔ Buscar Novos Grupos:** 
    *   *Marcado:* O bot caçará novos grupos ativamente pela busca, preenchendo regras de entrada.
    *   *Desmarcado:* O bot saltará a caça e postará *apenas* nos grupos que você já foi aprovado.
*   **Performance Sliders:** Controle o tempo ocioso entre postagens, buscas e simulação de erros humanos (Taxa de Erro).

---

## ⚠️ Aviso Legal
Este software foi desenvolvido exclusivamente para fins de Produtividade, Automação Orgânica de Marketing e Estudo de Cibersegurança Web. **O uso de bots excessivos, spams não filtrados e abuso da plataforma violam severamente os Termos de Serviço da Meta (Facebook).** Modere o tempo de execução e as taxas da GUI com sabedoria.

---

<p align="center">
  Desenvolvido com ❤️ por <b>Antigravity AI</b> (Código e Stealth) e por <b>Você</b> (Engenharia Social e Idealização).
</p>
