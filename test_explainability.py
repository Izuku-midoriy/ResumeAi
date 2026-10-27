from app.ml.predictor import SuitabilityPredictor

def test_explainability():
    predictor = SuitabilityPredictor()
    
    # Pass a random vector matching the 13 feature dimension layout
    feature_vector = [0.85, 0.6, 0.9, 0.1, 5.0, 1.0, 1.0, 1.0, 80.0, 2.0, 1.0, 0.8, 0.9]
    
    print("Testing ML prediction and SHAP explanation...")
    prediction = predictor.predict(feature_vector)
    print(f"Prediction: {prediction['prediction']}")
    
    explanation = predictor.explain(feature_vector)
    
    if "error" in explanation:
        print(f"Error: {explanation['error']}")
    else:
        print("\nSHAP Feature Contributions:")
        for k, v in explanation['feature_contributions'].items():
            print(f" - {k}: {v:.4f}")
            
        print("\nInsights:")
        for insight in explanation['insights']:
            print(f" -> {insight}")

if __name__ == "__main__":
    test_explainability()
