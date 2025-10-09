from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(__name__)
CORS(app)

class PharmaAPI:
    def __init__(self):
        self.df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.load_data()
        
    def load_data(self):
        """Load the pharmaceutical dataset"""
        try:
            # Try multiple possible paths for the dataset
            possible_paths = [
                '../Stage1_Product_initial_dataset.csv',  # Original path
                'Stage1_Product_initial_dataset.csv',     # Same directory
                './Stage1_Product_initial_dataset.csv',   # Current directory
                os.path.join('..', 'Stage1_Product_initial_dataset.csv'),  # Using os.path
            ]
            
            self.df = None
            for path in possible_paths:
                try:
                    if os.path.exists(path):
                        self.df = pd.read_csv(path)
                        print(f"✅ Successfully loaded {len(self.df)} medicines from: {path}")
                        break
                except Exception as path_error:
                    print(f"❌ Failed to load from {path}: {path_error}")
                    continue
            
            if self.df is None:
                raise FileNotFoundError("Dataset file not found in any expected location")
            
            # Prepare text data for similarity search
            self.prepare_search_data()
            
        except Exception as e:
            print(f"⚠️  Error loading data: {e}")
            print("📝 Creating sample data for demonstration...")
            # Create sample data if file not found
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data for demonstration"""
        sample_data = [
            {
                'medicine_name': 'Paracetamol 500mg Tablet 10 tablets',
                'salt_composition': 'Paracetamol (500mg)',
                'packagingType': 'strip or blister pack',
                'pack': '10 tablets',
                'marketed_by': 'Generic Pharma Ltd',
                'gst': '12',
                'manufactured_by': 'Generic Pharma Ltd'
            },
            {
                'medicine_name': 'Aceper Tablet 10 tablets',
                'salt_composition': 'Paracetamol (500mg) + Phenylpropanolamine (25mg) + Cetirizine (10mg)',
                'packagingType': 'strip or blister pack',
                'pack': '10 tablets',
                'marketed_by': '3A Pharmaceuticals',
                'gst': '12',
                'manufactured_by': '3A Pharmaceuticals'
            },
            {
                'medicine_name': 'Crocin 650mg Tablet 15 tablets',
                'salt_composition': 'Paracetamol (650mg)',
                'packagingType': 'strip or blister pack',
                'pack': '15 tablets',
                'marketed_by': 'GSK Pharmaceuticals',
                'gst': '12',
                'manufactured_by': 'GSK Pharmaceuticals'
            }
        ]
        
        self.df = pd.DataFrame(sample_data)
        self.prepare_search_data()
    
    def prepare_search_data(self):
        """Prepare data for text-based similarity search"""
        # Combine relevant text fields for search
        self.df['search_text'] = (
            self.df['medicine_name'].fillna('') + ' ' +
            self.df['salt_composition'].fillna('') + ' ' +
            self.df['marketed_by'].fillna('')
        ).str.lower()
        
        # Create TF-IDF matrix
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['search_text'])
        print("TF-IDF matrix created for similarity search")
    
    def search_medicines(self, query, filters=None):
        """Search medicines based on query and filters"""
        if not query.strip():
            return []
        
        # Convert query to TF-IDF vector
        query_vector = self.tfidf_vectorizer.transform([query.lower()])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top matches
        top_indices = similarity_scores.argsort()[-20:][::-1]
        
        results = []
        for idx in top_indices:
            if similarity_scores[idx] > 0.1:  # Minimum similarity threshold
                medicine = self.df.iloc[idx].to_dict()
                medicine['id'] = int(idx)
                medicine['confidence'] = int(similarity_scores[idx] * 100)
                
                # Extract additional features
                medicine['dosage'] = self.extract_dosage(medicine['medicine_name'])
                medicine['ingredients_count'] = self.count_ingredients(medicine['salt_composition'])
                
                # Clean up NaN values for JSON serialization
                for key, value in medicine.items():
                    if pd.isna(value):
                        medicine[key] = None
                    elif isinstance(value, (np.integer, np.floating)):
                        medicine[key] = value.item()
                
                results.append(medicine)
        
        # Apply filters
        if filters:
            results = self.apply_filters(results, filters)
        
        # Sort results
        results = self.sort_results(results, filters.get('sortBy', 'relevance') if filters else 'relevance')
        
        return results[:10]  # Return top 10 results
    
    def extract_dosage(self, medicine_name):
        """Extract dosage from medicine name"""
        if pd.isna(medicine_name):
            return None
        
        # Look for patterns like 500mg, 10mg, etc.
        dosage_match = re.search(r'(\d+)mg', str(medicine_name))
        if dosage_match:
            return f"{dosage_match.group(1)}mg"
        return None
    
    def count_ingredients(self, composition):
        """Count number of active ingredients"""
        if pd.isna(composition) or composition == 'Not specified':
            return 1
        
        # Count '+' symbols and add 1
        return str(composition).count('+') + 1
    
    def apply_filters(self, results, filters):
        """Apply filters to search results"""
        filtered_results = results
        
        if filters.get('packagingType'):
            filtered_results = [r for r in filtered_results if r.get('packagingType') == filters['packagingType']]
        
        if filters.get('manufacturer'):
            filtered_results = [r for r in filtered_results if r.get('marketed_by') == filters['manufacturer']]
        
        return filtered_results
    
    def sort_results(self, results, sort_by):
        """Sort results based on criteria"""
        if sort_by == 'name':
            return sorted(results, key=lambda x: x.get('medicine_name', ''))
        elif sort_by == 'manufacturer':
            return sorted(results, key=lambda x: x.get('marketed_by', ''))
        elif sort_by == 'packaging':
            return sorted(results, key=lambda x: x.get('packagingType', ''))
        else:  # relevance (default)
            return sorted(results, key=lambda x: x.get('confidence', 0), reverse=True)
    
    def get_recommendations(self, medicine_id):
        """Get similar medicines based on composition"""
        if medicine_id >= len(self.df):
            return []
        
        # Get the medicine
        medicine = self.df.iloc[medicine_id]
        
        # Find similar medicines based on composition
        medicine_vector = self.tfidf_matrix[medicine_id]
        similarity_scores = cosine_similarity(medicine_vector, self.tfidf_matrix).flatten()
        
        # Get top similar medicines (excluding the medicine itself)
        similar_indices = similarity_scores.argsort()[-6:][::-1][1:]  # Top 5 excluding self
        
        recommendations = []
        for idx in similar_indices:
            if similarity_scores[idx] > 0.2:  # Higher threshold for recommendations
                rec_medicine = self.df.iloc[idx].to_dict()
                rec_medicine['id'] = int(idx)
                rec_medicine['similarity'] = int(similarity_scores[idx] * 100)
                recommendations.append(rec_medicine)
        
        return recommendations

# Initialize the API
pharma_api = PharmaAPI()

@app.route('/api/search', methods=['POST'])
def search_medicines():
    """Search medicines endpoint"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        filters = data.get('filters', {})
        
        results = pharma_api.search_medicines(query, filters)
        
        return jsonify({
            'success': True,
            'medicines': results,
            'count': len(results)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recommendations/<int:medicine_id>', methods=['GET'])
def get_recommendations(medicine_id):
    """Get medicine recommendations endpoint"""
    try:
        recommendations = pharma_api.get_recommendations(medicine_id)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data endpoint"""
    try:
        df = pharma_api.df
        
        analytics = {
            'totalMedicines': len(df),
            'uniqueManufacturers': df['marketed_by'].nunique(),
            'packagingTypes': df['packagingType'].nunique(),
            'topManufacturers': df['marketed_by'].value_counts().head(10).to_dict(),
            'packagingDistribution': df['packagingType'].value_counts().head(10).to_dict()
        }
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'PharmaCatalogue API is running',
        'medicines_loaded': len(pharma_api.df) if pharma_api.df is not None else 0
    })

if __name__ == '__main__':
    print("Starting PharmaCatalogue API...")
    print(f"Loaded {len(pharma_api.df)} medicines")
    app.run(debug=True, host='0.0.0.0', port=5000)