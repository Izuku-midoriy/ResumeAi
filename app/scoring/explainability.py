import shap
import numpy as np
import pandas as pd
from typing import Dict, List, Any

class ModelExplainer:
    """Uses SHAP (SHapley Additive exPlanations) to explain ML predictions."""
    
    def __init__(self, model, feature_names: List[str], scaler=None):
        self.model = model
        self.feature_names = feature_names
        self.scaler = scaler
        
        # Initialize SHAP explainer based on model type
        # For tree-based models (RandomForest, XGBoost) we use TreeExplainer
        # For linear models (LogisticRegression) we use LinearExplainer or KernelExplainer
        
        # Checking if it's a linear model vs tree based
        if hasattr(model, 'coef_'):
            # It's a linear model
            self.explainer = shap.LinearExplainer(model, shap.maskers.Independent(np.zeros((1, len(feature_names)))))
            self.is_tree = False
        else:
            # Assume it's a tree model (Random Forest, XGBoost)
            self.explainer = shap.TreeExplainer(model)
            self.is_tree = True

    def explain_prediction(self, feature_vector: List[float]) -> Dict[str, Any]:
        """
        Takes a single feature vector and returns a human-readable explanation of feature contributions.
        """
        # Convert to DataFrame with feature names to match StandardScaler / model training
        X_df = pd.DataFrame([feature_vector], columns=self.feature_names)
        
        # Scale if scaler is provided (e.g., for Logistic Regression)
        if self.scaler:
            X = self.scaler.transform(X_df)
        else:
            X = X_df.values
            
        # Get SHAP values
        shap_values = self.explainer.shap_values(X)
        
        # shap_values structure depends on model and objective (binary vs multiclass)
        # For multiclass, shap_values is a list of arrays (one for each class)
        # For binary/some tree implementations, it's a single array
        
        # Simplify by getting the magnitude of feature importance for this specific prediction
        if isinstance(shap_values, list):
            # Multiclass: sum absolute contributions across all classes to find the most impactful features overall
            abs_shap = np.sum([np.abs(sv[0]) for sv in shap_values], axis=0)
            contributions = {self.feature_names[i]: float(abs_shap[i]) for i in range(len(self.feature_names))}
        else:
            # If shape is 3D (e.g., some multiclass implementations)
            if len(shap_values.shape) == 3:
                abs_shap = np.sum(np.abs(shap_values[0]), axis=1) # Summing across classes
            else:
                abs_shap = np.abs(shap_values[0])
            contributions = {self.feature_names[i]: float(abs_shap[i]) for i in range(len(self.feature_names))}
            
        # Sort features by impact magnitude (highest first)
        sorted_contributions = sorted(contributions.items(), key=lambda item: item[1], reverse=True)
        
        # Generate human readable insights
        top_features = sorted_contributions[:3]
        insights = [f"{feat} significantly influenced the AI's decision (Impact Score: {score:.2f})" 
                    for feat, score in top_features if score > 0.01]
                    
        if not insights:
            insights = ["The model made a balanced decision based on all available features."]
            
        return {
            "feature_contributions": contributions,
            "top_drivers": [feat for feat, score in top_features],
            "insights": insights
        }
