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
    inferred_skills?: Array<{ name: string; confidence?: number; evidence?: string } | string>;
  };
}

export default function ExtractedData({ data }: ExtractedDataProps) {
  if (!data) return null;

  const inferredSkillsText = data.inferred_skills && data.inferred_skills.length > 0
    ? data.inferred_skills.map(s => typeof s === 'string' ? s : s.name).join(', ')
    : undefined;

  const entries = [
    { label: 'Email', value: data.email },
    { label: 'Phone', value: data.phone },
    { label: 'Education', value: data.education },
    { label: 'Experience', value: data.experience },
    { label: 'Projects', value: data.projects },
    { label: 'Certifications', value: data.certifications },
    { label: 'AI Inferred Skills (Gemini)', value: inferredSkillsText },
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
