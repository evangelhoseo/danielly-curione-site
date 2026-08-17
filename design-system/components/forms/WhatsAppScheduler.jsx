import React, { useState } from 'react';

const SERVICOS = ['Psicoterapia individual', 'Terapia de casal', 'Atendimento para criança', 'Atendimento para adolescente', 'Atendimento para idoso', 'Avaliação psicológica', 'Orientação profissional'];

function buildMessage({ nome, servico, modalidade, periodo }) {
  const who = (nome || '').trim() || '[seu nome]';
  const mod = modalidade === 'Online' ? 'online' : 'presencial em Niterói';
  return `Olá, Danielly! Meu nome é ${who}. Gostaria de agendar ${servico.toLowerCase()}, na modalidade ${mod}, preferencialmente no período da ${periodo.toLowerCase()}. Podemos conversar?`;
}

export function WhatsAppScheduler({ phone = '5521971008336' }) {
  const [f, setF] = useState({ nome: '', servico: SERVICOS[0], modalidade: 'Online', periodo: 'Manhã' });
  const set = (k) => (e) => setF((s) => ({ ...s, [k]: e.target.value }));
  const inputStyle = { border: '1px solid var(--border-default)', borderRadius: 'var(--radius-sm)', background: 'var(--surface-page)', padding: '13px 14px', fontSize: 16, color: 'var(--text-heading)', outline: 'none', fontFamily: 'var(--font-body)' };
  const labelStyle = { display: 'flex', flexDirection: 'column', gap: 7, fontSize: 13, fontWeight: 700, color: '#8A6A3E', fontFamily: 'var(--font-body)' };
  return (
    <div style={{ background: 'var(--surface-panel)', borderRadius: 'var(--radius-md)', padding: '32px 30px', display: 'flex', flexDirection: 'column', gap: 18, maxWidth: 420 }}>
      <label style={labelStyle}>Seu nome
        <input style={inputStyle} value={f.nome} onChange={set('nome')} placeholder="Como você gostaria de ser chamada(o)" />
      </label>
      <label style={labelStyle}>O que você procura
        <select style={inputStyle} value={f.servico} onChange={set('servico')}>{SERVICOS.map((s) => <option key={s}>{s}</option>)}</select>
      </label>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <label style={labelStyle}>Modalidade
          <select style={inputStyle} value={f.modalidade} onChange={set('modalidade')}><option>Online</option><option>Presencial em Niterói</option></select>
        </label>
        <label style={labelStyle}>Melhor período
          <select style={inputStyle} value={f.periodo} onChange={set('periodo')}><option>Manhã</option><option>Tarde</option><option>Noite</option></select>
        </label>
      </div>
      <div style={{ background: 'var(--color-chip)', borderRadius: 14, padding: '18px 22px', display: 'flex', flexDirection: 'column', gap: 8 }}>
        <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '.18em', textTransform: 'uppercase', color: '#8A6A3E', fontFamily: 'var(--font-body)' }}>Prévia da mensagem</div>
        <div style={{ fontSize: 14.5, lineHeight: 1.7, color: 'var(--text-heading)', fontFamily: 'var(--font-body)' }}>{buildMessage(f)}</div>
      </div>
      <button
        onClick={() => window.open(`https://wa.me/${phone}?text=${encodeURIComponent(buildMessage(f))}`, '_blank', 'noopener')}
        style={{ background: 'var(--brand-primary)', color: 'var(--surface-panel)', border: 'none', borderRadius: 'var(--radius-pill)', padding: '17px 30px', fontSize: 15, fontWeight: 700, cursor: 'pointer', fontFamily: 'var(--font-body)' }}
      >Abrir WhatsApp com esta mensagem</button>
      <div style={{ fontSize: 12.5, lineHeight: 1.6, color: 'var(--text-muted)', fontFamily: 'var(--font-body)' }}>Nenhum dado é armazenado neste site.</div>
    </div>
  );
}
