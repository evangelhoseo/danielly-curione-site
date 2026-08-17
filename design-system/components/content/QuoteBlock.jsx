import React from 'react';

export function QuoteBlock({ quote, author }) {
  return (
    <div style={{ background: 'var(--surface-accent)', borderRadius: 'var(--radius-lg)', padding: '56px 60px', maxWidth: 840, textAlign: 'center', display: 'flex', flexDirection: 'column', gap: 18 }}>
      <div style={{ font: 'var(--text-display-quote)', color: 'var(--text-heading)' }}>&ldquo;{quote}&rdquo;</div>
      <div style={{ fontFamily: 'var(--font-body)', fontSize: 12, letterSpacing: '.22em', textTransform: 'uppercase', color: '#8A6A3E' }}>{author}</div>
    </div>
  );
}
