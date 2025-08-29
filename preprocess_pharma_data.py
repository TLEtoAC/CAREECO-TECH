import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class PharmaDataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        
    def load_data(self, filepath):
        """Load the pharmaceutical dataset"""
        self.df = pd.read_csv(filepath)
        print(f"Dataset loaded: {self.df.shape}")
        return self.df
    
    def basic_info(self):
        """Display basic information about the dataset"""
        print("\n=== DATASET INFO ===")
        print(f"Shape: {self.df.shape}")
        print(f"\nColumns: {list(self.df.columns)}")
        print(f"\nData types:\n{self.df.dtypes}")
        print(f"\nMissing values:\n{self.df.isnull().sum()}")
        print(f"\nUnique values per column:")
        for col in self.df.columns:
            print(f"{col}: {self.df[col].nunique()}")
    
    def clean_text_data(self):
        """Clean text columns"""
        print("\n=== CLEANING TEXT DATA ===")
        
        # Clean medicine names
        if 'medicine_name' in self.df.columns:
            self.df['medicine_name'] = self.df['medicine_name'].fillna('Unknown')
            self.df['medicine_name_clean'] = self.df['medicine_name'].str.lower().str.strip()
        
        # Clean salt composition
        if 'salt_composition' in self.df.columns:
            self.df['salt_composition'] = self.df['salt_composition'].fillna('Not specified')
            self.df['salt_composition_clean'] = self.df['salt_composition'].str.lower().str.strip()
        
        # Clean manufacturer names
        if 'marketed_by' in self.df.columns:
            self.df['marketed_by'] = self.df['marketed_by'].fillna('Unknown')
            self.df['marketed_by_clean'] = self.df['marketed_by'].str.lower().str.strip()
        
        if 'manufactured_by' in self.df.columns:
            self.df['manufactured_by'] = self.df['manufactured_by'].fillna('Unknown')
            self.df['manufactured_by_clean'] = self.df['manufactured_by'].str.lower().str.strip()
        
        print("Text data cleaned successfully")
    
    def extract_features(self):
        """Extract meaningful features from text data"""
        print("\n=== EXTRACTING FEATURES ===")
        
        # Extract dosage information from medicine names
        self.df['dosage_mg'] = self.df['medicine_name'].str.extract(r'(\d+)mg', expand=False).astype(float)
        self.df['dosage_gm'] = self.df['medicine_name'].str.extract(r'(\d+)gm', expand=False).astype(float)
        
        # Extract pack quantity
        self.df['pack_quantity'] = self.df['pack'].str.extract(r'(\d+)', expand=False).astype(float)
        
        # Extract number of active ingredients from salt composition
        self.df['num_ingredients'] = self.df['salt_composition'].str.count(r'\+') + 1
        self.df['num_ingredients'] = self.df['num_ingredients'].fillna(0)
        
        # Create binary features
        self.df['has_injection'] = self.df['packagingType'].str.contains('injection', case=False, na=False).astype(int)
        self.df['has_tablet'] = self.df['packagingType'].str.contains('tablet', case=False, na=False).astype(int)
        self.df['has_capsule'] = self.df['packagingType'].str.contains('capsule', case=False, na=False).astype(int)
        self.df['has_syrup'] = self.df['packagingType'].str.contains('syrup', case=False, na=False).astype(int)
        
        # Extract GST information
        if 'gst' in self.df.columns:
            self.df['gst'] = pd.to_numeric(self.df['gst'], errors='coerce')
            self.df['has_gst'] = (~self.df['gst'].isna()).astype(int)
        
        print("Features extracted successfully")
    
    def handle_missing_values(self):
        """Handle missing values in the dataset"""
        print("\n=== HANDLING MISSING VALUES ===")
        
        # Fill numerical missing values
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if col in ['dosage_mg', 'dosage_gm', 'pack_quantity']:
                self.df[col] = self.df[col].fillna(self.df[col].median())
            elif col == 'gst':
                self.df[col] = self.df[col].fillna(0)
        
        # Fill categorical missing values
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('Unknown')
        
        print("Missing values handled successfully")
    
    def encode_categorical_variables(self):
        """Encode categorical variables"""
        print("\n=== ENCODING CATEGORICAL VARIABLES ===")
        
        categorical_cols = ['packagingType', 'marketed_by_clean', 'manufactured_by_clean']
        
        for col in categorical_cols:
            if col in self.df.columns:
                le = LabelEncoder()
                self.df[f'{col}_encoded'] = le.fit_transform(self.df[col])
                self.label_encoders[col] = le
        
        print("Categorical variables encoded successfully")
    
    def create_text_features(self):
        """Create TF-IDF features from text data"""
        print("\n=== CREATING TEXT FEATURES ===")
        
        # Combine text features
        text_features = []
        if 'medicine_name_clean' in self.df.columns:
            text_features.append(self.df['medicine_name_clean'])
        if 'salt_composition_clean' in self.df.columns:
            text_features.append(self.df['salt_composition_clean'])
        
        if text_features:
            combined_text = pd.concat(text_features, axis=1).fillna('').apply(lambda x: ' '.join(x), axis=1)
            tfidf_features = self.tfidf_vectorizer.fit_transform(combined_text)
            
            # Convert to DataFrame
            tfidf_df = pd.DataFrame(
                tfidf_features.toarray(),
                columns=[f'tfidf_{i}' for i in range(tfidf_features.shape[1])]
            )
            
            # Concatenate with original dataframe
            self.df = pd.concat([self.df.reset_index(drop=True), tfidf_df], axis=1)
        
        print("Text features created successfully")
    
    def scale_numerical_features(self):
        """Scale numerical features"""
        print("\n=== SCALING NUMERICAL FEATURES ===")
        
        numerical_cols = ['dosage_mg', 'dosage_gm', 'pack_quantity', 'num_ingredients', 'gst']
        existing_cols = [col for col in numerical_cols if col in self.df.columns]
        
        if existing_cols:
            self.df[existing_cols] = self.df[existing_cols].fillna(0)
            scaled_features = self.scaler.fit_transform(self.df[existing_cols])
            
            for i, col in enumerate(existing_cols):
                self.df[f'{col}_scaled'] = scaled_features[:, i]
        
        print("Numerical features scaled successfully")
    
    def create_final_features(self):
        """Create final feature matrix for ML"""
        print("\n=== CREATING FINAL FEATURE MATRIX ===")
        
        # Select features for ML model
        feature_cols = []
        
        # Numerical features (scaled)
        numerical_scaled = [col for col in self.df.columns if col.endswith('_scaled')]
        feature_cols.extend(numerical_scaled)
        
        # Binary features
        binary_features = ['has_injection', 'has_tablet', 'has_capsule', 'has_syrup', 'has_gst']
        existing_binary = [col for col in binary_features if col in self.df.columns]
        feature_cols.extend(existing_binary)
        
        # Encoded categorical features
        encoded_features = [col for col in self.df.columns if col.endswith('_encoded')]
        feature_cols.extend(encoded_features)
        
        # TF-IDF features
        tfidf_features = [col for col in self.df.columns if col.startswith('tfidf_')]
        feature_cols.extend(tfidf_features)
        
        # Create final feature matrix
        self.X = self.df[feature_cols].copy()
        
        print(f"Final feature matrix shape: {self.X.shape}")
        print(f"Features included: {len(feature_cols)}")
        
        return self.X
    
    def save_processed_data(self, output_path):
        """Save processed data"""
        print(f"\n=== SAVING PROCESSED DATA ===")
        
        # Save full processed dataset
        self.df.to_csv(output_path.replace('.csv', '_full_processed.csv'), index=False)
        
        # Save feature matrix
        self.X.to_csv(output_path.replace('.csv', '_features.csv'), index=False)
        
        print(f"Processed data saved to: {output_path}")
        print(f"Feature matrix saved to: {output_path.replace('.csv', '_features.csv')}")
    
    def get_preprocessing_summary(self):
        """Get summary of preprocessing steps"""
        summary = {
            'original_shape': self.df.shape,
            'final_features': self.X.shape[1] if hasattr(self, 'X') else 0,
            'missing_values_handled': True,
            'categorical_encoded': len(self.label_encoders),
            'text_features_created': len([col for col in self.df.columns if col.startswith('tfidf_')]),
            'numerical_scaled': len([col for col in self.df.columns if col.endswith('_scaled')])
        }
        return summary

def main():
    # Initialize preprocessor
    preprocessor = PharmaDataPreprocessor()
    
    # Load data
    df = preprocessor.load_data('c:/Users/LENOVO/Desktop/Projects/CAREECO/Stage1_Product_initial_dataset.csv')
    
    # Display basic info
    preprocessor.basic_info()
    
    # Preprocessing steps
    preprocessor.clean_text_data()
    preprocessor.extract_features()
    preprocessor.handle_missing_values()
    preprocessor.encode_categorical_variables()
    preprocessor.create_text_features()
    preprocessor.scale_numerical_features()
    
    # Create final feature matrix
    X = preprocessor.create_final_features()
    
    # Save processed data
    preprocessor.save_processed_data('c:/Users/LENOVO/Desktop/Projects/CAREECO/processed_pharma_data.csv')
    
    # Print summary
    summary = preprocessor.get_preprocessing_summary()
    print("\n=== PREPROCESSING SUMMARY ===")
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print("\n=== PREPROCESSING COMPLETED SUCCESSFULLY ===")
    print("Your data is now ready for ML modeling!")
    
    return preprocessor, X

if __name__ == "__main__":
    preprocessor, X = main()