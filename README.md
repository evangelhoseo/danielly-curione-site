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
- **Reexportar do Claude Design sobrescreve o `<head>`.** Todo o SEO (title, description, robots,
  canonical, OG, JSON-LD, favicon, `lang="pt-BR"`) foi escrito à mão no `<head>` estático, fora do
  `<helmet>`, porque o `<helmet>` só é aplicado depois do JS carregar. Se vier um export novo,
  reaplicar esse bloco.

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
