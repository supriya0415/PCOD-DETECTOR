import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

FEATURE_NAMES = [
    "Age (yrs)", "Weight (Kg)", "Height(Cm)", "BMI", "Blood Group", "Cycle(R/I)", "Cycle length(days)",
    "Marriage Status (Yrs)", "Pregnant(Y/N)", "No. of aborptions", "Weight gain(Y/N)", "hair growth(Y/N)",
    "Skin darkening (Y/N)", "Hair loss(Y/N)", "Pimples(Y/N)", "Fast food (Y/N)", "Reg.Exercise(Y/N)"
]

def train_model():
    print("Loading data...")
    df = pd.read_csv("PCOD-10.csv")
    
    # Rename columns to match FEATURE_NAMES
    column_mapping = {
        ' Age (yrs)': 'Age (yrs)',
        'Height(Cm) ': 'Height(Cm)',
        'Marraige Status (Yrs)': 'Marriage Status (Yrs)'
    }
    df = df.rename(columns=column_mapping)
    
    # Drop rows without target
    df = df.dropna(subset=['PCOS (Y/N)'])
    
    X = df[FEATURE_NAMES]
    y = df['PCOS (Y/N)']
    
    # Handle missing values using imputer
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train
    print("Training SVM model...")
    svc = SVC(kernel='linear', probability=True, random_state=42)
    svc.fit(X_train_scaled, y_train)
    
    # Eval
    y_pred = svc.predict(X_test_scaled)
    print(f'Testing Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%')
    
    # Save models
    print("Saving models to model/ folder...")
    os.makedirs('model', exist_ok=True)
    joblib.dump(imputer, 'model/imputer.pkl')
    joblib.dump(scaler, 'model/scaler.pkl')
    joblib.dump(svc, 'model/pcos_svm_model.pkl')
    print("Done! Model files successfully generated.")

if __name__ == '__main__':
    train_model()
