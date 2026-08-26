/*!
 * cookie-banner.js — Foco Digital
 * Banner de consentimento de cookies (LGPD) para o site da Danielly Curione.
 * Sem consentimento explícito, nenhum evento de analytics é disparado: este
 * script só empurra `consent_granted` para o dataLayer depois do clique em
 * "Aceitar". O GTM (Google Tag + listener de cliques) só dispara tags a
 * partir desse evento — ver clientes/foco-tagueamento-ga4-status.md.
 */
(function () {
  'use strict';

  var COOKIE_NAME = 'foco_consent';
  var COOKIE_DAYS = 180;

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  function setCookie(name, value, days) {
    var expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = name + '=' + encodeURIComponent(value) +
      '; expires=' + expires.toUTCString() + '; path=/; SameSite=Lax';
  }

  function pushConsentGranted() {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'consent_granted' });
  }

  function buildBanner() {
    var wrap = document.createElement('div');
    wrap.id = 'foco-cookie-banner';
    wrap.setAttribute('role', 'dialog');
    wrap.setAttribute('aria-label', 'Aviso de cookies');
    wrap.style.cssText = [
      'position:fixed', 'left:0', 'right:0', 'bottom:0', 'z-index:9999',
      'display:flex', 'flex-wrap:wrap', 'align-items:center', 'justify-content:center',
      'gap:16px', 'padding:16px 20px',
      'background:#FFFAF2', 'border-top:1px solid #EBDCC6',
      'box-shadow:0 -2px 16px rgba(42,33,27,.08)',
      'font-family:"Nunito Sans",sans-serif', 'font-size:14px', 'line-height:1.5',
      'color:#5C4C3F'
    ].join(';');

    var text = document.createElement('p');
    text.style.cssText = 'margin:0;max-width:640px;flex:1 1 320px;min-width:240px;';
    text.innerHTML = 'Usamos cookies para estatísticas de uso (Google Analytics), ' +
      'mediante seu consentimento. Saiba mais na ' +
      '<a href="/politica-de-privacidade/" style="color:#B96A4B;text-decoration:underline;">Política de Privacidade</a>.';

    var actions = document.createElement('div');
    actions.style.cssText = 'display:flex;gap:10px;flex:0 0 auto;';

    var reject = document.createElement('button');
    reject.type = 'button';
    reject.textContent = 'Rejeitar';
    reject.style.cssText = [
      'padding:10px 18px', 'border-radius:999px', 'border:1px solid #EBDCC6',
      'background:transparent', 'color:#5C4C3F', 'font:inherit', 'cursor:pointer'
    ].join(';');

    var accept = document.createElement('button');
    accept.type = 'button';
    accept.textContent = 'Aceitar';
    accept.style.cssText = [
      'padding:10px 18px', 'border-radius:999px', 'border:none',
      'background:#B96A4B', 'color:#FFFAF2', 'font:inherit', 'font-weight:600', 'cursor:pointer'
    ].join(';');

    reject.addEventListener('click', function () {
      setCookie(COOKIE_NAME, 'denied', COOKIE_DAYS);
      hideBanner();
    });
    accept.addEventListener('click', function () {
      setCookie(COOKIE_NAME, 'granted', COOKIE_DAYS);
      pushConsentGranted();
      hideBanner();
    });

    actions.appendChild(reject);
    actions.appendChild(accept);
    wrap.appendChild(text);
    wrap.appendChild(actions);
    return wrap;
  }

  function hideBanner() {
    var el = document.getElementById('foco-cookie-banner');
    if (el && el.parentNode) el.parentNode.removeChild(el);
  }

  function showBanner() {
    hideBanner();
    document.body.appendChild(buildBanner());
  }

  function init() {
    var consent = getCookie(COOKIE_NAME);
    if (consent === 'granted') {
      pushConsentGranted();
      return;
    }
    if (consent === 'denied') return;
    showBanner();
  }

  window.focoReopenCookieBanner = showBanner;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
