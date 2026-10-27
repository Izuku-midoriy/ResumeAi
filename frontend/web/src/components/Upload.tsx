'use client';

import React, { useCallback, useState } from 'react';
import styles from './components.module.css';

interface UploadProps {
  onFileSelect: (file: File) => void;
  isLoading: boolean;
}

export default function Upload({ onFileSelect, isLoading }: UploadProps) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf' || file.name.endsWith('.docx')) {
        onFileSelect(file);
      } else {
        alert('Please upload a valid PDF or DOCX file.');
      }
    }
  }, [onFileSelect]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div 
      className={`${styles.uploadContainer} ${isDragging ? styles.dragActive : ''}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={() => document.getElementById('file-upload')?.click()}
    >
      <input 
        id="file-upload" 
        type="file" 
        accept=".pdf,.docx" 
        onChange={handleChange} 
        style={{ display: 'none' }}
      />
      
      {isLoading ? (
        <div className={styles.uploadText}>
          <span className="text-gradient animate-float" style={{ display: 'inline-block' }}>Processing AI Features...</span>
        </div>
      ) : (
        <>
          <div className={styles.uploadIcon}>
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="12" y1="18" x2="12" y2="12"></line>
              <line x1="9" y1="15" x2="12" y2="12"></line>
              <line x1="15" y1="15" x2="12" y2="12"></line>
            </svg>
          </div>
          <div className={styles.uploadText}>
            Click to upload or drag and drop
          </div>
          <div className={styles.uploadSubtext}>
            PDF or DOCX (Max 10MB)
          </div>
        </>
      )}
    </div>
  );
}
