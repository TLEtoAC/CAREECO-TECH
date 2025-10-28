from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
import re

# Try to import enhanced search, fallback to simple version
try:
    from enhanced_search import EnhancedPharmaSearch
    print("✅ Using full enhanced search with NLTK")
except Exception as e:
    print(f"⚠️ NLTK enhanced search failed: {e}")
    print("📝 Using simple enhanced search without NLTK")
    from simple_enhanced_search import SimpleEnhancedPharmaSearch as EnhancedPharmaSearch

app = Flask(__name__)
CORS(app)

class PharmaAPI:
    def __init__(self):
        self.enhanced_search = EnhancedPharmaSearch()
        self.load_data()
        
    def load_data(self):
        """Load the pharmaceutical dataset using enhanced search"""
        try:
            # Try multiple possible paths for the dataset
            possible_paths = [
                '../Stage1_Product_initial_dataset.csv',  # Original path
                'Stage1_Product_initial_dataset.csv',     # Same directory
                './Stage1_Product_initial_dataset.csv',   # Current directory
                os.path.join('..', 'Stage1_Product_initial_dataset.csv'),  # Using os.path
            ]
            
            loaded = False
            # Skip duplicates for faster startup during development
            skip_duplicates = os.getenv('SKIP_DUPLICATES', 'false').lower() == 'true'
            
            for path in possible_paths:
                try:
                    if os.path.exists(path):
                        loaded = self.enhanced_search.load_data(path, skip_duplicates=skip_duplicates)
                        if loaded:
                            print(f"✅ Successfully loaded enhanced search from: {path}")
                            break
                except Exception as path_error:
                    print(f"❌ Failed to load from {path}: {path_error}")
                    continue
            
            if not loaded:
                raise FileNotFoundError("Dataset file not found in any expected location")
            
        except Exception as e:
            print(f"⚠️  Error loading data: {e}")
            print("📝 Enhanced search initialization failed")
    

    
    def search_medicines(self, query, filters=None):
        """Search medicines using enhanced search with NLP and symptom support"""
        if not query.strip():
            return []
        
        try:
            # Use enhanced search
            results = self.enhanced_search.enhanced_search(query, filters, top_k=20)
            
            # Process results for API response
            processed_results = []
            for medicine in results:
                # Extract additional features
                medicine['dosage'] = self.extract_dosage(medicine.get('medicine_name', ''))
                medicine['ingredients_count'] = self.count_ingredients(medicine.get('salt_composition', ''))
                
                # Clean up NaN values for JSON serialization
                for key, value in medicine.items():
                    if pd.isna(value):
                        medicine[key] = None
                    elif isinstance(value, (np.integer, np.floating)):
                        medicine[key] = value.item()
                
                processed_results.append(medicine)
            
            return processed_results[:10]  # Return top 10 results
            
        except Exception as e:
            print(f"⚠️ Enhanced search failed: {e}")
            return []
    
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
    """Get analytics data endpoint with enhanced search metrics"""
    try:
        # Get enhanced search analytics
        search_analytics = pharma_api.enhanced_search.get_search_analytics()
        
        # Get basic dataset analytics
        df = pharma_api.enhanced_search.df
        if df is not None:
            basic_analytics = {
                'totalMedicines': len(df),
                'uniqueManufacturers': df['marketed_by'].nunique(),
                'packagingTypes': df['packagingType'].nunique(),
                'topManufacturers': df['marketed_by'].value_counts().head(10).to_dict(),
                'packagingDistribution': df['packagingType'].value_counts().head(10).to_dict()
            }
        else:
            basic_analytics = {}
        
        # Combine analytics
        analytics = {**basic_analytics, **search_analytics}
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/suggestions/<query>', methods=['GET'])
def get_suggestions(query):
    """Get search suggestions for autocomplete"""
    try:
        # Simple suggestion logic based on medicine names
        df = pharma_api.enhanced_search.df
        if df is None:
            return jsonify({'success': True, 'suggestions': []})
        
        query_lower = query.lower()
        suggestions = []
        
        # Find medicines that start with or contain the query
        for name in df['medicine_name'].dropna().unique():
            if query_lower in str(name).lower():
                suggestions.append(str(name))
                if len(suggestions) >= 10:
                    break
        
        return jsonify({
            'success': True,
            'suggestions': suggestions[:10]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/duplicates', methods=['GET'])
def get_duplicates():
    """Get information about duplicate medicines"""
    try:
        duplicate_info = {
            'total_groups': len(pharma_api.enhanced_search.duplicate_groups),
            'groups': []
        }
        
        # Get sample duplicate groups (limit to 10 for performance)
        for rep_id, group_ids in list(pharma_api.enhanced_search.duplicate_groups.items())[:10]:
            df = pharma_api.enhanced_search.df
            group_medicines = []
            
            for med_id in group_ids:
                medicine = df.iloc[med_id]
                group_medicines.append({
                    'id': med_id,
                    'name': medicine['medicine_name'],
                    'manufacturer': medicine['marketed_by']
                })
            
            duplicate_info['groups'].append({
                'representative_id': rep_id,
                'medicines': group_medicines
            })
        
        return jsonify({
            'success': True,
            'duplicates': duplicate_info
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    df = pharma_api.enhanced_search.df
    return jsonify({
        'success': True,
        'message': 'PharmaCatalogue API is running with Enhanced Search',
        'medicines_loaded': len(df) if df is not None else 0,
        'features': [
            'Symptom-based search',
            'Duplicate detection',
            'NLP-based ranking',
            'Query caching',
            'Enhanced TF-IDF'
        ]
    })

if __name__ == '__main__':
    print("Starting PharmaCatalogue API...")
    df = pharma_api.enhanced_search.df
    if df is not None:
        print(f"Loaded {len(df)} medicines")
    else:
        print("No medicines loaded - using fallback mode")
    app.run(debug=True, host='0.0.0.0', port=5000)