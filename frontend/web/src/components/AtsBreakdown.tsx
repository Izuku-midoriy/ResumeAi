import React from 'react';
import styles from './components.module.css';

interface AtsBreakdownProps {
  breakdown: Record<string, number>;
}

export default function AtsBreakdown({ breakdown }: AtsBreakdownProps) {
  if (!breakdown || Object.keys(breakdown).length === 0) return null;

  const maxPoints: Record<string, number> = {
    "Contact Information": 10,
    "Skills": 25,
    "Education": 15,
    "Experience": 20,
    "Projects": 15,
    "Certifications": 10,
    "Resume Content": 5
  };

  return (
    <div className={`glass-panel ${styles.breakdownContainer}`}>
      <h3 className={styles.panelTitle}>ATS Diagnostics</h3>
      <ul className={styles.breakdownList}>
        {Object.entries(breakdown).map(([category, score], idx) => {
          const max = maxPoints[category] || 10;
          const isPassed = score > 0;
          return (
            <li key={idx} className={styles.breakdownItem}>
              <span className={isPassed ? styles.checkIcon : styles.crossIcon}>
                {isPassed ? '✓' : '✗'}
              </span>
              <span className={styles.breakdownText}>
                <strong>{category}:</strong> {score} / {max} pts
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
