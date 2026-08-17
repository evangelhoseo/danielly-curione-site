import React from 'react';

export function ServiceCard({ title, description, linkLabel = 'Saber mais →', highlighted = false }) {
  return (
    <div style={{
      background: highlighted ? 'var(--surface-accent)' : 'var(--surface-panel)',
      borderRadius: 'var(--radius-md)', padding: '28px 26px',
      display: 'flex', flexDirection: 'column', gap: 10,
      justifyContent: highlighted ? 'center' : 'flex-start'
    }}>
      <div style={{ font: 'var(--text-display-md)', color: 'var(--text-heading)', fontStyle: highlighted ? 'italic' : 'normal' }}>{title}</div>
      <p style={{ margin: 0, font: 'var(--text-body-md)', color: 'var(--text-body)' }}>{description}</p>
      {!highlighted && <span style={{ fontFamily: 'var(--font-body)', fontSize: '13px', fontWeight: 700, color: 'var(--brand-secondary)', marginTop: 6 }}>{linkLabel}</span>}
    </div>
  );
}
