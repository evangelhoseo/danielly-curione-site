# -*- coding: utf-8 -*-
"""
Gera as paginas do site a partir de Site.dc.html (fonte unica).

    python build.py

Cada rota vira um arquivo HTML de verdade, com <head> proprio (title, description,
canonical, OG, JSON-LD). O corpo e identico em todas: e o mesmo componente dc-runtime,
que sobe ja na pagina certa por causa de window.__DC_PAGE__.

NUNCA editar os arquivos gerados a mao — o proximo build sobrescreve. Edite Site.dc.html.
"""
import io, os, re, shutil

RAIZ = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(RAIZ, 'Site.dc.html')

# ---------------------------------------------------------------------------
# Enquanto o DNS nao aponta para o GitHub Pages, o site fica no endereco de revisao
# e FORA do Google. Ao ligar o dominio: trocar BASE_URL e por INDEXAR = True.
# ---------------------------------------------------------------------------
DOMINIO = 'https://daniellycurionepsicologia.com'
BASE_URL = DOMINIO
INDEXAR = True

OG_IMAGE = BASE_URL + '/og-image.png'

# Tagueamento (GTM+GA4, padrao da agencia — ver clientes/foco-tagueamento-ga4-status.md).
# GTM_ID vazio desliga a injecao (fica sem o snippet, util pra rodar build fora do ar).
GTM_ID = 'GTM-5VK6P9XT'

DESC_PADRAO = ('Psicoterapia para adultos, adolescentes, crianças, idosos e casais, avaliação '
               'psicológica e orientação profissional. Atendimento online e presencial em Niterói-RJ. CRP 05/77951.')

# chave do estado `page`, pasta, <title>, meta description, tipo de schema
ROTAS = [
    dict(page='home', pasta='', indexar=True,
         title='Danielly Curione — Psicóloga e Psicanalista em Niterói | CRP 05/77951',
         desc=DESC_PADRAO, schema='psychologist', trilha='Início'),

    dict(page='sobre', pasta='sobre', indexar=True,
         title='Sobre Danielly Curione — Psicóloga e Psicanalista em Niterói',
         desc='Psicóloga clínica e psicanalista em Niterói (CRP 05/77951). Formação, abordagem '
              'clínica e o compromisso com o sigilo profissional previsto no Código de Ética.',
         schema='sobre', trilha='Sobre'),

    dict(page='adultos', pasta='psicoterapia-adultos', indexar=True,
         title='Psicoterapia para Adultos em Niterói e Online | Danielly Curione',
         desc='Ansiedade, luto, relações, trabalho e as perguntas que insistem em voltar. '
              'Psicoterapia semanal com psicóloga e psicanalista em Niterói-RJ, presencial ou online.',
         schema='servico', servico='Psicoterapia para adultos', trilha='Psicoterapia para adultos'),

    dict(page='criancas', pasta='criancas-adolescentes-idosos', indexar=True,
         title='Psicoterapia para Crianças, Adolescentes e Idosos em Niterói',
         desc='Uma escuta adequada a cada fase da vida: o brincar na infância, as perguntas da '
              'adolescência, a memória e as perdas no envelhecer. Niterói-RJ e online.',
         schema='servico', servico='Psicoterapia para crianças, adolescentes e idosos',
         trilha='Crianças, adolescentes e idosos'),

    dict(page='casal', pasta='terapia-de-casal', indexar=True,
         title='Terapia de Casal em Niterói e Online | Danielly Curione',
         desc='Um espaço para que os dois possam falar e ser escutados. Terapia de casal presencial '
              'em Niterói-RJ ou online, para impasses, crises e mudanças na vida a dois.',
         schema='servico', servico='Terapia de casal', trilha='Terapia de casal'),

    dict(page='avaliacao', pasta='avaliacao-psicologica', indexar=True,
         title='Avaliação Psicológica em Niterói | Oito Contextos | CRP 05/77951',
         desc='Avaliação terapêutica, neuropsicológica, infantojuvenil, orientação profissional, '
              'trânsito, arma de fogo, contexto jurídico e cirúrgico. Documentos psicológicos '
              'conforme a legislação do CFP, em Niterói-RJ.',
         schema='servico', servico='Avaliação psicológica', trilha='Avaliação psicológica'),

    dict(page='orientacao', pasta='orientacao-profissional', indexar=True,
         title='Orientação Profissional e de Carreira em Niterói | Danielly Curione',
         desc='Escolha de curso, dúvidas na universidade, transição de carreira e aposentadoria: '
              'um processo psicológico de autoconhecimento para decidir com mais consciência.',
         schema='servico', servico='Orientação profissional', trilha='Orientação profissional'),

    dict(page='contato', pasta='contato', indexar=True,
         title='Contato e Agendamento | Danielly Curione — Psicóloga em Niterói',
         desc='Agende pelo WhatsApp. Consultório na sala 818 do Plaza Corporate Offices, Centro de '
              'Niterói-RJ, e atendimento online para todo o Brasil.',
         schema='contato', trilha='Contato'),

    dict(page='sublocacao', pasta='sublocacao-de-sala', indexar=True,
         title='Sublocação de Sala para Psicólogos em Niterói | Sala 818',
         desc='Sala mobiliada no Plaza Corporate Offices, Centro de Niterói, para psicólogos e '
              'terapeutas. Consulte disponibilidade e valores pelo WhatsApp.',
         schema='pagina', trilha='Sublocação de sala'),

    dict(page='lgpd', pasta='politica-de-privacidade', indexar=True, prioridade='0.3',
         title='Política de Privacidade (LGPD) | Danielly Curione',
         desc='Como os dados são tratados neste site: o formulário de contato monta a mensagem no '
              'navegador e envia pelo WhatsApp, sem armazenar nada.',
         schema='pagina', trilha='Política de privacidade'),

    # Placeholder "Em breve, novos artigos" — fica fora do Google e do sitemap ate ter conteudo.
    dict(page='blog', pasta='blog', indexar=False,
         title='Blog | Danielly Curione — Psicóloga e Psicanalista em Niterói',
         desc='Reflexões sobre saúde mental, psicanálise e os temas que atravessam a clínica.',
         schema='pagina', trilha='Blog'),
]

PSYCHOLOGIST = {
    "@type": "Psychologist",
    "@id": "%(base)s/#consultorio",
    "name": "Danielly Curione — Psicologia e Desenvolvimento Humano",
    "legalName": "Danielly Curione Psicologia e Desenvolvimento Humano LTDA",
    "taxID": "61.487.467/0001-00",
}


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def url_da_rota(rota):
    return BASE_URL + '/' + (rota['pasta'] + '/' if rota['pasta'] else '')


def jsonld(rota):
    """Bloco JSON-LD da rota. A home carrega a ficha completa do consultorio;
    as internas referenciam o mesmo @id e acrescentam trilha/servico."""
    u = url_da_rota(rota)
    if rota['schema'] == 'psychologist':
        return '''{
  "@context": "https://schema.org",
  "@type": "Psychologist",
  "@id": "%(base)s/#consultorio",
  "name": "Danielly Curione — Psicologia e Desenvolvimento Humano",
  "legalName": "Danielly Curione Psicologia e Desenvolvimento Humano LTDA",
  "taxID": "61.487.467/0001-00",
  "description": "Consultório de psicologia clínica e psicanálise em Niterói-RJ. Psicoterapia para adultos, adolescentes, crianças, idosos e casais, avaliação psicológica e orientação profissional, online e presencial.",
  "url": "%(base)s/",
  "image": "%(og)s",
  "logo": "%(base)s/logo-vertical.svg",
  "telephone": "+55-21-97100-8336",
  "email": "daniellycurione@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua 15 de Novembro, 4 — sala 818, Edifício Plaza Corporate Offices",
    "addressLocality": "Niterói",
    "addressRegion": "RJ",
    "addressCountry": "BR"
  },
  "areaServed": [
    { "@type": "City", "name": "Niterói" },
    { "@type": "Country", "name": "Brasil" }
  ],
  "availableLanguage": "pt-BR",
  "sameAs": [
    "https://www.instagram.com/daniellycurionepsicologa/",
    "https://www.linkedin.com/in/danielly-curione-0a92476a/"
  ],
  "founder": {
    "@type": "Person",
    "name": "Danielly Curione",
    "jobTitle": "Psicóloga clínica e psicanalista",
    "identifier": "CRP 05/77951"
  }
}''' % dict(base=BASE_URL, og=OG_IMAGE)

    trilha = '''    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Início", "item": "%(base)s/" },
        { "@type": "ListItem", "position": 2, "name": "%(nome)s", "item": "%(url)s" }
      ]
    }''' % dict(base=BASE_URL, nome=esc(rota['trilha']), url=u)

    blocos = [trilha]
    if rota['schema'] == 'servico':
        blocos.append('''    {
      "@type": "Service",
      "name": "%(servico)s",
      "serviceType": "%(servico)s",
      "url": "%(url)s",
      "description": "%(desc)s",
      "provider": { "@id": "%(base)s/#consultorio" },
      "areaServed": [
        { "@type": "City", "name": "Niterói" },
        { "@type": "Country", "name": "Brasil" }
      ],
      "availableChannel": [
        { "@type": "ServiceChannel", "serviceLocation": { "@id": "%(base)s/#consultorio" } },
        { "@type": "ServiceChannel", "name": "Atendimento online" }
      ]
    }''' % dict(servico=esc(rota['servico']), url=u, desc=esc(rota['desc']), base=BASE_URL))
    else:
        blocos.append('''    {
      "@type": "WebPage",
      "name": "%(title)s",
      "url": "%(url)s",
      "description": "%(desc)s",
      "isPartOf": { "@id": "%(base)s/#consultorio" },
      "inLanguage": "pt-BR"
    }''' % dict(title=esc(rota['title']), url=u, desc=esc(rota['desc']), base=BASE_URL))

    return '{\n  "@context": "https://schema.org",\n  "@graph": [\n%s\n  ]\n}' % ',\n'.join(blocos)


def gtm_head():
    if not GTM_ID:
        return ''
    return ('''<!-- Consent Mode (default: negado ate o aceite no cookie-banner.js) -->
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('consent','default',{
  'ad_storage':'denied',
  'ad_user_data':'denied',
  'ad_personalization':'denied',
  'analytics_storage':'denied'
});
</script>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','%s');</script>
<!-- End Google Tag Manager -->

''' % GTM_ID)


def gtm_noscript():
    if not GTM_ID:
        return ''
    return ('<!-- Google Tag Manager (noscript) -->\n'
            '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
            '<!-- End Google Tag Manager (noscript) -->\n' % GTM_ID)


def head_da_rota(rota, prefixo):
    u = url_da_rota(rota)
    indexavel = INDEXAR and rota['indexar']
    robots = ('<meta name="robots" content="index, follow, max-image-preview:large">' if indexavel
              else '<meta name="robots" content="noindex, nofollow">')
    return '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="author" content="Danielly Curione">
<meta name="theme-color" content="#FBF3E8">

%(robots)s
<link rel="canonical" href="%(url)s">

<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Danielly Curione — Psicologia e Desenvolvimento Humano">
<meta property="og:url" content="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(og)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(og)s">

<link rel="icon" type="image/svg+xml" href="%(p)slogo-simbolo.svg">
<link rel="apple-touch-icon" href="%(p)slogo-simbolo.svg">''' % dict(
        title=esc(rota['title']), desc=esc(rota['desc']), robots=robots,
        url=u, og=OG_IMAGE, p=prefixo)


def main():
    fonte = io.open(FONTE, encoding='utf-8').read()

    cabeca, corpo = fonte.split('</head>', 1)
    # tudo que vem antes de <link rel="preconnect"> e SEO gerado; o resto (fontes, style,
    # JSON-LD antigo, support.js) e reaproveitado sem o bloco de schema.
    resto_cabeca = cabeca[cabeca.index('<link rel="preconnect"'):]
    resto_cabeca = re.sub(r'<script type="application/ld\+json">.*?</script>\s*',
                          '', resto_cabeca, flags=re.S)

    gerados = []
    for rota in ROTAS:
        prefixo = '../' if rota['pasta'] else './'
        # Os caminhos ficam literais no HTML (nada de {{ base }} em src): o preload scanner do
        # navegador le o src cru antes do React montar, e um placeholder ali vira 404 em toda pagina.
        head = head_da_rota(rota, prefixo) + '\n\n' + resto_cabeca.strip().replace('"./', '"' + prefixo)
        corpo_rota = corpo.replace('"./', '"' + prefixo)
        if GTM_ID:
            corpo_rota = corpo_rota.replace('<body>', '<body>\n' + gtm_noscript(), 1)
        boot = ('<script>window.__DC_PAGE__=%r;window.__DC_BASE__=%r;</script>'
                % (str(rota['page']), str(prefixo))).replace("'", '"')
        html = ('<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n'
                + gtm_head()
                + head + '\n\n<script type="application/ld+json">\n' + jsonld(rota) + '\n</script>\n\n'
                + boot + '\n</head>' + corpo_rota)

        destino = os.path.join(RAIZ, rota['pasta'], 'index.html') if rota['pasta'] \
            else os.path.join(RAIZ, 'index.html')
        pasta = os.path.dirname(destino)
        if not os.path.isdir(pasta):
            os.makedirs(pasta)
        io.open(destino, 'w', encoding='utf-8', newline='').write(html)
        gerados.append(os.path.relpath(destino, RAIZ).replace('\\', '/'))

    # ------------------------------------------------------------------ sitemap
    urls = []
    for rota in ROTAS:
        if not (INDEXAR and rota['indexar']):
            continue
        urls.append('  <url>\n    <loc>%s</loc>\n    <priority>%s</priority>\n  </url>'
                    % (url_da_rota(rota), rota.get('prioridade', '1.0' if rota['page'] == 'home' else '0.8')))
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + '\n'.join(urls) + '\n</urlset>\n') if urls else None
    caminho_sitemap = os.path.join(RAIZ, 'sitemap.xml')
    if sitemap:
        io.open(caminho_sitemap, 'w', encoding='utf-8', newline='').write(sitemap)
        gerados.append('sitemap.xml')
    elif os.path.exists(caminho_sitemap):
        os.remove(caminho_sitemap)

    # ------------------------------------------------------------------ robots
    if INDEXAR:
        robots = ('# Site no ar. Sitemap abaixo.\nUser-agent: *\nAllow: /\n\n'
                  'Sitemap: %s/sitemap.xml\n' % BASE_URL)
    else:
        robots = ('# Endereco de revisao: fora do Google de proposito.\n'
                  '# Ao ligar o dominio, por INDEXAR = True no build.py e rodar de novo.\n'
                  'User-agent: *\nDisallow: /\n')
    io.open(os.path.join(RAIZ, 'robots.txt'), 'w', encoding='utf-8', newline='').write(robots)
    gerados.append('robots.txt')

    # ------------------------------------------------------------------ CNAME
    caminho_cname = os.path.join(RAIZ, 'CNAME')
    if INDEXAR and BASE_URL == DOMINIO:
        io.open(caminho_cname, 'w', encoding='utf-8', newline='').write(
            DOMINIO.replace('https://', '') + '\n')
        gerados.append('CNAME')
    elif os.path.exists(caminho_cname):
        os.remove(caminho_cname)

    print('base: %s   indexar: %s' % (BASE_URL, INDEXAR))
    for g in gerados:
        print('  ' + g)


if __name__ == '__main__':
    main()
