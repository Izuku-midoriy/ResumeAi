import React from 'react';
import styles from './components.module.css';

interface ExtractedDataProps {
  data: {
    email?: string;
    phone?: string;
    education?: string;
    experience?: string;
    projects?: string;
    certifications?: string;
  };
}

export default function ExtractedData({ data }: ExtractedDataProps) {
  if (!data) return null;

  const entries = [
    { label: 'Email', value: data.email },
    { label: 'Phone', value: data.phone },
    { label: 'Education', value: data.education },
    { label: 'Experience', value: data.experience },
    { label: 'Projects', value: data.projects },
    { label: 'Certifications', value: data.certifications },
  ].filter(e => e.value);

  if (entries.length === 0) return null;

  return (
    <div className={`glass-panel ${styles.breakdownContainer}`}>
      <h3 className={styles.panelTitle}>Extracted Intelligence</h3>
      <div className={styles.dataGrid}>
        {entries.map((entry, idx) => (
          <div key={idx} className={styles.dataItem}>
            <div className={styles.dataLabel}>{entry.label}</div>
            <div className={styles.dataValue}>{entry.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
