import React from 'react';
import styles from './components.module.css';
import ExplainabilityWidget from './ExplainabilityWidget';

interface JobCardProps {
  job: {
    title: string;
    description: string;
    required_skills: string;
    ml_prediction?: string;
    explanation?: string;
    missing_skills?: string[];
  };
}

export default function JobCard({ job }: JobCardProps) {
  const getScoreClass = (prediction: string | undefined) => {
    if (prediction === 'Good Fit') return '';
    if (prediction === 'Potential Fit') return styles.potential;
    if (prediction === 'No Fit') return styles.poor;
    return '';
  };

  const skills = job.required_skills ? job.required_skills.split(',').map(s => s.trim()) : [];

  return (
    <div className={`glass-panel ${styles.jobCard} animate-fade-in`}>
      <div className={styles.jobHeader}>
        <h3 className={styles.jobTitle}>{job.title}</h3>
        {job.ml_prediction && (
          <span className={`${styles.jobScore} ${getScoreClass(job.ml_prediction)}`}>
            {job.ml_prediction}
          </span>
        )}
      </div>
      
      <p className={styles.jobDescription}>{job.description}</p>
      
      {skills.length > 0 && (
        <div className={styles.tagsContainer}>
          {skills.map((skill, i) => {
            const isMissing = job.missing_skills?.includes(skill);
            return (
              <span key={i} className={`${styles.tag} ${isMissing ? styles.missingTag : ''}`}>
                {skill}
              </span>
            );
          })}
        </div>
      )}
      
      {job.missing_skills && job.missing_skills.length > 0 && (
        <div className={styles.skillGapContainer}>
          <div className={styles.skillGapTitle}>Skill Gaps Detected</div>
          <div className={styles.upskillLinks}>
            {job.missing_skills.map((skill, i) => (
              <a 
                key={i} 
                href={`https://www.coursera.org/search?query=${encodeURIComponent(skill)}`}
                target="_blank" 
                rel="noopener noreferrer"
                className={styles.upskillLink}
              >
                Upskill: {skill} ↗
              </a>
            ))}
          </div>
        </div>
      )}

      <ExplainabilityWidget explanation={job.explanation || ''} />
    </div>
  );
}
