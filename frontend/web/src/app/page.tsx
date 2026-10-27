'use client';

import React, { useState } from 'react';
import styles from './page.module.css';
import Upload from '../components/Upload';
import JobCard from '../components/JobCard';
import AtsBreakdown from '../components/AtsBreakdown';
import ExtractedData from '../components/ExtractedData';

interface MatchResponse {
  status: string;
  ats_score: number;
  ats_breakdown: Record<string, number>;
  resume_extracted_data: {
    email?: string;
    phone?: string;
    education?: string;
    experience?: string;
    projects?: string;
    certifications?: string;
    skills?: string[];
  };
  matches: Array<{
    id: string;
    title: string;
    description: string;
    required_skills: string;
    ml_prediction?: string;
    explanation?: string;
    ranking_score?: number;
  }>;
}

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<MatchResponse | null>(null);
  const [topN, setTopN] = useState<number>(3);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // In production, this would be an absolute URL or proxied route
      const response = await fetch(`http://localhost:8000/api/v1/match?top_n=${topN}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Server error: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred while processing the resume.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!results) return;
    try {
      const response = await fetch('http://localhost:8000/api/v1/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_info: results.resume_extracted_data,
          ats_score: results.ats_score,
          ats_breakdown: results.ats_breakdown,
          matches: results.matches
        })
      });
      if (!response.ok) throw new Error("Failed to generate report");
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'ResumeAI_Report.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Error downloading report.");
    }
  };

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <h1 className={`${styles.title} text-gradient`}>ResumeAI</h1>
        <p className={styles.subtitle}>
          Intelligent resume parsing, ATS scoring, and XGBoost-driven job matching with SHAP explainability.
        </p>
      </header>

      <div className={styles.dashboardGrid}>
        <section className={styles.uploadSection}>
          <div className={styles.sliderContainer}>
            <label className={styles.sliderLabel}>
              Number of Job Recommendations: <strong>{topN}</strong>
            </label>
            <input 
              type="range" 
              min="1" 
              max="10" 
              value={topN} 
              onChange={(e) => setTopN(parseInt(e.target.value))}
              className={styles.slider}
            />
          </div>
          
          <Upload onFileSelect={handleFileUpload} isLoading={isLoading} />
          
          {error && <div className={styles.errorState} style={{ marginTop: '1rem' }}>{error}</div>}
          
          {results && (
            <div className={`${styles.statsGrid} animate-fade-in`}>
              <div className={styles.statCard}>
                <div className={styles.statValue}>{Math.round(results.ats_score)}</div>
                <div className={styles.statLabel}>ATS Score</div>
              </div>
              <div className={styles.statCard}>
                <div className={styles.statValue}>{results.resume_extracted_data?.skills?.length || 0}</div>
                <div className={styles.statLabel}>Skills Found</div>
              </div>
            </div>
          )}
          
          {results && (
            <div className="animate-fade-in" style={{ animationDelay: '0.1s' }}>
              <AtsBreakdown breakdown={results.ats_breakdown} />
              <ExtractedData data={results.resume_extracted_data} />
              
              <button className={`btn btn-primary ${styles.downloadBtn}`} onClick={handleDownloadReport}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Download PDF Report
              </button>
            </div>
          )}
        </section>

        <section className={styles.resultsSection}>
          <h2 className={styles.sectionTitle}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
            Job Matches
          </h2>
          
          {isLoading && (
            <div className={styles.emptyState}>
              <div className="animate-float">Analyzing semantics and SHAP contributions...</div>
            </div>
          )}
          
          {!isLoading && !results && !error && (
            <div className={styles.emptyState}>
              Upload a resume to reveal your best job fits.
            </div>
          )}

          {!isLoading && results && results.matches.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
          
        </section>
      </div>
    </main>
  );
}
