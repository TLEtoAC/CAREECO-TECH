import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import re
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
from difflib import SequenceMatcher
import json

# Download required NLTK data
def download_nltk_data():
    """Download required NLTK data with compatibility for different versions"""
    try:
        # Try punkt_tab first (newer NLTK versions)
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            try:
                nltk.download('punkt_tab')
            except:
                # Fallback to punkt for older versions
                nltk.download('punkt')
        
        # Download stopwords
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        # Download wordnet
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
            
        print("✅ NLTK data downloaded successfully")
        return True
        
    except Exception as e:
        print(f"⚠️ NLTK download error: {e}")
        return False

# Download NLTK data
download_nltk_data()

class EnhancedPharmaSearch:
    def __init__(self):
        self.df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.symptom_vectorizer = None
        self.symptom_matrix = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.query_cache = {}
        self.duplicate_groups = {}
        
        # Symptom to medicine mapping
        self.symptom_medicine_map = {
            'headache': ['paracetamol', 'ibuprofen', 'aspirin', 'diclofenac'],
            'fever': ['paracetamol', 'ibuprofen', 'aspirin', 'acetaminophen'],
            'pain': ['paracetamol', 'ibuprofen', 'diclofenac', 'tramadol', 'ketorolac'],
            'cold': ['cetirizine', 'phenylephrine', 'pseudoephedrine', 'loratadine'],
            'cough': ['dextromethorphan', 'guaifenesin', 'codeine'],
            'allergy': ['cetirizine', 'loratadine', 'fexofenadine', 'diphenhydramine'],
            'acidity': ['pantoprazole', 'omeprazole', 'ranitidine', 'esomeprazole'],
            'diabetes': ['metformin', 'glimepiride', 'insulin', 'gliclazide'],
            'hypertension': ['amlodipine', 'losartan', 'atenolol', 'ramipril'],
            'infection': ['amoxicillin', 'azithromycin', 'ceftriaxone', 'ciprofloxacin'],
            'inflammation': ['ibuprofen', 'diclofenac', 'prednisolone', 'dexamethasone'],
            'nausea': ['ondansetron', 'domperidone', 'metoclopramide'],
            'diarrhea': ['loperamide', 'ofloxacin', 'norfloxacin'],
            'constipation': ['lactulose', 'bisacodyl', 'docusate'],
            'anxiety': ['alprazolam', 'lorazepam', 'diazepam'],
            'depression': ['sertraline', 'fluoxetine', 'amitriptyline'],
            'insomnia': ['zolpidem', 'melatonin', 'diphenhydramine'],
            'asthma': ['salbutamol', 'montelukast', 'budesonide'],
            'arthritis': ['diclofenac', 'ibuprofen', 'methotrexate'],
            'migraine': ['sumatriptan', 'rizatriptan', 'paracetamol']
        }
        
    def load_data(self, csv_path, skip_duplicates=False):
        """Load and prepare pharmaceutical data"""
        try:
            self.df = pd.read_csv(csv_path)
            print(f"✅ Loaded {len(self.df)} medicines")
            
            # Clean and prepare data
            self.prepare_enhanced_search_data()
            
            # Optionally skip duplicate detection for faster startup
            if skip_duplicates:
                print("⚠️ Skipping duplicate detection for faster startup")
                self.duplicate_groups = {}
            else:
                self.identify_duplicates()
            
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def clean_text(self, text):
        """Advanced text cleaning with NLP"""
        if pd.isna(text):
            return ""
        
        text = str(text).lower()
        
        # Remove special characters but keep medical terms
        text = re.sub(r'[^\w\s\+\-\(\)]', ' ', text)
        
        # Tokenize with fallback for different NLTK versions
        try:
            tokens = word_tokenize(text)
        except Exception as e:
            print(f"⚠️ Tokenization error: {e}")
            # Fallback to simple split if NLTK fails
            tokens = text.split()
        
        # Remove stopwords but keep medical terms
        medical_stopwords = {'mg', 'tablet', 'capsule', 'injection', 'syrup', 'ml', 'gm'}
        tokens = [token for token in tokens if token not in self.stop_words or token in medical_stopwords]
        
        # Lemmatize with error handling
        try:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        except Exception as e:
            print(f"⚠️ Lemmatization error: {e}")
            # Continue without lemmatization if it fails
        
        return ' '.join(tokens)
    
    def prepare_enhanced_search_data(self):
        """Prepare data with enhanced NLP processing"""
        print("🔄 Preparing enhanced search data...")
        
        # Create comprehensive search text
        self.df['enhanced_search_text'] = (
            self.df['medicine_name'].fillna('').apply(self.clean_text) + ' ' +
            self.df['salt_composition'].fillna('').apply(self.clean_text) + ' ' +
            self.df['marketed_by'].fillna('').apply(self.clean_text) + ' ' +
            self.df['packagingType'].fillna('').apply(self.clean_text)
        )
        
        # Create TF-IDF matrix with enhanced parameters
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 3),  # Include trigrams for better matching
            stop_words='english',
            min_df=2,  # Ignore terms that appear in less than 2 documents
            max_df=0.8,  # Ignore terms that appear in more than 80% of documents
            sublinear_tf=True  # Use sublinear TF scaling
        )
        
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['enhanced_search_text'])
        
        # Create symptom-based search capability
        self.prepare_symptom_search()
        
        print("✅ Enhanced search data prepared")
    
    def prepare_symptom_search(self):
        """Prepare symptom-based search mapping"""
        print("🔄 Preparing symptom-based search...")
        
        # Create symptom descriptions for medicines
        symptom_descriptions = []
        
        for _, row in self.df.iterrows():
            medicine_name = str(row['medicine_name']).lower()
            composition = str(row['salt_composition']).lower()
            
            # Map medicines to symptoms based on active ingredients
            symptoms = []
            for symptom, medicines in self.symptom_medicine_map.items():
                for medicine in medicines:
                    if medicine in composition or medicine in medicine_name:
                        symptoms.append(symptom)
            
            symptom_descriptions.append(' '.join(symptoms))
        
        self.df['symptom_description'] = symptom_descriptions
        
        # Create symptom TF-IDF matrix
        self.symptom_vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        # Only fit if we have symptom data
        non_empty_symptoms = [desc for desc in symptom_descriptions if desc.strip()]
        if non_empty_symptoms:
            self.symptom_matrix = self.symptom_vectorizer.fit_transform(symptom_descriptions)
        
        print("✅ Symptom-based search prepared")
    
    def identify_duplicates(self):
        """Identify duplicate medicines using optimized similarity (faster approach)"""
        print("🔄 Identifying duplicate medicines (optimized)...")
        
        # For large datasets, use a faster heuristic approach
        if len(self.df) > 10000:
            print(f"📊 Large dataset detected ({len(self.df)} medicines), using fast duplicate detection...")
            self.fast_duplicate_detection()
        else:
            print("📊 Small dataset, using comprehensive duplicate detection...")
            self.comprehensive_duplicate_detection()
    
    def fast_duplicate_detection(self):
        """Fast duplicate detection for large datasets"""
        duplicate_groups = defaultdict(list)
        
        # Create normalized name and composition dictionaries for fast lookup
        name_groups = defaultdict(list)
        comp_groups = defaultdict(list)
        
        print("🔄 Grouping by normalized names and compositions...")
        
        for i, row in self.df.iterrows():
            # Group by normalized names
            norm_name = self.normalize_medicine_name(row['medicine_name'])
            if norm_name:  # Only if not empty
                name_groups[norm_name].append(i)
            
            # Group by normalized compositions
            norm_comp = self.normalize_composition(row['salt_composition'])
            if norm_comp:  # Only if not empty
                comp_groups[norm_comp].append(i)
        
        print("🔄 Processing duplicate groups...")
        
        # Process name-based groups
        group_id = 0
        for norm_name, indices in name_groups.items():
            if len(indices) > 1:
                # Use the most complete entry as representative
                representative = max(indices, key=lambda x: len(str(self.df.iloc[x]['medicine_name'])))
                duplicate_groups[representative] = indices
                group_id += 1
        
        # Process composition-based groups (merge with existing if needed)
        for norm_comp, indices in comp_groups.items():
            if len(indices) > 1:
                # Check if any of these are already in a group
                existing_group = None
                for rep, group in duplicate_groups.items():
                    if any(idx in group for idx in indices):
                        existing_group = rep
                        break
                
                if existing_group:
                    # Merge with existing group
                    duplicate_groups[existing_group].extend(
                        [idx for idx in indices if idx not in duplicate_groups[existing_group]]
                    )
                else:
                    # Create new group
                    representative = max(indices, key=lambda x: len(str(self.df.iloc[x]['medicine_name'])))
                    duplicate_groups[representative] = indices
        
        self.duplicate_groups = duplicate_groups
        print(f"✅ Fast duplicate detection completed: {len(duplicate_groups)} groups found")
    
    def comprehensive_duplicate_detection(self):
        """Comprehensive duplicate detection for smaller datasets"""
        duplicate_groups = defaultdict(list)
        processed = set()
        
        total = len(self.df)
        for i, row1 in self.df.iterrows():
            if i in processed:
                continue
            
            if i % 1000 == 0:  # Progress indicator
                print(f"   Progress: {i}/{total} ({i/total*100:.1f}%)")
                
            group = [i]
            name1 = self.normalize_medicine_name(row1['medicine_name'])
            comp1 = self.normalize_composition(row1['salt_composition'])
            
            # Only check remaining items
            for j in range(i+1, len(self.df)):
                if j in processed:
                    continue
                
                row2 = self.df.iloc[j]
                name2 = self.normalize_medicine_name(row2['medicine_name'])
                comp2 = self.normalize_composition(row2['salt_composition'])
                
                # Check similarity
                if self.are_duplicates(name1, comp1, name2, comp2):
                    group.append(j)
                    processed.add(j)
            
            if len(group) > 1:
                # Use the most complete entry as the representative
                representative = max(group, key=lambda x: len(str(self.df.iloc[x]['medicine_name'])))
                duplicate_groups[representative] = group
            
            processed.add(i)
        
        self.duplicate_groups = duplicate_groups
        print(f"✅ Comprehensive duplicate detection completed: {len(duplicate_groups)} groups found")
    
    def normalize_medicine_name(self, name):
        """Normalize medicine name for duplicate detection"""
        if pd.isna(name):
            return ""
        
        name = str(name).lower()
        # Remove common variations
        name = re.sub(r'\b(tablet|capsule|injection|syrup|ml|mg|gm)\b', '', name)
        name = re.sub(r'\d+', '', name)  # Remove numbers
        name = re.sub(r'[^\w\s]', '', name)  # Remove special characters
        return ' '.join(name.split())
    
    def normalize_composition(self, composition):
        """Normalize composition for duplicate detection"""
        if pd.isna(composition):
            return ""
        
        comp = str(composition).lower()
        # Extract active ingredients
        ingredients = re.findall(r'([a-zA-Z\s]+)', comp)
        ingredients = [ing.strip() for ing in ingredients if ing.strip()]
        return ' '.join(sorted(ingredients))
    
    def are_duplicates(self, name1, comp1, name2, comp2):
        """Determine if two medicines are duplicates"""
        # Check name similarity
        name_similarity = SequenceMatcher(None, name1, name2).ratio()
        
        # Check composition similarity
        comp_similarity = SequenceMatcher(None, comp1, comp2).ratio()
        
        # Consider duplicates if high similarity in either name or composition
        return name_similarity > 0.8 or comp_similarity > 0.9
    
    def normalize_query(self, query):
        """Normalize search query for caching and duplicate detection"""
        query = query.lower().strip()
        
        # Remove common variations
        query = re.sub(r'\b(medicine|tablet|capsule|for|the|a|an)\b', '', query)
        query = re.sub(r'\s+', ' ', query).strip()
        
        # Sort words for consistent caching
        words = query.split()
        words.sort()
        
        return ' '.join(words)
    
    def enhanced_search(self, query, filters=None, top_k=20):
        """Enhanced search with NLP ranking and duplicate handling"""
        if not query.strip():
            return []
        
        # Normalize query for caching
        normalized_query = self.normalize_query(query)
        cache_key = f"{normalized_query}_{str(filters)}"
        
        # Check cache
        if cache_key in self.query_cache:
            print(f"📋 Cache hit for query: {query}")
            return self.query_cache[cache_key]
        
        print(f"🔍 Enhanced search for: {query}")
        
        # Clean the query
        cleaned_query = self.clean_text(query)
        
        # 1. Symptom-based search
        symptom_results = self.symptom_based_search(query, top_k//2)
        
        # 2. Regular TF-IDF search
        tfidf_results = self.tfidf_search(cleaned_query, top_k)
        
        # 3. Combine and rank results
        combined_results = self.combine_and_rank_results(
            symptom_results, tfidf_results, query, top_k
        )
        
        # 4. Handle duplicates
        final_results = self.handle_duplicates(combined_results)
        
        # 5. Apply filters
        if filters:
            final_results = self.apply_filters(final_results, filters)
        
        # Cache the results
        self.query_cache[cache_key] = final_results[:top_k]
        
        return final_results[:top_k]
    
    def symptom_based_search(self, query, top_k):
        """Search based on symptoms"""
        results = []
        
        if self.symptom_matrix is None:
            return results
        
        # Check if query contains symptom keywords
        query_lower = query.lower()
        matching_symptoms = []
        
        for symptom in self.symptom_medicine_map.keys():
            if symptom in query_lower:
                matching_symptoms.append(symptom)
        
        if not matching_symptoms:
            return results
        
        print(f"🎯 Found symptoms: {matching_symptoms}")
        
        # Create symptom query vector
        symptom_query = ' '.join(matching_symptoms)
        
        try:
            query_vector = self.symptom_vectorizer.transform([symptom_query])
            similarity_scores = cosine_similarity(query_vector, self.symptom_matrix).flatten()
            
            # Get top matches
            top_indices = similarity_scores.argsort()[-top_k:][::-1]
            
            for idx in top_indices:
                if similarity_scores[idx] > 0.1:
                    medicine = self.df.iloc[idx].to_dict()
                    medicine['id'] = int(idx)
                    medicine['confidence'] = int(similarity_scores[idx] * 100)
                    medicine['search_type'] = 'symptom'
                    results.append(medicine)
        
        except Exception as e:
            print(f"⚠️ Symptom search error: {e}")
        
        return results
    
    def tfidf_search(self, cleaned_query, top_k):
        """Traditional TF-IDF search with enhancements"""
        results = []
        
        try:
            # Transform query
            query_vector = self.tfidf_vectorizer.transform([cleaned_query])
            
            # Calculate similarity
            similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top matches
            top_indices = similarity_scores.argsort()[-top_k:][::-1]
            
            for idx in top_indices:
                if similarity_scores[idx] > 0.05:  # Lower threshold for more results
                    medicine = self.df.iloc[idx].to_dict()
                    medicine['id'] = int(idx)
                    medicine['confidence'] = int(similarity_scores[idx] * 100)
                    medicine['search_type'] = 'tfidf'
                    results.append(medicine)
        
        except Exception as e:
            print(f"⚠️ TF-IDF search error: {e}")
        
        return results
    
    def combine_and_rank_results(self, symptom_results, tfidf_results, original_query, top_k):
        """Combine and rank results using NLP-based scoring"""
        # Create a dictionary to merge results by medicine ID
        merged_results = {}
        
        # Add symptom results with boost
        for result in symptom_results:
            med_id = result['id']
            result['confidence'] = min(100, result['confidence'] + 20)  # Boost symptom matches
            merged_results[med_id] = result
        
        # Add TF-IDF results
        for result in tfidf_results:
            med_id = result['id']
            if med_id in merged_results:
                # Combine scores
                existing_conf = merged_results[med_id]['confidence']
                new_conf = result['confidence']
                merged_results[med_id]['confidence'] = min(100, int((existing_conf + new_conf) / 2 * 1.2))
                merged_results[med_id]['search_type'] = 'combined'
            else:
                merged_results[med_id] = result
        
        # Convert back to list and apply NLP ranking
        results = list(merged_results.values())
        
        # Apply additional NLP-based ranking
        for result in results:
            nlp_score = self.calculate_nlp_score(result, original_query)
            result['confidence'] = min(100, int(result['confidence'] * nlp_score))
        
        # Sort by confidence
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return results
    
    def calculate_nlp_score(self, medicine, query):
        """Calculate NLP-based relevance score"""
        score_multiplier = 1.0
        
        query_lower = query.lower()
        medicine_name = str(medicine.get('medicine_name', '')).lower()
        composition = str(medicine.get('salt_composition', '')).lower()
        
        # Exact match bonus
        if query_lower in medicine_name:
            score_multiplier *= 1.5
        
        # Composition match bonus
        query_words = query_lower.split()
        for word in query_words:
            if len(word) > 3 and word in composition:
                score_multiplier *= 1.2
        
        # Brand name recognition
        common_brands = ['crocin', 'dolo', 'combiflam', 'augmentin', 'azee', 'pantocid']
        for brand in common_brands:
            if brand in query_lower and brand in medicine_name:
                score_multiplier *= 1.3
        
        return min(1.8, score_multiplier)  # Cap the multiplier
    
    def handle_duplicates(self, results):
        """Handle duplicate medicines in results"""
        seen_groups = set()
        filtered_results = []
        
        for result in results:
            med_id = result['id']
            
            # Check if this medicine is part of a duplicate group
            representative_id = None
            for rep_id, group in self.duplicate_groups.items():
                if med_id in group:
                    representative_id = rep_id
                    break
            
            if representative_id is not None:
                if representative_id not in seen_groups:
                    # Use the representative medicine
                    if med_id == representative_id:
                        filtered_results.append(result)
                    else:
                        # Replace with representative
                        rep_medicine = self.df.iloc[representative_id].to_dict()
                        rep_medicine['id'] = representative_id
                        rep_medicine['confidence'] = result['confidence']
                        rep_medicine['search_type'] = result.get('search_type', 'tfidf')
                        filtered_results.append(rep_medicine)
                    
                    seen_groups.add(representative_id)
            else:
                # Not a duplicate, add as is
                filtered_results.append(result)
        
        return filtered_results
    
    def apply_filters(self, results, filters):
        """Apply search filters"""
        filtered_results = results
        
        if filters.get('packagingType'):
            filtered_results = [
                r for r in filtered_results 
                if r.get('packagingType') == filters['packagingType']
            ]
        
        if filters.get('manufacturer'):
            filtered_results = [
                r for r in filtered_results 
                if r.get('marketed_by') == filters['manufacturer']
            ]
        
        # Sort by specified criteria
        sort_by = filters.get('sortBy', 'relevance')
        if sort_by == 'name':
            filtered_results.sort(key=lambda x: x.get('medicine_name', ''))
        elif sort_by == 'manufacturer':
            filtered_results.sort(key=lambda x: x.get('marketed_by', ''))
        elif sort_by == 'confidence':
            filtered_results.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        # 'relevance' is already sorted by confidence
        
        return filtered_results
    
    def get_search_analytics(self):
        """Get analytics about search performance"""
        return {
            'total_medicines': len(self.df),
            'duplicate_groups': len(self.duplicate_groups),
            'cached_queries': len(self.query_cache),
            'symptom_mappings': len(self.symptom_medicine_map),
            'tfidf_features': self.tfidf_matrix.shape[1] if self.tfidf_matrix is not None else 0
        }