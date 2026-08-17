import React from 'react';

export function Chip({ children }) {
  return (
    <span style={{
      background: 'var(--color-chip)', color: 'var(--text-heading)',
      padding: '9px 16px', borderRadius: 'var(--radius-pill)',
      fontFamily: 'var(--font-body)', fontSize: '13px', display: 'inline-block'
    }}>{children}</span>
  );
}
