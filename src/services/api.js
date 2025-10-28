import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
console.log('API_BASE_URL configured as:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Search medicines
export const searchMedicines = async (query, filters = {}) => {
  try {
    console.log('Making API call to:', `${API_BASE_URL}/search`);
    console.log('Query:', query, 'Filters:', filters);
    
    const response = await api.post('/search', {
      query,
      filters
    });
    
    console.log('API Response:', response.data);
    console.log('Response status:', response.status);
    console.log('Response has medicines?', response.data && response.data.medicines);
    console.log('Medicines count:', response.data?.medicines?.length);
    
    // Handle different response formats
    if (response.data && response.data.medicines) {
      console.log('✅ Returning medicines array with', response.data.medicines.length, 'items');
      return response.data.medicines;
    } else if (response.data && Array.isArray(response.data)) {
      console.log('✅ Returning direct array with', response.data.length, 'items');
      return response.data;
    } else {
      console.warn('❌ Unexpected response format:', response.data);
      return [];
    }
  } catch (error) {
    console.error('Search API error:', error);
    console.error('Error details:', error.response?.data || error.message);
    throw error;
  }
};

// Get recommendations based on medicine
export const getRecommendations = async (medicineId) => {
  try {
    const response = await api.get(`/recommendations/${medicineId}`);
    return response.data.recommendations || [];
  } catch (error) {
    console.error('Recommendations API error:', error);
    throw error;
  }
};

// Get analytics data
export const getAnalytics = async () => {
  try {
    const response = await api.get('/analytics');
    return response.data;
  } catch (error) {
    console.error('Analytics API error:', error);
    throw error;
  }
};

// Predict medicine category
export const predictCategory = async (medicineData) => {
  try {
    const response = await api.post('/predict', medicineData);
    return response.data;
  } catch (error) {
    console.error('Prediction API error:', error);
    throw error;
  }
};

export default api;