import pandas as pd
from pathlib import Path

class JobRepository:
    """Repository for loading and managing job descriptions."""

    def __init__(self, data_path=None):
        if data_path is None:
            # Default to the data/jobs/jobs.csv relative to this file
            self.data_path = Path(__file__).resolve().parent.parent.parent / "data" / "jobs" / "jobs.csv"
        else:
            self.data_path = Path(data_path)
            
        self.jobs_df = None

    def load_jobs(self):
        """Load jobs from the CSV file into a pandas DataFrame."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Job dataset not found at {self.data_path}")
            
        try:
            self.jobs_df = pd.read_csv(self.data_path)
            # Basic cleaning: fill NaNs with empty strings
            self.jobs_df = self.jobs_df.fillna("")
            return True
        except Exception as e:
            print(f"Error loading job dataset: {e}")
            return False

    def get_all_jobs(self):
        """Return all jobs as a list of dictionaries."""
        if self.jobs_df is None:
            self.load_jobs()
            
        if self.jobs_df is None or self.jobs_df.empty:
            return []
            
        return self.jobs_df.to_dict(orient="records")

    def get_job_by_id(self, job_id):
        """Retrieve a specific job by its ID."""
        if self.jobs_df is None:
            self.load_jobs()
            
        if self.jobs_df is None or self.jobs_df.empty:
            return None
            
        # Ensure job_id is int if possible, for matching
        try:
            job_id = int(job_id)
        except ValueError:
            pass
            
        job = self.jobs_df[self.jobs_df["job_id"] == job_id]
        if not job.empty:
            return job.iloc[0].to_dict()
            
        return None
