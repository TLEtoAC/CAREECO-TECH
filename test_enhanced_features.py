#!/usr/bin/env python3
"""
Test script for Enhanced PharmaCatalogue Features

This script demonstrates:
1. Symptom-based searching
2. Duplicate identification
3. NLP-based ranking
4. Query normalization and caching

Run this script to test all enhanced features.
"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def test_health_check():
    """Test if the enhanced API is running"""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        data = response.json()
        
        if data['success']:
            print(f"✅ API is running with {data['medicines_loaded']} medicines")
            print(f"🚀 Features: {', '.join(data['features'])}")
            return True
        else:
            print("❌ API health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_symptom_based_search():
    """Test symptom-based search functionality"""
    print("\n🎯 Testing Symptom-Based Search...")
    
    symptom_queries = [
        "headache",
        "fever and pain",
        "cold and cough",
        "acidity problem",
        "diabetes medicine",
        "blood pressure",
        "allergy relief",
        "infection treatment"
    ]
    
    for query in symptom_queries:
        try:
            response = requests.post(f"{API_BASE}/search", 
                                   json={"query": query})
            data = response.json()
            
            if data['success'] and data['medicines']:
                print(f"✅ '{query}' → {data['count']} results")
                
                # Show top result
                top_result = data['medicines'][0]
                print(f"   Top: {top_result['medicine_name']} ({top_result['confidence']}%)")
                
                # Check if it's symptom-based
                if top_result.get('search_type') == 'symptom':
                    print("   🎯 Symptom-based match detected!")
            else:
                print(f"⚠️  '{query}' → No results")
                
        except Exception as e:
            print(f"❌ Error testing '{query}': {e}")
        
        time.sleep(0.5)  # Rate limiting

def test_duplicate_detection():
    """Test duplicate detection functionality"""
    print("\n🔍 Testing Duplicate Detection...")
    
    try:
        response = requests.get(f"{API_BASE}/duplicates")
        data = response.json()
        
        if data['success']:
            duplicates = data['duplicates']
            print(f"✅ Found {duplicates['total_groups']} duplicate groups")
            
            # Show sample duplicate groups
            for i, group in enumerate(duplicates['groups'][:3]):
                print(f"\n   Group {i+1}:")
                for med in group['medicines']:
                    print(f"     - {med['name']} ({med['manufacturer']})")
        else:
            print("❌ Duplicate detection failed")
            
    except Exception as e:
        print(f"❌ Duplicate detection error: {e}")

def test_nlp_ranking():
    """Test NLP-based ranking with similar queries"""
    print("\n🧠 Testing NLP-Based Ranking...")
    
    # Test queries that should return similar results but with different rankings
    query_pairs = [
        ("paracetamol", "paracetamol tablet"),
        ("pain relief", "medicine for pain"),
        ("crocin", "crocin tablet"),
        ("antibiotic", "infection medicine"),
        ("diabetes", "diabetes treatment")
    ]
    
    for query1, query2 in query_pairs:
        try:
            # Search with first query
            response1 = requests.post(f"{API_BASE}/search", 
                                    json={"query": query1})
            data1 = response1.json()
            
            # Search with second query
            response2 = requests.post(f"{API_BASE}/search", 
                                    json={"query": query2})
            data2 = response2.json()
            
            if data1['success'] and data2['success']:
                count1 = data1['count']
                count2 = data2['count']
                
                print(f"✅ '{query1}' → {count1} results")
                print(f"✅ '{query2}' → {count2} results")
                
                # Compare top results
                if data1['medicines'] and data2['medicines']:
                    top1 = data1['medicines'][0]
                    top2 = data2['medicines'][0]
                    
                    print(f"   Top 1: {top1['medicine_name']} ({top1['confidence']}%)")
                    print(f"   Top 2: {top2['medicine_name']} ({top2['confidence']}%)")
                
                print()
            
        except Exception as e:
            print(f"❌ Error testing NLP ranking: {e}")
        
        time.sleep(0.5)

def test_query_variations():
    """Test handling of query variations and normalization"""
    print("\n🔄 Testing Query Variations...")
    
    # Test similar queries that should return similar results
    query_variations = [
        ["paracetamol", "paracetamol medicine", "paracetamol tablet"],
        ["headache", "head ache", "headache medicine"],
        ["crocin", "crocin tablet", "crocin medicine"],
        ["diabetes", "diabetes medicine", "diabetic medicine"]
    ]
    
    for variations in query_variations:
        print(f"\nTesting variations of: {variations[0]}")
        
        results = []
        for query in variations:
            try:
                response = requests.post(f"{API_BASE}/search", 
                                       json={"query": query})
                data = response.json()
                
                if data['success']:
                    results.append((query, data['count'], 
                                  data['medicines'][0]['confidence'] if data['medicines'] else 0))
                
            except Exception as e:
                print(f"❌ Error with '{query}': {e}")
        
        # Display results
        for query, count, confidence in results:
            print(f"   '{query}' → {count} results (top: {confidence}%)")

def test_search_suggestions():
    """Test search suggestions functionality"""
    print("\n💡 Testing Search Suggestions...")
    
    suggestion_queries = ["para", "croc", "diab", "anti", "pain"]
    
    for query in suggestion_queries:
        try:
            response = requests.get(f"{API_BASE}/suggestions/{query}")
            data = response.json()
            
            if data['success']:
                suggestions = data['suggestions']
                print(f"✅ '{query}' → {len(suggestions)} suggestions")
                
                # Show first few suggestions
                for suggestion in suggestions[:3]:
                    print(f"   - {suggestion}")
            else:
                print(f"⚠️  No suggestions for '{query}'")
                
        except Exception as e:
            print(f"❌ Error getting suggestions for '{query}': {e}")

def test_enhanced_analytics():
    """Test enhanced analytics endpoint"""
    print("\n📊 Testing Enhanced Analytics...")
    
    try:
        response = requests.get(f"{API_BASE}/analytics")
        data = response.json()
        
        if data['success']:
            analytics = data['analytics']
            
            print("✅ Enhanced Analytics:")
            print(f"   Total Medicines: {analytics.get('total_medicines', 'N/A')}")
            print(f"   Duplicate Groups: {analytics.get('duplicate_groups', 'N/A')}")
            print(f"   Cached Queries: {analytics.get('cached_queries', 'N/A')}")
            print(f"   Symptom Mappings: {analytics.get('symptom_mappings', 'N/A')}")
            print(f"   TF-IDF Features: {analytics.get('tfidf_features', 'N/A')}")
        else:
            print("❌ Analytics failed")
            
    except Exception as e:
        print(f"❌ Analytics error: {e}")

def main():
    """Run all tests"""
    print("🧪 Enhanced PharmaCatalogue Feature Tests")
    print("=" * 50)
    
    # Check if API is running
    if not test_health_check():
        print("\n❌ API is not running. Please start the backend server first.")
        print("Run: python backend/app.py")
        return
    
    # Run all tests
    test_symptom_based_search()
    test_duplicate_detection()
    test_nlp_ranking()
    test_query_variations()
    test_search_suggestions()
    test_enhanced_analytics()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\n📝 Summary of Enhanced Features:")
    print("✅ Symptom-based search - Find medicines by symptoms")
    print("✅ Duplicate detection - Identify and handle duplicate medicines")
    print("✅ NLP-based ranking - Intelligent relevance scoring")
    print("✅ Query normalization - Handle variations in search terms")
    print("✅ Search caching - Improved performance for repeated queries")
    print("✅ Enhanced analytics - Detailed search metrics")

if __name__ == "__main__":
    main()