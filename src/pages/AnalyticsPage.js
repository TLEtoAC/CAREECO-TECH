import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, Package, Building2, Pill } from 'lucide-react';

const AnalyticsPage = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading analytics data
    setTimeout(() => {
      setAnalyticsData(getSampleAnalytics());
      setLoading(false);
    }, 1000);
  }, []);

  const getSampleAnalytics = () => {
    return {
      totalMedicines: 15420,
      uniqueManufacturers: 1250,
      packagingTypes: 45,
      avgConfidence: 87.5,
      packagingDistribution: [
        { name: 'Strip/Blister', value: 6500, percentage: 42 },
        { name: 'Tablet', value: 3200, percentage: 21 },
        { name: 'Capsule', value: 2100, percentage: 14 },
        { name: 'Injection', value: 1800, percentage: 12 },
        { name: 'Syrup', value: 1000, percentage: 6 },
        { name: 'Others', value: 820, percentage: 5 }
      ],
      manufacturerDistribution: [
        { name: 'GSK Pharmaceuticals', count: 850 },
        { name: 'Cipla Ltd', count: 720 },
        { name: 'Sun Pharma', count: 680 },
        { name: 'Dr. Reddy\'s', count: 620 },
        { name: 'Lupin Ltd', count: 580 },
        { name: 'Aurobindo Pharma', count: 540 },
        { name: 'Torrent Pharma', count: 480 },
        { name: 'Others', count: 4950 }
      ],
      dosageDistribution: [
        { dosage: '500mg', count: 2800 },
        { dosage: '250mg', count: 2200 },
        { dosage: '100mg', count: 1800 },
        { dosage: '10mg', count: 1500 },
        { dosage: '50mg', count: 1200 },
        { dosage: '25mg', count: 1000 },
        { dosage: '5mg', count: 800 }
      ]
    };
  };

  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];

  if (loading) {
    return (
      <div className="container" style={{ padding: '60px 20px', textAlign: 'center' }}>
        <div className="loading" style={{ margin: '0 auto 20px' }}></div>
        <p>Loading analytics data...</p>
      </div>
    );
  }

  return (
    <div className="container" style={{ padding: '40px 20px' }}>
      <div className="page-header" style={{ marginBottom: '40px', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: '700', color: 'white', marginBottom: '16px' }}>
          Dataset Analytics
        </h1>
        <p style={{ fontSize: '1.2rem', color: 'rgba(255,255,255,0.8)' }}>
          Insights from your pharmaceutical dataset and ML model performance
        </p>
      </div>

      {/* Key Metrics */}
      <div className="metrics-grid" style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
        gap: '20px', 
        marginBottom: '40px' 
      }}>
        <div className="metric-card card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ 
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
              padding: '12px', 
              borderRadius: '12px',
              color: 'white'
            }}>
              <Pill size={24} />
            </div>
            <div>
              <h3 style={{ fontSize: '2rem', fontWeight: '700', margin: '0', color: '#2c3e50' }}>
                {analyticsData.totalMedicines.toLocaleString()}
              </h3>
              <p style={{ margin: '4px 0 0', color: '#6c757d' }}>Total Medicines</p>
            </div>
          </div>
        </div>

        <div className="metric-card card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ 
              background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', 
              padding: '12px', 
              borderRadius: '12px',
              color: 'white'
            }}>
              <Building2 size={24} />
            </div>
            <div>
              <h3 style={{ fontSize: '2rem', fontWeight: '700', margin: '0', color: '#2c3e50' }}>
                {analyticsData.uniqueManufacturers.toLocaleString()}
              </h3>
              <p style={{ margin: '4px 0 0', color: '#6c757d' }}>Manufacturers</p>
            </div>
          </div>
        </div>

        <div className="metric-card card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ 
              background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', 
              padding: '12px', 
              borderRadius: '12px',
              color: 'white'
            }}>
              <Package size={24} />
            </div>
            <div>
              <h3 style={{ fontSize: '2rem', fontWeight: '700', margin: '0', color: '#2c3e50' }}>
                {analyticsData.packagingTypes}
              </h3>
              <p style={{ margin: '4px 0 0', color: '#6c757d' }}>Packaging Types</p>
            </div>
          </div>
        </div>

        <div className="metric-card card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ 
              background: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)', 
              padding: '12px', 
              borderRadius: '12px',
              color: '#2c3e50'
            }}>
              <TrendingUp size={24} />
            </div>
            <div>
              <h3 style={{ fontSize: '2rem', fontWeight: '700', margin: '0', color: '#2c3e50' }}>
                {analyticsData.avgConfidence}%
              </h3>
              <p style={{ margin: '4px 0 0', color: '#6c757d' }}>Avg ML Confidence</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="charts-grid" style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', 
        gap: '30px' 
      }}>
        {/* Packaging Distribution */}
        <div className="card">
          <h3 style={{ marginBottom: '20px', color: '#2c3e50' }}>Packaging Type Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={analyticsData.packagingDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name} (${percentage}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {analyticsData.packagingDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Top Manufacturers */}
        <div className="card">
          <h3 style={{ marginBottom: '20px', color: '#2c3e50' }}>Top Manufacturers</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData.manufacturerDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                angle={-45}
                textAnchor="end"
                height={100}
                fontSize={12}
              />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#667eea" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Dosage Distribution */}
        <div className="card">
          <h3 style={{ marginBottom: '20px', color: '#2c3e50' }}>Common Dosages</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData.dosageDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="dosage" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#764ba2" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Model Performance */}
        <div className="card">
          <h3 style={{ marginBottom: '20px', color: '#2c3e50' }}>ML Model Performance</h3>
          <div style={{ padding: '20px' }}>
            <div style={{ marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span>Random Forest Accuracy</span>
                <span style={{ fontWeight: '600' }}>94.2%</span>
              </div>
              <div style={{ background: '#e9ecef', borderRadius: '4px', height: '8px' }}>
                <div style={{ 
                  background: 'linear-gradient(90deg, #28a745, #20c997)', 
                  width: '94.2%', 
                  height: '100%', 
                  borderRadius: '4px' 
                }} />
              </div>
            </div>
            
            <div style={{ marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span>Logistic Regression Accuracy</span>
                <span style={{ fontWeight: '600' }}>87.8%</span>
              </div>
              <div style={{ background: '#e9ecef', borderRadius: '4px', height: '8px' }}>
                <div style={{ 
                  background: 'linear-gradient(90deg, #ffc107, #fd7e14)', 
                  width: '87.8%', 
                  height: '100%', 
                  borderRadius: '4px' 
                }} />
              </div>
            </div>

            <div style={{ 
              background: '#f8f9fa', 
              padding: '16px', 
              borderRadius: '8px',
              marginTop: '20px'
            }}>
              <h4 style={{ margin: '0 0 12px', color: '#495057' }}>Key Insights</h4>
              <ul style={{ margin: 0, paddingLeft: '20px', color: '#6c757d' }}>
                <li>Random Forest shows best performance for packaging prediction</li>
                <li>High confidence scores indicate reliable recommendations</li>
                <li>Model trained on {analyticsData.totalMedicines.toLocaleString()} medicine records</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;