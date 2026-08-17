export interface ButtonProps {
  /** @startingPoint section="Core" subtitle="Pill CTA in three weights" viewport="700x160" */
  variant?: 'primary' | 'secondary' | 'ghost';
  children: React.ReactNode;
  onClick?: () => void;
  style?: React.CSSProperties;
}
