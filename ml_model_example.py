import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class PharmaMLModel:
    def __init__(self):
        self.models = {}
        self.target_encoder = LabelEncoder()
        
    def load_processed_data(self, features_path, original_path):
        """Load preprocessed features and original data"""
        self.X = pd.read_csv(features_path)
        self.original_df = pd.read_csv(original_path)
        print(f"Features loaded: {self.X.shape}")
        print(f"Original data loaded: {self.original_df.shape}")
        
    def create_target_variable(self):
        """Create a target variable for demonstration"""
        # Example: Predict packaging type category
        packaging_types = self.original_df['packagingType'].fillna('Unknown')
        
        # Group similar packaging types
        def categorize_packaging(pkg_type):
            pkg_type = str(pkg_type).lower()
            if 'tablet' in pkg_type:
                return 'tablet'
            elif 'capsule' in pkg_type:
                return 'capsule'
            elif 'injection' in pkg_type:
                return 'injection'
            elif 'syrup' in pkg_type:
                return 'syrup'
            elif 'cream' in pkg_type or 'gel' in pkg_type or 'ointment' in pkg_type:
                return 'topical'
            else:
                return 'other'
        
        self.y = packaging_types.apply(categorize_packaging)
        self.y_encoded = self.target_encoder.fit_transform(self.y)
        
        print(f"Target variable created with {len(self.target_encoder.classes_)} classes:")
        for i, class_name in enumerate(self.target_encoder.classes_):
            count = (self.y == class_name).sum()
            print(f"  {class_name}: {count} samples")
        
        return self.y_encoded
    
    def split_data(self, test_size=0.2, random_state=42):
        """Split data into train and test sets"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y_encoded, test_size=test_size, random_state=random_state, stratify=self.y_encoded
        )
        
        print(f"Training set: {self.X_train.shape}")
        print(f"Test set: {self.X_test.shape}")
        
    def train_models(self):
        """Train multiple ML models"""
        print("\n=== TRAINING MODELS ===")
        
        # Random Forest
        print("Training Random Forest...")
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf_model.fit(self.X_train, self.y_train)
        self.models['Random Forest'] = rf_model
        
        # Logistic Regression
        print("Training Logistic Regression...")
        lr_model = LogisticRegression(random_state=42, max_iter=1000)
        lr_model.fit(self.X_train, self.y_train)
        self.models['Logistic Regression'] = lr_model
        
        print("Models trained successfully!")
        
    def evaluate_models(self):
        """Evaluate all trained models"""
        print("\n=== MODEL EVALUATION ===")
        
        results = {}
        
        for model_name, model in self.models.items():
            print(f"\n{model_name} Results:")
            print("-" * 30)
            
            # Predictions
            y_pred = model.predict(self.X_test)
            
            # Accuracy
            accuracy = accuracy_score(self.y_test, y_pred)
            results[model_name] = accuracy
            
            print(f"Accuracy: {accuracy:.4f}")
            
            # Classification report
            target_names = self.target_encoder.classes_
            print("\nClassification Report:")
            print(classification_report(self.y_test, y_pred, target_names=target_names))
        
        # Best model
        best_model = max(results, key=results.get)
        print(f"\n🏆 Best Model: {best_model} (Accuracy: {results[best_model]:.4f})")
        
        return results
    
    def feature_importance(self):
        """Show feature importance for Random Forest"""
        if 'Random Forest' in self.models:
            print("\n=== FEATURE IMPORTANCE (Random Forest) ===")
            
            rf_model = self.models['Random Forest']
            feature_importance = pd.DataFrame({
                'feature': self.X.columns,
                'importance': rf_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("Top 20 Most Important Features:")
            for i, (_, row) in enumerate(feature_importance.head(20).iterrows(), 1):
                print(f"{i:2d}. {row['feature']}: {row['importance']:.4f}")
            
            return feature_importance
    
    def predict_sample(self, sample_index=0):
        """Make prediction on a sample"""
        if 'Random Forest' in self.models:
            model = self.models['Random Forest']
            
            # Get sample
            sample = self.X_test.iloc[sample_index:sample_index+1]
            true_label = self.y_test[sample_index]
            
            # Predict
            prediction = model.predict(sample)[0]
            probabilities = model.predict_proba(sample)[0]
            
            print(f"\n=== SAMPLE PREDICTION ===")
            print(f"True label: {self.target_encoder.classes_[true_label]}")
            print(f"Predicted label: {self.target_encoder.classes_[prediction]}")
            print(f"Correct: {'✅' if prediction == true_label else '❌'}")
            
            print("\nPrediction probabilities:")
            for i, prob in enumerate(probabilities):
                print(f"  {self.target_encoder.classes_[i]}: {prob:.4f}")

def main():
    # Initialize ML model
    ml_model = PharmaMLModel()
    
    # Load data
    ml_model.load_processed_data(
        'c:/Users/LENOVO/Desktop/Projects/CAREECO/processed_pharma_data_features.csv',
        'c:/Users/LENOVO/Desktop/Projects/CAREECO/Stage1_Product_initial_dataset.csv'
    )
    
    # Create target variable
    ml_model.create_target_variable()
    
    # Split data
    ml_model.split_data()
    
    # Train models
    ml_model.train_models()
    
    # Evaluate models
    results = ml_model.evaluate_models()
    
    # Feature importance
    feature_importance = ml_model.feature_importance()
    
    # Sample prediction
    ml_model.predict_sample()
    
    print("\n✅ ML modeling completed successfully!")
    print("Your preprocessed data is working well with machine learning models!")

if __name__ == "__main__":
    main()