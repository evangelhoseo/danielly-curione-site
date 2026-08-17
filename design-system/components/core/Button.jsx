import React from 'react';

export function Button({ variant = 'primary', children, onClick, style }) {
  const base = {
    fontFamily: 'var(--font-body)',
    fontSize: '15px',
    fontWeight: 700,
    border: 'none',
    borderRadius: 'var(--radius-pill)',
    padding: '16px 32px',
    cursor: 'pointer',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    ...style
  };
  const variants = {
    primary: { background: 'var(--brand-primary)', color: 'var(--surface-panel)', boxShadow: 'var(--shadow-cta)' },
    secondary: { background: 'transparent', color: 'var(--brand-secondary)', border: '1px solid var(--brand-secondary)' },
    ghost: { background: 'transparent', color: 'var(--text-heading)', border: '1px solid var(--border-default)' }
  };
  return (
    <button style={{ ...base, ...variants[variant] }} onClick={onClick}>{children}</button>
  );
}
