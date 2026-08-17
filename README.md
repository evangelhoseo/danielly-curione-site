# Danielly Curione — site institucional

Site institucional de **Danielly Curione**, psicóloga clínica e psicanalista (CRP 05/77951, Niterói-RJ).
Cliente da Agência Foco Digital. Substitui o site antigo em Wix.

- **Endereço de revisão:** https://evangelhoseo.github.io/danielly-curione-site/
- **Domínio próprio (ainda não ligado):** `daniellycurionepsicologia.com` — comprado na Wix, nunca conectado.
- **Direção visual:** 1b "Acolhedora quente", aprovada pela cliente.

## Como funciona (sem build)

Export **dc-runtime** do Claude Design — mesmo padrão de `vinicolo-site` e `tarja-verde-aventuras-site`.
100% client-side: `support.js` interpreta `<x-dc>` e carrega React/Babel do unpkg em runtime.
Não existe etapa de build, npm ou deploy script — o que está no repo é o que o navegador serve.

Diferença dos outros dois: aqui o site inteiro é **um arquivo só**. As 11 páginas (Início, Sobre,
Adultos, Crianças/adolescentes/idosos, Casal, Avaliação, Orientação, Blog, Contato, Sublocação, LGPD)
são estados de `page` no componente, não arquivos separados.

```
index.html      ← é o que o GitHub Pages serve na raiz
Site.dc.html    ← MESMO conteúdo, com o nome .dc.html para reabrir no Claude Design
support.js      ← runtime dc (não editar)
.nojekyll       ← obrigatório no Pages (ver "Pegadinhas")
robots.txt      ← bloqueia indexação enquanto está no endereço de revisão
assets/         ← fotos reais (retrato, consultório) + logos
logo-*.svg      ← logos na raiz (o site referencia daqui)
og-image.png    ← imagem de compartilhamento (WhatsApp, redes)
design-system/  ← documentação da direção 1b: tokens, componentes, guidelines
```

> **`index.html` e `Site.dc.html` precisam ficar idênticos.** Edite `Site.dc.html` e copie:
> ```bash
> cp Site.dc.html index.html
> ```

## Preview local

Registrado no `.claude/launch.json` do projeto `Novos Sites` como **`danielly-curione`** (porta 8097).
Manualmente:

```bash
python -m http.server 8097 --directory .
```

Precisa ser servido por HTTP — abrir o arquivo direto (`file://`) não funciona.

## Publicar alteração

Push na `main` → o GitHub Pages republica em ~1 min. Não há Actions neste repo.

## Pegadinhas

- **`.nojekyll` é obrigatório.** O Pages roda Jekyll por padrão e ignora qualquer pasta que comece
  com `_`. Não há pasta `_` hoje, mas o arquivo fica como proteção — foi exatamente isso que
  quebrou o `vinicolo-site` na primeira publicação.
- **Repo público** porque GitHub Pages gratuito exige isso.
- **`1fr` com `<select>` dentro estoura a tela.** `1fr` é `minmax(auto,1fr)`, e o piso `auto` é a
  largura da opção mais longa do select ("Presencial em Niterói", ~200px). No par
  Modalidade/Melhor período isso dava colunas de `202px 99px` em vez de 50/50: no mobile o rótulo
  "Melhor período" era cortado e a página de Contato ganhava rolagem horizontal. Corrigido com
  `grid.pair` (empilha no mobile, `minmax(0,1fr)` no desktop) + trava
  `input,select,textarea{max-width:100%;min-width:0;box-sizing:border-box}` no `<style>`.
  **Se criar outro par de campos lado a lado, use `{{ grid.pair }}`, nunca `1fr 1fr`.**
- **O botão flutuante do WhatsApp é `fixed`** e cobria a linha do CVV no fim do rodapé — a linha mais
  sensível do site. O rodapé tem `padding-bottom` extra (`pad.footerBottom`) só por causa disso.
  Não reduzir.

### Reexportar do Claude Design apaga estas correções

Um export novo sobrescreve o arquivo inteiro. Estas quatro coisas foram feitas à mão e precisam ser
reaplicadas:

1. Todo o `<head>` estático de SEO (title, description, robots, canonical, OG, JSON-LD, favicon,
   `lang="pt-BR"`) — fora do `<helmet>`, que só roda depois do JS carregar.
2. `criancas`, `casal` e `avaliacao` no mapa `servicePages` + o título da página de LGPD.
3. `grid.pair` nos dois pares de campos e a trava de largura dos campos no `<style>`.
4. `pad.footerBottom` no rodapé.

## Ao ligar o domínio próprio

1. Apagar `<meta name="robots" content="noindex, nofollow">` do `Site.dc.html` **e** do `index.html`.
2. Apagar o `Disallow: /` do `robots.txt`.
3. Trocar as URLs de `canonical`, `og:url`, `og:image`, `twitter:image` e do JSON-LD para o domínio.
4. Criar o arquivo `CNAME` na raiz com o domínio e apontar o DNS para o GitHub Pages.

## Pendências de conteúdo

- Fotos que ainda faltam: placa da sala 818, mais ângulos do consultório, foto/mapa para a
  página de Contato. Hoje o site usa a mesma foto de consultório em três lugares.
- Página **Blog** existe ("Em breve, novos artigos") mas não está em nenhum menu — sem link.
- **Limitação de SEO por ser SPA de uma URL:** as 11 páginas compartilham o mesmo endereço, título e
  description, então o Google só consegue indexar uma. Para busca local (o que interessa a ela),
  isso precisa virar URLs de verdade por página antes de considerar o site "no ar pra valer".

## Nunca colocar no site

Regras vindas do briefing e do Código de Ética do CFP (YMYL):

- Depoimentos de pacientes.
- **Mestrado na PUC-Rio — não existe, a própria cliente negou.** Não reintroduzir.
- Avaliações do Google (não há), promessas de resultado terapêutico.
- Foto de banco de imagem ou rosto gerado por IA.
- Clichês visuais de psicologia (cérebro, quebra-cabeça, mãos em concha) e estética de coach.
