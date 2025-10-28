# PharmaCatalogue - AI-Powered Medicine Recommendation System

A comprehensive pharmaceutical catalogue system that leverages artificial intelligence to provide accurate medicine recommendations and comprehensive drug information.

## 🚀 Features

- **AI-Powered Search**: Intelligent medicine search using TF-IDF vectorization and cosine similarity
- **Smart Recommendations**: ML-based medicine recommendations using Random Forest and Logistic Regression
- **Advanced Filters**: Filter by packaging type, manufacturer, and sort options
- **Data Analytics**: Comprehensive dashboard with visualizations and insights
- **Responsive Design**: Modern React.js interface optimized for all devices
- **Real-time Results**: Fast search with confidence scoring

## 🛠️ Technology Stack

### Frontend
- **React.js** - Modern UI framework
- **React Router** - Navigation and routing
- **Recharts** - Data visualization
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client

### Backend
- **Flask** - Python web framework
- **Pandas** - Data manipulation
- **Scikit-learn** - Machine learning
- **TF-IDF** - Text feature extraction
- **Cosine Similarity** - Recommendation engine

### Machine Learning
- **Random Forest** - Classification model
- **Logistic Regression** - Alternative model
- **Feature Engineering** - Text processing and encoding
- **Data Preprocessing** - Cleaning and transformation

## 📁 Project Structure

```
pharma-catalogue/
├── src/                          # React frontend
│   ├── components/              # Reusable components
│   │   ├── Header.js
│   │   ├── MedicineCard.js
│   │   └── SearchFilters.js
│   ├── pages/                   # Page components
│   │   ├── SearchPage.js
│   │   ├── AnalyticsPage.js
│   │   └── AboutPage.js
│   ├── services/               # API services
│   │   └── api.js
│   └── App.js                  # Main app component
├── backend/                     # Flask API
│   ├── app.py                  # Main API server
│   └── requirements.txt        # Python dependencies
├── public/                     # Static files
├── Stage1_Product_initial_dataset.csv      # Main dataset
├── processed_pharma_data_features.csv      # Processed features
├── processed_pharma_data_full_processed.csv # Full processed data
├── ml_model_example.py         # ML model implementation
├── data_analysis.py            # Data analysis and visualization
├── preprocess_pharma_data.py   # Data preprocessing pipeline
├── preprocessing_summary.py    # Data preprocessing summary
├── package.json               # Node.js dependencies
├── requirements.txt           # Python dependencies (root)
├── .gitignore                # Git ignore file
└── README.md                 # Project documentation
```

## 📋 **Essential Files for Users**

### **Required Files:**
- `Stage1_Product_initial_dataset.csv` - Main pharmaceutical dataset
- `src/` - Complete React frontend application
- `backend/` - Flask API server
- `package.json` - Frontend dependencies
- `README.md` - Setup and usage instructions

### **Optional Files (for development/analysis):**
- `ml_model_example.py` - ML model training example
- `data_analysis.py` - Data visualization and analysis
- `preprocess_pharma_data.py` - Data preprocessing pipeline
- `preprocessing_summary.py` - Preprocessing summary generator
- `processed_pharma_data_*.csv` - Pre-processed datasets

### **Generated Files (excluded from git):**
- `node_modules/` - Frontend dependencies
- `venv/` - Python virtual environment
- `build/` - Production build files
- `*.png` - Generated visualization charts
- `processed_pharma_data_*.csv` - Large processed datasets (73MB+ files)
- `.env` - Environment variables

### **⚠️ Large Files Notice:**
The processed CSV files (`processed_pharma_data_*.csv`) are excluded from git due to GitHub's 100MB file size limit. Users can generate these files by running the preprocessing script.

## 🚀 Quick Start

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- npm or yarn

### Frontend Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start the development server**
   ```bash
   npm start
   ```

3. **Open your browser**
   Navigate to `http://localhost:3000`

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Flask server**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

### Machine Learning Setup

1. **Generate processed data files (Required for first run)**
   ```bash
   python preprocess_pharma_data.py
   ```
   *This will create the large processed CSV files needed by the backend*

2. **Train ML models**
   ```bash
   python ml_model_example.py
   ```

3. **Generate analytics**
   ```bash
   python data_analysis.py
   ```

### **📊 Data Processing Note**
If you cloned this repository, you'll need to generate the processed data files first:
- Run `python preprocess_pharma_data.py` to create processed datasets
- This generates `processed_pharma_data_*.csv` files (excluded from git due to size)
- The backend requires these files to function properly

## 📊 Dataset Information

The project uses a comprehensive pharmaceutical dataset containing:

- **15,000+** medicine records
- **Medicine names** and compositions
- **Salt compositions** with active ingredients
- **Packaging types** and quantities
- **Manufacturer information**
- **GST and pricing data**

### Data Processing Pipeline

1. **Data Cleaning**: Remove duplicates, handle missing values
2. **Feature Extraction**: Extract dosage, ingredient count, packaging info
3. **Text Processing**: TF-IDF vectorization for medicine names and compositions
4. **Encoding**: Label encoding for categorical variables
5. **Scaling**: StandardScaler for numerical features
6. **Model Training**: Random Forest and Logistic Regression

## 🔍 API Endpoints

### Search Medicines
```http
POST /api/search
Content-Type: application/json

{
  "query": "paracetamol",
  "filters": {
    "packagingType": "tablet",
    "manufacturer": "GSK Pharmaceuticals",
    "sortBy": "relevance"
  }
}
```

### Get Recommendations
```http
GET /api/recommendations/{medicine_id}
```

### Analytics Data
```http
GET /api/analytics
```

### Health Check
```http
GET /api/health
```

## 🎯 Usage Examples

### Basic Search
```javascript
// Search for paracetamol medicines
const results = await searchMedicines('paracetamol');
```

### Filtered Search
```javascript
// Search with filters
const results = await searchMedicines('antibiotic', {
  packagingType: 'tablet',
  manufacturer: 'Cipla Ltd',
  sortBy: 'name'
});
```

### Get Recommendations
```javascript
// Get similar medicines
const recommendations = await getRecommendations(123);
```

## 📈 Model Performance

- **Random Forest Accuracy**: 94.2%
- **Logistic Regression Accuracy**: 87.8%
- **Average Confidence Score**: 87.5%
- **Feature Count**: 5000+ TF-IDF features

## 🎨 UI Features

### Search Interface
- Real-time search with autocomplete
- Advanced filtering options
- Sort by relevance, name, manufacturer
- Confidence scoring for results

### Medicine Cards
- Detailed medicine information
- Composition breakdown
- Manufacturer details
- Packaging information
- Confidence indicators

### Analytics Dashboard
- Interactive charts and graphs
- Market distribution analysis
- Model performance metrics
- Key insights and trends

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:5000/api
FLASK_ENV=development
FLASK_DEBUG=True
```

### API Configuration
Update `src/services/api.js` for custom API endpoints:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

## 🚀 Deployment

### Frontend Deployment
```bash
npm run build
# Deploy the build folder to your hosting service
```

### Backend Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Data Structures Course** - Academic foundation
- **Scikit-learn** - Machine learning framework
- **React Community** - Frontend development
- **Flask** - Backend API framework

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code examples

---

**Built with ❤️ for the Data Structures Course Project**