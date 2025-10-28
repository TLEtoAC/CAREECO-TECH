import React from 'react';
import { Brain, Database, Search, BarChart3, Shield, Zap } from 'lucide-react';

const AboutPage = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Recommendations',
      description: 'Advanced machine learning algorithms analyze medicine compositions and provide intelligent recommendations based on similarity and effectiveness patterns.'
    },
    {
      icon: Database,
      title: 'Comprehensive Database',
      description: 'Access to thousands of medicines with detailed information including compositions, manufacturers, packaging types, and dosage information.'
    },
    {
      icon: Search,
      title: 'Smart Search',
      description: 'Intelligent search functionality that understands medical terminology, brand names, generic names, and active ingredients.'
    },
    {
      icon: BarChart3,
      title: 'Data Analytics',
      description: 'Comprehensive analytics dashboard showing market trends, manufacturer distributions, and model performance metrics.'
    },
    {
      icon: Shield,
      title: 'Reliable Data',
      description: 'All medicine data is carefully processed and validated to ensure accuracy and reliability for healthcare professionals.'
    },
    {
      icon: Zap,
      title: 'Fast Performance',
      description: 'Optimized algorithms and efficient data structures ensure quick search results and real-time recommendations.'
    }
  ];

  const techStack = [
    { name: 'React.js', description: 'Modern frontend framework for building interactive user interfaces' },
    { name: 'Python', description: 'Backend processing and machine learning model development' },
    { name: 'Scikit-learn', description: 'Machine learning library for building recommendation models' },
    { name: 'Pandas', description: 'Data manipulation and analysis for processing pharmaceutical data' },
    { name: 'TF-IDF', description: 'Text feature extraction for medicine name and composition analysis' },
    { name: 'Random Forest', description: 'Ensemble learning method for accurate medicine classification' }
  ];

  return (
    <div className="container" style={{ padding: '40px 20px' }}>
      {/* Hero Section */}
      <div className="page-header" style={{ marginBottom: '60px', textAlign: 'center' }}>
        <h1 style={{ fontSize: '3rem', fontWeight: '700', color: 'white', marginBottom: '20px' }}>
          About PharmaCatalogue
        </h1>
        <p style={{ fontSize: '1.3rem', color: 'rgba(255,255,255,0.9)', maxWidth: '800px', margin: '0 auto', lineHeight: '1.6' }}>
          An intelligent pharmaceutical catalogue system that leverages artificial intelligence to provide 
          accurate medicine recommendations and comprehensive drug information for healthcare professionals and patients.
        </p>
      </div>

      {/* Project Overview */}
      <div className="card" style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '2rem', fontWeight: '600', marginBottom: '20px', color: '#2c3e50' }}>
          Project Overview
        </h2>
        <div style={{ fontSize: '16px', lineHeight: '1.7', color: '#495057' }}>
          <p style={{ marginBottom: '16px' }}>
            PharmaCatalogue is a comprehensive Data Structures Course project that combines machine learning, 
            data analysis, and modern web development to create an intelligent medicine recommendation system. 
            The project addresses the critical need for accurate and accessible pharmaceutical information in healthcare.
          </p>
          <p style={{ marginBottom: '16px' }}>
            Our system processes extensive pharmaceutical datasets, applies advanced preprocessing techniques, 
            and utilizes machine learning algorithms to provide users with relevant medicine recommendations 
            based on their search queries and specific requirements.
          </p>
          <p>
            The platform serves both healthcare professionals and patients by offering detailed medicine information, 
            composition analysis, manufacturer details, and intelligent suggestions for alternative medications.
          </p>
        </div>
      </div>

      {/* Features Grid */}
      <div style={{ marginBottom: '60px' }}>
        <h2 style={{ fontSize: '2rem', fontWeight: '600', marginBottom: '30px', color: 'white', textAlign: 'center' }}>
          Key Features
        </h2>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', 
          gap: '24px' 
        }}>
          {features.map((feature, index) => (
            <div key={index} className="card" style={{ padding: '30px' }}>
              <div style={{ 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
                padding: '16px', 
                borderRadius: '12px',
                color: 'white',
                width: 'fit-content',
                marginBottom: '20px'
              }}>
                <feature.icon size={28} />
              </div>
              <h3 style={{ fontSize: '1.3rem', fontWeight: '600', marginBottom: '12px', color: '#2c3e50' }}>
                {feature.title}
              </h3>
              <p style={{ color: '#6c757d', lineHeight: '1.6' }}>
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Technology Stack */}
      <div className="card" style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '2rem', fontWeight: '600', marginBottom: '30px', color: '#2c3e50' }}>
          Technology Stack
        </h2>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: '20px' 
        }}>
          {techStack.map((tech, index) => (
            <div key={index} style={{ 
              padding: '20px', 
              background: '#f8f9fa', 
              borderRadius: '8px',
              border: '1px solid #e9ecef'
            }}>
              <h4 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '8px', color: '#495057' }}>
                {tech.name}
              </h4>
              <p style={{ color: '#6c757d', fontSize: '14px', margin: 0, lineHeight: '1.5' }}>
                {tech.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Project Workflow */}
      <div className="card" style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '2rem', fontWeight: '600', marginBottom: '30px', color: '#2c3e50' }}>
          Project Workflow
        </h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {[
            {
              step: '1',
              title: 'Data Collection & Preprocessing',
              description: 'Comprehensive pharmaceutical dataset processing including text cleaning, feature extraction, and missing value handling.'
            },
            {
              step: '2',
              title: 'Feature Engineering',
              description: 'Advanced feature creation using TF-IDF vectorization, categorical encoding, and numerical scaling for optimal ML performance.'
            },
            {
              step: '3',
              title: 'Model Training',
              description: 'Implementation of multiple ML algorithms including Random Forest and Logistic Regression for medicine classification and recommendation.'
            },
            {
              step: '4',
              title: 'Frontend Development',
              description: 'Modern React.js interface with responsive design, intelligent search, and interactive data visualizations.'
            },
            {
              step: '5',
              title: 'Integration & Testing',
              description: 'Seamless integration between ML models and frontend interface with comprehensive testing and validation.'
            }
          ].map((item, index) => (
            <div key={index} style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
              <div style={{ 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: '600',
                flexShrink: 0
              }}>
                {item.step}
              </div>
              <div>
                <h4 style={{ fontSize: '1.2rem', fontWeight: '600', marginBottom: '8px', color: '#2c3e50' }}>
                  {item.title}
                </h4>
                <p style={{ color: '#6c757d', lineHeight: '1.6', margin: 0 }}>
                  {item.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Contact Information */}
      <div className="card" style={{ textAlign: 'center' }}>
        <h2 style={{ fontSize: '2rem', fontWeight: '600', marginBottom: '20px', color: '#2c3e50' }}>
          Project Information
        </h2>
        <p style={{ fontSize: '16px', color: '#6c757d', marginBottom: '20px' }}>
          This project was developed as part of the Data Structures Course, demonstrating the practical 
          application of data structures, algorithms, and machine learning in healthcare technology.
        </p>
        <div style={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          padding: '20px',
          borderRadius: '12px',
          marginTop: '20px'
        }}>
          <h3 style={{ margin: '0 0 8px', fontSize: '1.3rem' }}>Ready to explore medicines?</h3>
          <p style={{ margin: '0 0 16px', opacity: 0.9 }}>
            Start searching for medicines and discover intelligent recommendations powered by AI.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;