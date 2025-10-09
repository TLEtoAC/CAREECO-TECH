import React, { useState, useEffect } from 'react';
import { Search, Filter, Loader } from 'lucide-react';
import MedicineCard from '../components/MedicineCard';
import SearchFilters from '../components/SearchFilters';
import { searchMedicines, getRecommendations } from '../services/api';

const SearchPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [medicines, setMedicines] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    packagingType: '',
    manufacturer: '',
    sortBy: 'relevance'
  });
  const [showFilters, setShowFilters] = useState(false);
  const [searchPerformed, setSearchPerformed] = useState(false);

  const testDirectConnection = async () => {
    console.log('Testing direct connection to backend...');
    try {
      const response = await fetch('http://localhost:5000/api/health');
      const data = await response.json();
      console.log('Direct connection test result:', data);
      alert(`Backend connection: ${data.success ? 'SUCCESS' : 'FAILED'}\nMedicines loaded: ${data.medicines_loaded}`);
    } catch (error) {
      console.error('Direct connection failed:', error);
      alert(`Backend connection FAILED: ${error.message}`);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    alert(`🔍 Starting search for: "${searchQuery}"`);
    console.log('🔍 SEARCH STARTED for:', searchQuery);
    
    setLoading(true);
    setSearchPerformed(true);
    
    try {
      console.log('Searching for:', searchQuery);
      const results = await searchMedicines(searchQuery, filters);
      console.log('Search results:', results);
      console.log('Results type:', typeof results, 'Length:', results?.length);
      
      if (results && results.length > 0) {
        console.log('✅ Setting medicines state with', results.length, 'items');
        console.log('First medicine:', results[0]);
        setMedicines(results);
        console.log('✅ Medicines state updated');
      } else {
        console.log('No results returned from API, using sample data');
        setMedicines(getSampleMedicines(searchQuery));
      }
    } catch (error) {
      console.error('Search failed:', error);
      console.log('Using sample data due to error');
      // For demo purposes, show sample data
      setMedicines(getSampleMedicines(searchQuery));
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const getSampleMedicines = (query) => {
    // Sample data for demonstration
    const sampleData = [
      {
        id: 1,
        medicine_name: "Paracetamol 500mg Tablet 10 tablets",
        salt_composition: "Paracetamol (500mg)",
        packagingType: "strip or blister pack",
        pack: "10 tablets",
        marketed_by: "Generic Pharma Ltd",
        confidence: 95,
        dosage: "500mg",
        ingredients_count: 1
      },
      {
        id: 2,
        medicine_name: "Aceper Tablet 10 tablets",
        salt_composition: "Paracetamol (500mg) + Phenylpropanolamine (25mg) + Cetirizine (10mg)",
        packagingType: "strip or blister pack",
        pack: "10 tablets",
        marketed_by: "3A Pharmaceuticals",
        confidence: 87,
        dosage: "500mg",
        ingredients_count: 3
      },
      {
        id: 3,
        medicine_name: "Crocin 650mg Tablet 15 tablets",
        salt_composition: "Paracetamol (650mg)",
        packagingType: "strip or blister pack",
        pack: "15 tablets",
        marketed_by: "GSK Pharmaceuticals",
        confidence: 92,
        dosage: "650mg",
        ingredients_count: 1
      }
    ];

    return sampleData.filter(med => 
      med.medicine_name.toLowerCase().includes(query.toLowerCase()) ||
      med.salt_composition.toLowerCase().includes(query.toLowerCase())
    );
  };

  return (
    <div>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <h1 className="hero-title">AI-Powered Medicine Search</h1>
          <p className="hero-subtitle">
            Find the right medicines with intelligent recommendations powered by machine learning
          </p>
        </div>
      </section>

      {/* Search Section */}
      <section className="search-section">
        <div className="container">
          <div className="search-container">
            <input
              type="text"
              className="search-input"
              placeholder="Search for medicines, compositions, or symptoms..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button 
              className="search-btn"
              onClick={handleSearch}
              disabled={loading}
            >
              {loading ? <Loader className="loading" size={20} /> : <Search size={20} />}
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>

          <div className="filters-container">
            <button 
              className="btn btn-secondary"
              onClick={() => setShowFilters(!showFilters)}
            >
              <Filter size={16} />
              Filters
            </button>
            <button 
              className="btn btn-secondary"
              onClick={testDirectConnection}
              style={{ marginLeft: '10px' }}
            >
              Test Backend Connection
            </button>
          </div>

          {showFilters && (
            <SearchFilters 
              filters={filters}
              onFiltersChange={setFilters}
            />
          )}
        </div>
      </section>

      {/* Results Section */}
      {searchPerformed && (
        <section className="results-section">
          <div className="container">
            {loading ? (
              <div className="loading-container" style={{ textAlign: 'center', padding: '40px' }}>
                <Loader className="loading" size={40} />
                <p style={{ marginTop: '16px', color: '#6c757d' }}>
                  Searching medicines and generating recommendations...
                </p>
              </div>
            ) : (
              <>
                <div className="results-header">
                  <h2 className="results-count">
                    {medicines.length} medicine{medicines.length !== 1 ? 's' : ''} found
                  </h2>
                  {console.log('🎯 RENDERING: medicines.length =', medicines.length)}
                  {console.log('🎯 RENDERING: medicines =', medicines)}
                </div>

                {medicines.length > 0 ? (
                  <div className="medicine-grid">
                    {medicines.map((medicine) => (
                      <MedicineCard 
                        key={medicine.id} 
                        medicine={medicine} 
                      />
                    ))}
                  </div>
                ) : (
                  <div className="no-results">
                    <div className="no-results-icon">🔍</div>
                    <h3 className="no-results-title">No medicines found</h3>
                    <p className="no-results-text">
                      Try adjusting your search terms or filters to find what you're looking for.
                    </p>
                  </div>
                )}
              </>
            )}
          </div>
        </section>
      )}
    </div>
  );
};

export default SearchPage;