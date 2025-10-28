import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import warnings
import sys
import xgboost as xgb

# print("Python executable:", sys.executable)
# print("XGBoost version:", xgb.__version__)

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
        """Create a target variable (packaging type groups)"""
        packaging_types = self.original_df['packagingType'].fillna('Unknown')

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
            elif any(k in pkg_type for k in ['cream', 'gel', 'ointment', 'lotion']):
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

    def train_random_forest(self):
        """Train Random Forest"""
        print("Training Random Forest...")
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf_model.fit(self.X_train, self.y_train)
        self.models['Random Forest'] = rf_model

    def train_logistic_regression(self):
        """Train Logistic Regression"""
        print("Training Logistic Regression...")
        lr_model = LogisticRegression(random_state=42, max_iter=1000)
        lr_model.fit(self.X_train, self.y_train)
        self.models['Logistic Regression'] = lr_model

    def train_xgboost(self):
        """Train XGBoost with early stopping (using booster directly)"""
        print("Training XGBoost...")

        dtrain = xgb.DMatrix(self.X_train, label=self.y_train)
        dval = xgb.DMatrix(self.X_test, label=self.y_test)

        params = {
            "objective": "multi:softprob",
            "num_class": len(np.unique(self.y_train)),
            "learning_rate": 0.05,
            "max_depth": 6,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "reg_lambda": 1.0,
            "eval_metric": "mlogloss",
            "tree_method": "hist",
            "seed": 42
        }

        evals = [(dtrain, "train"), (dval, "eval")]
        booster = xgb.train(
            params=params,
            dtrain=dtrain,
            num_boost_round=1000,
            evals=evals,
            early_stopping_rounds=50,
            verbose_eval=50
        )

        self.models["XGBoost"] = booster
        print(f"Best iteration: {booster.best_iteration}")



    def evaluate_models(self):
        """Evaluate all trained models"""
        print("\n=== MODEL EVALUATION ===")
        results = {}

        for model_name, model in self.models.items():
            print(f"\n{model_name} Results:")
            print("-" * 30)

            if model_name == "XGBoost":
                # Use booster for predictions
                dtest = xgb.DMatrix(self.X_test)
                y_prob = model.predict(dtest)
                y_pred = np.argmax(y_prob, axis=1)
            else:
                y_pred = model.predict(self.X_test)

            accuracy = accuracy_score(self.y_test, y_pred)
            results[model_name] = accuracy

            print(f"Accuracy: {accuracy:.4f}")
            print("\nClassification Report:")
            print(classification_report(self.y_test, y_pred, target_names=self.target_encoder.classes_))

        best_model = max(results, key=results.get)
        print(f"\n🏆 Best Model: {best_model} (Accuracy: {results[best_model]:.4f})")
        return results


    def feature_importance_xgboost(self):
        """Show feature importance for XGBoost"""
        if "XGBoost" in self.models:
            print("\n=== FEATURE IMPORTANCE (XGBoost) ===")
            booster = self.models["XGBoost"]
            importance = booster.get_score(importance_type="weight")
            importance_df = pd.DataFrame(
                sorted(importance.items(), key=lambda x: x[1], reverse=True),
                columns=["feature", "importance"]
            )
            print(importance_df.head(20))
            return importance_df



def main():
    ml_model = PharmaMLModel()

    # Load data
    ml_model.load_processed_data(
        'processed_pharma_data_features.csv',
        'Stage1_Product_initial_dataset.csv'
    )

    # Create target
    ml_model.create_target_variable()

    # Split data
    ml_model.split_data()

    # Train models
    ml_model.train_random_forest()
    ml_model.train_logistic_regression()
    ml_model.train_xgboost()

    # Evaluate
    ml_model.evaluate_models()

    # Feature importance (XGBoost only)
    ml_model.feature_importance_xgboost()

    print("\n✅ ML modeling completed successfully!")


if __name__ == "__main__":
    main()
