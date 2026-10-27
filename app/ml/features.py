class FeatureExtractor:
    """Converts resume information, job information, and matcher scores into numerical ML features."""

    def __init__(self):
        pass

    def calculate_skill_match_ratios(self, resume_skills, job_required_skills):
        """
        Calculates skill match ratio, missing skill ratio, matched skill count, and missing skill count.
        """
        if not job_required_skills:
            return 1.0, 0.0, 0, 0 # If no skills required, it's a perfect match

        if isinstance(job_required_skills, str):
            # Parse CSV skills which are typically separated by semicolons or commas
            separator = ';' if ';' in job_required_skills else ','
            job_skills = [s.strip().lower() for s in job_required_skills.split(separator) if s.strip()]
        else:
            job_skills = [s.strip().lower() for s in job_required_skills if s.strip()]
            
        resume_skills_lower = [s.lower() for s in resume_skills]

        matched = 0
        for skill in job_skills:
            if skill in resume_skills_lower:
                matched += 1
                
        total_required = len(job_skills)
        if total_required == 0:
            return 1.0, 0.0, matched, 0
            
        skill_match_ratio = matched / total_required
        missing_skill_ratio = (total_required - matched) / total_required
        missing_skill_count = total_required - matched
        
        return skill_match_ratio, missing_skill_ratio, matched, missing_skill_count

    def calculate_experience_match(self, resume_experience, job_experience_required):
        """
        Simple binary match for experience. In a real system, this would parse years.
        For now, if the job requires experience and the resume has an experience section, it's a 1.
        """
        if not job_experience_required:
            return 1 # No experience required
            
        if resume_experience and len(resume_experience.strip()) > 10:
            return 1 # Has experience section
            
        return 0

    def calculate_education_match(self, resume_education, job_education_required):
        """
        Simple binary match for education.
        """
        if not job_education_required:
            return 1
            
        if resume_education and len(resume_education.strip()) > 10:
            return 1
            
        return 0

    def calculate_project_count(self, projects_text):
        if not projects_text or len(projects_text.strip()) < 10:
            return 0
        # A simple heuristic: split by newlines or count bullets
        return max(1, len([line for line in projects_text.split('\n') if len(line.strip()) > 5]))

    def calculate_certification_count(self, certs_text):
        if not certs_text or len(certs_text.strip()) < 10:
            return 0
        return max(1, len([line for line in certs_text.split('\n') if len(line.strip()) > 5]))

    def calculate_resume_completeness(self, resume_info):
        score = 0
        expected_keys = ["email", "phone", "skills", "education", "experience", "projects", "certifications"]
        for key in expected_keys:
            val = resume_info.get(key)
            if val and (isinstance(val, list) and len(val) > 0 or isinstance(val, str) and len(val.strip()) > 0):
                score += 1
        return score / len(expected_keys) if expected_keys else 0.0

    def calculate_inferred_skill_match(self, inferred_skills, job_required_skills):
        if not job_required_skills or not inferred_skills:
            return 0.0
        
        # If job_required_skills is string, split it
        if isinstance(job_required_skills, str):
            separator = ';' if ';' in job_required_skills else ','
            job_skills = [s.strip().lower() for s in job_required_skills.split(separator) if s.strip()]
        else:
            job_skills = [s.strip().lower() for s in job_required_skills if s.strip()]

        # inferred_skills is typically a list of dicts from the LLM
        inferred_names = []
        for s in inferred_skills:
            if isinstance(s, dict) and "name" in s:
                inferred_names.append(s["name"].lower())
            elif isinstance(s, str):
                inferred_names.append(s.lower())

        matched = sum(1 for skill in job_skills if skill in inferred_names)
        return matched / len(job_skills) if job_skills else 0.0

    def create_feature_vector(self, resume_info, job_info, ats_score, semantic_similarity, tfidf_similarity):
        """
        Generates the advanced feature vector for ML training/prediction.
        """
        # Calculate derived features
        skill_match_ratio, missing_skill_ratio, matched_skill_count, missing_skill_count = self.calculate_skill_match_ratios(
            resume_info.get("skills", []), 
            job_info.get("required_skills", "")
        )
        
        experience_match = self.calculate_experience_match(
            resume_info.get("experience", ""), 
            job_info.get("experience_required", "")
        )
        
        education_match = self.calculate_education_match(
            resume_info.get("education", ""), 
            job_info.get("education_required", "")
        )
        
        project_count = self.calculate_project_count(resume_info.get("projects", ""))
        certification_count = self.calculate_certification_count(resume_info.get("certifications", ""))
        resume_completeness = self.calculate_resume_completeness(resume_info)
        inferred_skill_match = self.calculate_inferred_skill_match(
            resume_info.get("inferred_skills", []), 
            job_info.get("required_skills", "")
        )

        # Assemble the advanced feature vector
        vector = [
            float(semantic_similarity),
            float(tfidf_similarity),
            float(skill_match_ratio),
            float(missing_skill_ratio),
            float(matched_skill_count),
            float(missing_skill_count),
            float(experience_match),
            float(education_match),
            float(ats_score),
            float(project_count),
            float(certification_count),
            float(resume_completeness),
            float(inferred_skill_match)
        ]
        
        return vector
