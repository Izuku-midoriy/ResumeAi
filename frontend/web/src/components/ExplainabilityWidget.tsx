import React from 'react';
import styles from './components.module.css';

interface ExplainabilityWidgetProps {
  explanation: string;
}

export default function ExplainabilityWidget({ explanation }: ExplainabilityWidgetProps) {
  if (!explanation) return null;

  return (
    <div className={styles.explainabilityWidget}>
      <div className={styles.explainabilityTitle}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
        AI Decision Insight
      </div>
      <ul className={styles.insightList}>
        <li className={styles.insightItem}>{explanation}</li>
      </ul>
    </div>
  );
}
