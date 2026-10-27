import pandas as pd
from pathlib import Path
import numpy as np

def patch_csv(file_path):
    print(f"Patching {file_path}...")
    df = pd.read_csv(file_path)
    
    # Check if columns exist
    new_cols = ["project_count", "certification_count", "resume_completeness", "inferred_skill_match"]
    for col in new_cols:
        if col not in df.columns:
            # Add synthetic data for the new features so training doesn't crash
            if col == "resume_completeness":
                df[col] = np.random.uniform(0.3, 1.0, size=len(df))
            elif col == "inferred_skill_match":
                df[col] = np.random.uniform(0.0, 0.8, size=len(df))
            else:
                df[col] = np.random.randint(0, 5, size=len(df))
    
    df.to_csv(file_path, index=False)
    print(f"Successfully patched {file_path}")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    data_dir = project_root / "data" / "training"
    
    for split in ["train_features.csv", "val_features.csv", "test_features.csv"]:
        path = data_dir / split
        if path.exists():
            patch_csv(path)
        else:
            print(f"File not found: {path}")
