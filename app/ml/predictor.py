import joblib
import numpy as np
import pandas as pd
import json
from pathlib import Path

class SuitabilityPredictor:
    """Loads the trained ML model and uses it to predict job suitability."""
    
    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent.parent
        model_path = project_root / "models" / "suitability_model.pkl"
        scaler_path = project_root / "models" / "scaler.pkl"
        encoder_path = project_root / "models" / "label_encoder.pkl"
        meta_path = project_root / "models" / "model_meta.json"
        
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.encoder = joblib.load(encoder_path)
            
            with open(meta_path, "r") as f:
                self.meta = json.load(f)
                
            self.is_loaded = True
        except FileNotFoundError:
            self.is_loaded = False
            print("⚠️ Warning: Trained model not found. Run app/ml/train.py first.")

    def predict(self, feature_vector):
        """
        Takes a 9-dimensional feature vector (or whatever best feature set is), scales it, and predicts suitability.
        Returns:
            dict containing prediction and probabilities for all classes.
        """
        if not self.is_loaded:
            # Fallback if model hasn't been trained yet
            return {
                "prediction": "Unknown",
                "probabilities": {"Good Fit": 0.0, "Potential Fit": 0.0, "No Fit": 0.0}
            }
            
        # We assume the feature_vector comes in as the full 9 features.
        # But if the best model uses fewer features, we should slice it.
        # Wait, the matcher generates all 9 features anyway. To be safe, we just pass the full vector
        # unless we explicitly mapped features. For now, assuming the best model used Full Features,
        # or we just pass the features it needs. The instruction states "The predictor must support THREE classes."
        # If it used fewer features, this would break if we pass 9. Let's assume Full Features or just pass all 9 to scaler.
        # Actually, let's filter the features if needed based on metadata.
        # The feature_vector passed from matcher is [semantic_sim, tfidf_sim, skill_match_ratio, missing_skill_ratio, matched_count, missing_count, exp_match, edu_match, ats_score]
        
        # We need to map the incoming list to a dict to pick the right features if we want to be robust,
        # but to keep it simple, we just pass the raw feature vector and assume full features were used
        # OR we rely on the caller to pass exactly what's needed. Let's stick to Full Features order.
        
        # We'll just run it through the model. 
        # If the model used fewer features, X will have too many columns. 
        # Let's map it:
        feature_names = [
            "semantic_similarity", "tfidf_similarity", "skill_match_ratio", "missing_skill_ratio", 
            "matched_skill_count", "missing_skill_count", "experience_match", "education_match", "resume_score",
            "project_count", "certification_count", "resume_completeness", "inferred_skill_match"
        ]
        
        feature_dict = dict(zip(feature_names, feature_vector))
        best_features = self.meta.get("features", feature_names)
        
        X_df = pd.DataFrame([{f: feature_dict[f] for f in best_features}])
        
        if self.meta.get("best_model_name") == "Logistic Regression":
            X = self.scaler.transform(X_df)
        else:
            X = X_df
            
        probs = self.model.predict_proba(X)[0]
        pred_idx = self.model.predict(X)[0]
        
        pred_class = self.encoder.inverse_transform([pred_idx])[0]
        classes = self.encoder.classes_
        
        prob_dict = {classes[i]: float(probs[i]) for i in range(len(classes))}
        
        return {
            "prediction": pred_class,
            "probabilities": prob_dict,
            "model_used": self.meta.get("best_model_name", "Unknown")
        }

    def explain(self, feature_vector):
        """
        Generates a SHAP explanation for the prediction.
        """
        if not self.is_loaded:
            return {"error": "Model not loaded"}
            
        try:
            from app.scoring.explainability import ModelExplainer
            
            feature_names = [
                "semantic_similarity", "tfidf_similarity", "skill_match_ratio", "missing_skill_ratio", 
                "matched_skill_count", "missing_skill_count", "experience_match", "education_match", "resume_score",
                "project_count", "certification_count", "resume_completeness", "inferred_skill_match"
            ]
            
            # Identify which features are actually used by the model
            best_features = self.meta.get("features", feature_names)
            
            # Select the correct indices from the vector
            feature_dict = dict(zip(feature_names, feature_vector))
            X_selected = [feature_dict[f] for f in best_features]
            
            explainer = ModelExplainer(self.model, best_features, self.scaler if self.meta.get("best_model_name") == "Logistic Regression" else None)
            return explainer.explain_prediction(X_selected)
        except Exception as e:
            return {"error": f"Failed to generate explanation: {e}"}
