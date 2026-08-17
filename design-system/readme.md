# Danielly Curione — Design System (direção 1b · Acolhedora quente)

Design system para o site institucional de Danielly Curione, psicóloga clínica e psicanalista (CRP 05/77951, Niterói-RJ). Migração Wix → WordPress/Elementor, 10 páginas. Este pacote documenta a direção visual **aprovada pela cliente**: "Acolhedora quente".

Fontes: briefing de design da cliente (posicionamento, públicos, arquitetura de 10 páginas), logo oficial fornecido em raster (vetorizado aqui), fotos reais do consultório e retrato da profissional, documento "Áreas de atuação" (finalidades da avaliação psicológica).

## Índice
- `styles.css` — entry point, importa todos os tokens.
- `tokens/` — `colors.css`, `typography.css`, `spacing.css`, `radii.css`.
- `components/core/` — Button, Chip.
- `components/cards/` — ServiceCard.
- `components/content/` — QuoteBlock.
- `components/forms/` — WhatsAppScheduler (agendador funcional, sem backend).
- `assets/` — logo vetorizado (símbolo + lockup vertical, claro e escuro) e fotos reais.
- `guidelines/` — specimens de cor, tipografia, espaçamento, marca e fotografia.

## Conteúdo — tom e voz
Escuta ética e acolhedora, elegante sem ser fria. Primeira pessoa quando fala da prática ("Trabalho com..."), segunda pessoa ao dirigir-se ao visitante ("Você escreve pelo WhatsApp..."). Frases médias, sem jargão clínico. Nenhum emoji. A citação de Ferenczi — *"O que cura é o afeto: não há terapia sem simpatia"* — é a única citação de autoridade do site; nunca depoimentos de pacientes (vedado por CFP/YMYL).

Proibições de conteúdo, sempre: depoimentos de pacientes, menção a mestrado (não existe), citação de plataformas de telepsicologia (Conexa etc.), avaliações do Google (não há), promessas de resultado terapêutico, clichês visuais de psicologia (cérebro, quebra-cabeça, mãos em concha) e estética de coach motivacional.

## Fundamentos visuais
- **Cor:** base creme (`--color-cream` `#FBF3E8`), painéis num creme mais claro (`--color-cream-panel` `#FFFAF2`), acento madeira (`--color-wood` `#E8D5BC`). Cor de marca em dois tons quentes — mustard `#C8871F` (CTA primário) e terracota `#B96A4B` (CTA secundário, links). Texto em `--color-ink` `#2A211B` (quase preto, nunca preto puro) e corpo em `--color-ink-soft` `#5C4C3F`. Rodapé inverte para `--color-ink` como fundo.
- **Tipografia:** títulos em Newsreader (serifada, peso 300–400, às vezes itálico nas citações); corpo e UI em Nunito Sans (300/400 no texto corrido, 700 em rótulos e botões). Rótulos em caixa alta com tracking largo (.14–.24em).
- **Forma:** cantos muito arredondados — pill (999px) em botões, chips e no formulário; 18–24px em cards e painéis. Sem sombras duras; only a sombra suave sob o CTA principal (mustard, 35% opacidade).
- **Imagens:** fotografia real da profissional e do consultório, nunca banco de imagens. Recortes em blocos retos ou levemente arredondados, nunca círculos decorativos.
- **Animação:** nenhuma até o momento — o site é estático; hover apenas reduz opacidade dos links (72%).
- **Ícones:** nenhum sistema de ícones adotado; a marca usa apenas o símbolo Ψ do logo. Não introduzir bibliotecas de ícones sem necessidade.
- **Layout:** grid amplo, muito respiro entre seções (80px+), botão de WhatsApp fixo no canto inferior direito, acima do rodapé (nunca sobre ele).

## Iconografia
Não há sistema de ícones no material fornecido. O único elemento gráfico de marca é o símbolo Ψ vetorizado. Evitar adicionar ícones genéricos (lupa, seta, engrenagem) — preferir texto ou o próprio Chip/Button.

## Marca
Logo mantido exatamente como a cliente entregou — símbolo Ψ desenhado à mão dentro de um círculo + "DANIELLY CURIONE" em serifada clássica + "PSICOLOGIA / DESENVOLVIMENTO HUMANO". Vetorizado a partir do arquivo raster original (traço preservado, não redesenhado). Variantes em `assets/`: símbolo isolado (claro/escuro) e lockup vertical completo (claro/escuro). Fonte do texto do logo identificada por comparação visual: **Libre Baskerville** — usar para qualquer recriação do lockup em HTML/CSS (menus, rodapés, decks).

## Intentional additions
- `Chip`, `ServiceCard`, `QuoteBlock`, `WhatsAppScheduler` não vêm de um kit de componentes pré-existente — foram definidos a partir do briefing (que pedia explicitamente "chips de credencial", "card de serviço", "bloco de citação" e o "formulário do agendador WhatsApp"). `Button` e `Chip` seguem o padrão visual observado nas páginas já aprovadas.

## Caveats
- Sem arquivo de fonte local: `typography.css` importa Newsreader/Nunito Sans via Google Fonts CDN. Se a cliente tiver arquivos de fonte licenciados, substituir por `@font-face` local.
- Fotos de placeholder: apenas duas fotos reais foram recebidas (retrato com marca d'água, foto de consultório). Faltam: placa "818", detalhes do consultório, foto/mapa para Contato.
- Este pacote documenta só a direção 1b (aprovada). As direções 1a/1c/2a exploradas antes da aprovação ficam em `Danielly Curione - Site.dc.html`, fora deste design system.

**Peça concreto:** envie as fotos em alta resolução (retrato sem marca d'água, consultório, placa 818) para eu substituir os assets aqui e refletir automaticamente nas 10 páginas do site.

Lembrete: para outras pessoas da equipe visualizarem este design system, defina o tipo do arquivo como **Design System** no menu Share.
