import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class JobMatcher:
    """Matches a resume against a list of jobs using TF-IDF and Cosine Similarity."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def _clean_text(self, text):
        """Basic text normalization."""
        if not text or not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def calculate_tfidf_similarity(self, resume_text, jobs):
        """
        Calculates similarity between resume and a list of jobs.
        
        Returns:
            List of job dictionaries, each augmented with a 'tfidf_similarity' key, 
            sorted descending by score.
        """
        if not jobs:
            return []

        cleaned_resume = self._clean_text(resume_text)
        
        # Build the corpus for jobs
        job_texts = []
        for job in jobs:
            # Combine relevant fields for matching
            description = str(job.get("description", ""))
            skills = str(job.get("required_skills", ""))
            job_texts.append(self._clean_text(f"{description} {skills}"))

        # Corpus is [resume, job1, job2, ...]
        corpus = [cleaned_resume] + job_texts

        try:
            # Compute TF-IDF matrix
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Resume is index 0, jobs are index 1 to N
            resume_vector = tfidf_matrix[0:1]
            job_vectors = tfidf_matrix[1:]

            # Compute cosine similarity
            similarity_scores = cosine_similarity(resume_vector, job_vectors).flatten()

            # Attach scores to jobs and sort
            ranked_jobs = []
            for i, job in enumerate(jobs):
                # Copy job to avoid modifying original dataset objects
                ranked_job = dict(job)
                ranked_job["tfidf_similarity"] = float(similarity_scores[i])
                ranked_jobs.append(ranked_job)

            # Sort by similarity descending
            ranked_jobs.sort(key=lambda x: x["tfidf_similarity"], reverse=True)
            return ranked_jobs

        except Exception as e:
            print(f"Error calculating TF-IDF similarity: {e}")
            # Fallback to zero similarity
            ranked_jobs = []
            for job in jobs:
                ranked_job = dict(job)
                ranked_job["tfidf_similarity"] = 0.0
                ranked_jobs.append(ranked_job)
            return ranked_jobs

    def calculate_semantic_similarity(self, resume_text, jobs):
        """
        Calculates semantic similarity between resume and jobs using sentence-transformers.
        """
        if not jobs:
            return []

        # Import locally to avoid downloading/loading model on startup if unused
        from app.nlp.embeddings import SemanticEmbedder
        
        try:
            embedder = SemanticEmbedder()
            cleaned_resume = self._clean_text(resume_text)
            resume_vector = embedder.get_embedding(cleaned_resume)

            ranked_jobs = []
            for job in jobs:
                description = str(job.get("description", ""))
                skills = str(job.get("required_skills", ""))
                job_text = self._clean_text(f"{description} {skills}")
                
                job_vector = embedder.get_embedding(job_text)
                similarity = embedder.calculate_similarity(resume_vector, job_vector)
                
                ranked_job = dict(job)
                ranked_job["semantic_similarity"] = float(similarity)
                ranked_jobs.append(ranked_job)

            # Sort by semantic similarity descending
            ranked_jobs.sort(key=lambda x: x["semantic_similarity"], reverse=True)
            return ranked_jobs

        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            ranked_jobs = []
            for job in jobs:
                ranked_job = dict(job)
                ranked_job["semantic_similarity"] = 0.0
                ranked_jobs.append(ranked_job)
            return ranked_jobs

    def rank_jobs_with_ml(self, resume_text, resume_info, ats_score, jobs):
        """
        Full pipeline: generates Stage 7 features for all pairs,
        runs the trained ML model, and ranks by the ranking score.
        """
        # First get TF-IDF and Semantic similarities for all jobs
        jobs_with_tfidf = self.calculate_tfidf_similarity(resume_text, jobs)
        jobs_with_semantic = self.calculate_semantic_similarity(resume_text, jobs_with_tfidf)
        
        from app.ml.features import FeatureExtractor
        from app.ml.predictor import SuitabilityPredictor
        
        feature_extractor = FeatureExtractor()
        predictor = SuitabilityPredictor()
            
        ml_ranked_jobs = []
        for job in jobs_with_semantic:
            semantic_sim = job.get("semantic_similarity", 0.0)
            tfidf_sim = job.get("tfidf_similarity", 0.0)
            
            # Use the feature extractor
            feature_vector = feature_extractor.create_feature_vector(
                resume_info,
                job,
                ats_score,
                semantic_sim,
                tfidf_sim
            )
            
            # Run Predictor
            prediction_result = predictor.predict(feature_vector)
            prediction = prediction_result["prediction"]
            probs = prediction_result["probabilities"]
            
            p_good = probs.get("Good Fit", 0.0)
            p_potential = probs.get("Potential Fit", 0.0)
            
            # Calculate ranking score
            ranking_score = p_good + 0.5 * p_potential
            
            # Prepare SHAP explanation using the predictor wrapper
            explanation_data = predictor.explain(feature_vector)
            if "error" in explanation_data:
                explanation = "AI explanation unavailable for this prediction."
            else:
                insights = explanation_data.get("insights", [])
                explanation = insights[0] if insights else "Balanced decision."
            
            job_copy = dict(job)
            job_copy["ml_prediction"] = prediction
            job_copy["ml_probabilities"] = probs
            job_copy["ranking_score"] = ranking_score
            job_copy["explanation"] = explanation
            job_copy["feature_dict"] = {
                "semantic_similarity": semantic_sim,
                "tfidf_similarity": tfidf_sim,
                "skill_match_ratio": feature_vector[2],
                "missing_skill_ratio": feature_vector[3],
                "matched_skill_count": feature_vector[4],
                "missing_skill_count": feature_vector[5],
                "experience_match": feature_vector[6],
                "education_match": feature_vector[7],
                "resume_score": ats_score,
                "project_count": feature_vector[9] if len(feature_vector) > 9 else 0,
                "certification_count": feature_vector[10] if len(feature_vector) > 10 else 0,
                "resume_completeness": feature_vector[11] if len(feature_vector) > 11 else 0,
                "inferred_skill_match": feature_vector[12] if len(feature_vector) > 12 else 0
            }
            ml_ranked_jobs.append(job_copy)
            
        # Sort by ranking score descending
        ml_ranked_jobs.sort(key=lambda x: x["ranking_score"], reverse=True)
        return ml_ranked_jobs
