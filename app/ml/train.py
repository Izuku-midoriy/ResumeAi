import pandas as pd
import numpy as np
import joblib
import json
import os
from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from xgboost import XGBClassifier

def train_ablation_models():
    """
    Trains ML models with different feature configurations (Ablation Study)
    and evaluates them to pick the best model for Stage 8.
    """
    print("Starting ML Model Training Pipeline (Stage 8)...")
    
    project_root = Path(__file__).resolve().parent.parent.parent
    data_dir = project_root / "data" / "training"
    
    train_path = data_dir / "train_features.csv"
    val_path = data_dir / "val_features.csv"
    test_path = data_dir / "test_features.csv"
    
    if not train_path.exists():
        print(f"Error: Dataset splits not found. Please run data/training/prepare_real_training_data.py first.")
        return
        
    df_train = pd.read_csv(train_path)
    df_val = pd.read_csv(val_path)
    df_test = pd.read_csv(test_path)
    
    print(f"Loaded dataset. Train: {len(df_train)}, Val: {len(df_val)}, Test: {len(df_test)}")
    
    # Label Encoding
    le = LabelEncoder()
    y_train = le.fit_transform(df_train["label"])
    y_val = le.transform(df_val["label"])
    y_test = le.transform(df_test["label"])
    
    classes = list(le.classes_)
    print(f"Classes: {classes}")
    
    # Define Feature Sets for Ablation Study
    feature_sets = {
        "Text Only": ["tfidf_similarity", "semantic_similarity"],
        "Text + Skills": [
            "tfidf_similarity", "semantic_similarity", 
            "skill_match_ratio", "missing_skill_ratio", 
            "matched_skill_count", "missing_skill_count"
        ],
        "Full Features": [
            "tfidf_similarity", "semantic_similarity", 
            "skill_match_ratio", "missing_skill_ratio", 
            "matched_skill_count", "missing_skill_count",
            "experience_match", "education_match", "resume_score",
            "project_count", "certification_count", "resume_completeness", "inferred_skill_match"
        ]
    }
    
    results = []
    best_macro_f1 = -1
    best_model_info = {}
    best_model_obj = None
    best_scaler_obj = None
    
    for fs_name, features in feature_sets.items():
        print(f"\n--- Experiment: {fs_name} ---")
        
        X_train = df_train[features]
        X_val = df_val[features]
        X_test = df_test[features]
        
        # Scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        X_test_scaled = scaler.transform(X_test)
        
        # Models
        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
            "Random Forest": RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42),
            "XGBoost": XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='mlogloss')
        }
        
        for model_name, model in models.items():
            # Use scaled data for LR, unscaled for RF (though scaled is fine for RF too, we use scaled for consistency here)
            if model_name == "Logistic Regression":
                model.fit(X_train_scaled, y_train)
                preds = model.predict(X_val_scaled)
            else:
                model.fit(X_train, y_train)
                preds = model.predict(X_val)
            
            # Validation Metrics
            acc = accuracy_score(y_val, preds)
            macro_f1 = f1_score(y_val, preds, average='macro')
            weighted_f1 = f1_score(y_val, preds, average='weighted')
            
            print(f"{model_name:20s} | Acc: {acc:.4f} | Macro F1: {macro_f1:.4f} | Weighted F1: {weighted_f1:.4f}")
            
            result_dict = {
                "Feature Set": fs_name,
                "Model": model_name,
                "Validation Accuracy": float(acc),
                "Validation Macro F1": float(macro_f1),
                "Validation Weighted F1": float(weighted_f1)
            }
            results.append(result_dict)
            
            if macro_f1 > best_macro_f1:
                best_macro_f1 = macro_f1
                best_model_info = result_dict
                best_model_obj = model
                best_scaler_obj = scaler if model_name == "Logistic Regression" else None
                
    print("\nBest Model Selected (on Validation Set):")
    print(f"{best_model_info['Model']} with {best_model_info['Feature Set']} features (Macro F1: {best_model_info['Validation Macro F1']:.4f})")
    
    # Evaluate Best Model on Test Set
    print("\nEvaluating Best Model on Test Set...")
    best_features = feature_sets[best_model_info['Feature Set']]
    X_test_final = df_test[best_features]
    
    if best_model_info['Model'] == "Logistic Regression":
        X_test_final = best_scaler_obj.transform(X_test_final)
        
    test_preds = best_model_obj.predict(X_test_final)
    
    test_acc = accuracy_score(y_test, test_preds)
    test_macro_f1 = f1_score(y_test, test_preds, average='macro')
    test_weighted_f1 = f1_score(y_test, test_preds, average='weighted')
    
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test Macro F1: {test_macro_f1:.4f}")
    print(f"Test Weighted F1: {test_weighted_f1:.4f}")
    print("\nClassification Report (Test):")
    print(classification_report(y_test, test_preds, target_names=classes))
    
    # Save Results and Models
    models_dir = project_root / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Save evaluation results
    eval_file = models_dir / "evaluation_results.json"
    with open(eval_file, "w") as f:
        json.dump({
            "ablation_results": results,
            "best_model_selection": best_model_info,
            "test_metrics": {
                "accuracy": test_acc,
                "macro_f1": test_macro_f1,
                "weighted_f1": test_weighted_f1
            }
        }, f, indent=4)
        
    # Save the actual best model to the standard paths used by predictor
    joblib.dump(best_model_obj, models_dir / "suitability_model.pkl")
    if best_scaler_obj:
        joblib.dump(best_scaler_obj, models_dir / "scaler.pkl")
    else:
        # Save a dummy scaler if RF was chosen to prevent predictor errors, or just save standard scaler
        # We'll save the standard scaler fitted on the best features anyway just in case
        scaler = StandardScaler()
        scaler.fit(df_train[best_features])
        joblib.dump(scaler, models_dir / "scaler.pkl")
        
    joblib.dump(le, models_dir / "label_encoder.pkl")
    
    # Save a metadata file so the predictor knows which features to use
    with open(models_dir / "model_meta.json", "w") as f:
        json.dump({
            "best_model_name": best_model_info["Model"],
            "best_feature_set_name": best_model_info["Feature Set"],
            "features": best_features,
            "classes": classes
        }, f, indent=4)
        
    print(f"\nSaved model, scaler, label encoder, and evaluation results to {models_dir}")
    print("Training Pipeline Complete!")

if __name__ == "__main__":
    train_ablation_models()
