import joblib
import shap
import numpy as np
from pathlib import Path

class ModelExplainer:
    """Uses SHAP to explain why the ML model made a specific prediction."""
    
    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent.parent
        model_path = project_root / "models" / "suitability_model.pkl"
        
        try:
            self.model = joblib.load(model_path)
            scaler_path = project_root / "models" / "scaler.pkl"
            self.scaler = joblib.load(scaler_path)
            
            # TreeExplainer is highly optimized for Random Forest
            self.explainer = shap.TreeExplainer(self.model)
            self.is_loaded = True
        except Exception as e:
            self.is_loaded = False
            print(f"⚠️ Explainer Initialization Error: {e}")
            
        self.feature_names = [
            "Semantic Match", 
            "Keyword Match", 
            "Skill Match", 
            "Missing Skills", 
            "Experience", 
            "Education", 
            "ATS Score"
        ]

    def explain_prediction(self, feature_vector, is_suitable):
        """
        Calculates SHAP values and returns a human-readable explanation string.
        """
        if not self.is_loaded:
            return "Explanation not available (model missing)."
            
        # The explainer expects a 2D array, properly scaled
        X = np.array(feature_vector).reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        
        try:
            # Calculate SHAP values
            shap_values = self.explainer.shap_values(X_scaled)
            
            # Extract class 1 (Suitable) SHAP values based on SHAP version format
            if isinstance(shap_values, np.ndarray) and len(shap_values.shape) == 3:
                # Format: (n_samples, n_features, n_classes)
                class_1_shap_values = shap_values[0, :, 1]
            elif isinstance(shap_values, list):
                # Format: list of length n_classes, each (n_samples, n_features)
                class_1_shap_values = shap_values[1][0]
            else:
                class_1_shap_values = shap_values[0]
            
            # If the model predicted it IS suitable, find the biggest POSITIVE contributors
            if is_suitable:
                # Get indices of the top 2 highest positive SHAP values
                top_indices = np.argsort(class_1_shap_values)[-2:][::-1]
                top_features = [self.feature_names[i] for i in top_indices if class_1_shap_values[i] > 0]
                
                if top_features:
                    reason = " and ".join(top_features)
                    return f"This job is a strong match primarily due to your **{reason}**."
                else:
                    return "This job is a match based on a holistic review of your profile."
                    
            # If the model predicted it IS NOT suitable, find the biggest NEGATIVE contributors
            else:
                # Get indices of the top 2 lowest negative SHAP values
                bottom_indices = np.argsort(class_1_shap_values)[:2]
                bottom_features = [self.feature_names[i] for i in bottom_indices if class_1_shap_values[i] < 0]
                
                if bottom_features:
                    reason = " and ".join(bottom_features)
                    return f"The model flagged this as not a match primarily due to low **{reason}**."
                else:
                    return "The model flagged this as not a match based on a holistic review of your profile."
                    
        except Exception as e:
            print(f"SHAP explanation error: {e}")
            return "Explanation generation failed."
