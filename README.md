# Danielly Curione — site institucional

Site institucional de **Danielly Curione**, psicóloga clínica e psicanalista (CRP 05/77951, Niterói-RJ).
Cliente da Agência Foco Digital. Substitui o site antigo em Wix.

- **Endereço de revisão:** https://evangelhoseo.github.io/danielly-curione-site/
- **Domínio próprio (ainda não ligado):** `daniellycurionepsicologia.com` — comprado na Wix, nunca conectado.
- **Direção visual:** 1b "Acolhedora quente", aprovada pela cliente.

## Como funciona

Export **dc-runtime** do Claude Design — mesmo padrão de `vinicolo-site` e `tarja-verde-aventuras-site`.
O corpo é 100% client-side: `support.js` interpreta `<x-dc>` e carrega React/Babel do unpkg em runtime.

**`Site.dc.html` é a fonte única.** As 11 páginas continuam sendo estados de `page` num único
componente, mas cada uma vira um **arquivo HTML de verdade**, com URL e `<head>` próprios, gerado
por `build.py`. Quem decide em que página o componente sobe é o `window.__DC_PAGE__` que o build
injeta em cada arquivo.

```
Site.dc.html    ← FONTE. É o único arquivo que se edita à mão.
build.py        ← gera as 11 páginas + robots.txt + sitemap.xml (+ CNAME)
index.html      ← GERADO (home)
sobre/          ← GERADO ... e assim por diante, uma pasta por rota
support.js      ← runtime dc (não editar)
.nojekyll       ← obrigatório no Pages (ver "Pegadinhas")
assets/         ← fotos reais do consultório + retrato
logo-*.svg      ← logos na raiz (o site referencia daqui)
og-image.png    ← imagem de compartilhamento (WhatsApp, redes)
design-system/  ← documentação da direção 1b: tokens, componentes, guidelines
```

> **Nunca editar os arquivos gerados.** O próximo `build.py` sobrescreve tudo. Edite `Site.dc.html`
> e rode:
> ```bash
> python build.py
> ```

### As rotas

| Página | URL | `page` |
|---|---|---|
| Início | `/` | `home` |
| Sobre | `/sobre/` | `sobre` |
| Psicoterapia para adultos | `/psicoterapia-adultos/` | `adultos` |
| Crianças, adolescentes e idosos | `/criancas-adolescentes-idosos/` | `criancas` |
| Terapia de casal | `/terapia-de-casal/` | `casal` |
| Avaliação psicológica | `/avaliacao-psicologica/` | `avaliacao` |
| Orientação profissional | `/orientacao-profissional/` | `orientacao` |
| Contato | `/contato/` | `contato` |
| Sublocação de sala | `/sublocacao-de-sala/` | `sublocacao` |
| Política de privacidade | `/politica-de-privacidade/` | `lgpd` |
| Blog | `/blog/` | `blog` (fora do sitemap, `noindex` — é placeholder) |

Mudar um slug é mudar em dois lugares: a lista `ROTAS` do `build.py` e o `hrefs()` do
`Site.dc.html`. Se os dois discordarem, o menu aponta para 404.

## Preview local

Registrado no `.claude/launch.json` do projeto `Novos Sites` como **`danielly-curione`** (porta 8097).
Manualmente:

```bash
python -m http.server 8097 --directory .
```

Precisa ser servido por HTTP — abrir o arquivo direto (`file://`) não funciona.

## Publicar alteração

1. Editar `Site.dc.html`
2. `python build.py`
3. Commit dos arquivos gerados junto (o Pages serve o que está no repo — não há Actions aqui)
4. Push na `main` → republica em ~1 min

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

Um export novo sobrescreve o arquivo inteiro. Estas coisas foram feitas à mão e precisam ser
reaplicadas:

1. O `<head>` estático — hoje quem monta o SEO é o `build.py`, mas o export traz um `<head>`
   genérico e é dele que o build reaproveita `lang="pt-BR"`, as fontes e o `<style>`.
2. `criancas`, `casal` e `avaliacao` no mapa `servicePages` + o título da página de LGPD.
3. `grid.pair` nos dois pares de campos e a trava de largura dos campos no `<style>`.
4. `pad.footerBottom` no rodapé.
5. **O andaime das rotas:** `base()` / `hrefs()`, o `go()` que navega de verdade
   (`window.location.assign`), o `page` inicial vindo de `window.__DC_PAGE__`, os itens de menu e
   rodapé como `<a href="{{ hrefs.X }}">` e o rodapé com as duas colunas de navegação.
6. `width`/`height` nas fotos — sem eles a placa da sala 818 (que usa `height:auto`) entra em
   colapso de layout enquanto carrega.

## Ao ligar o domínio próprio

Tudo isso virou configuração no topo do `build.py`. **Primeiro o DNS, depois o build** — na ordem
inversa o site fica fora do ar no intervalo, porque o Pages passa a redirecionar o endereço de
revisão para um domínio que ainda não resolve.

1. No painel de domínios da Wix, apontar `daniellycurionepsicologia.com` para o GitHub Pages:
   quatro registros `A` na raiz (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
   `185.199.111.153`) e um `CNAME` de `www` para `evangelhoseo.github.io`.
2. No `build.py`: `BASE_URL = DOMINIO` e `INDEXAR = True`.
3. `python build.py` — isso já troca canonical/OG/JSON-LD, libera o `robots.txt`, escreve o
   `sitemap.xml` e cria o `CNAME`.
4. Commit + push, conferir o HTTPS no Settings → Pages e mandar o sitemap no Search Console.

## Pendências de conteúdo

- Página **Blog** existe ("Em breve, novos artigos") mas não está em nenhum menu e sai `noindex`,
  fora do sitemap. Quando tiver artigo, entra no menu e sai do `indexar=False`.
- **Instituições de formação:** a cliente pediu para tirar UNESA/PRAXIS/RAC/IPOG dos chips da home
  (feito), mas não falou da tabela "Formação" do Sobre nem do `alumniOf` do JSON-LD, que continuam
  citando as quatro. Confirmar com ela se é para tirar de tudo.
- **O logo do cabeçalho ainda não é um `<a>`** — navega por JS. Funciona, inclusive para o
  rastreador, porque o rodapé linka todas as rotas, mas não abre em nova aba.

## Nunca colocar no site

Regras vindas do briefing e do Código de Ética do CFP (YMYL):

- Depoimentos de pacientes.
- **Mestrado na PUC-Rio — não existe, a própria cliente negou.** Não reintroduzir.
- Avaliações do Google (não há), promessas de resultado terapêutico.
- Foto de banco de imagem ou rosto gerado por IA.
- Clichês visuais de psicologia (cérebro, quebra-cabeça, mãos em concha) e estética de coach.
