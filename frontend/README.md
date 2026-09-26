# StressPredict - Student Stress Prediction System

An AI-powered web application that predicts student stress levels and types using machine learning. Built with React (frontend) and Flask (backend), this system uses Random Forest classifiers to analyze various factors affecting student mental health.

![StressPredict](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18+-61dafb)
![Flask](https://img.shields.io/badge/Flask-2.3+-black)

## 🎯 Features

### Two Prediction Models

1. **Stress Level Predictor**
   - Classifies stress as: Low, Moderate, or High
   - Analyzes 20 factors including mental health, physical symptoms, environment, and academics
   - Provides confidence scores for each category
   - High accuracy: ~85-90%

2. **Stress Type Classifier**
   - Identifies stress type: Distress (negative), Eustress (positive), or No Stress
   - Uses 24 behavioral and experiential questions
   - Likert scale (1-5) responses
   - High accuracy: ~85-90%

### Key Capabilities

- ✅ Real-time predictions using trained ML models
- ✅ Confidence scores and probability distributions
- ✅ Personalized recommendations based on results
- ✅ Responsive design with Tailwind CSS
- ✅ Form validation on both frontend and backend
- ✅ RESTful API architecture
- ✅ Professional UI/UX with loading states and error handling

## 📁 Project Structure

```
stress-prediction-system/
│
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── components/         # Reusable components
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── ResultCard.jsx
│   │   │
│   │   ├── pages/              # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── About.jsx
│   │   │   ├── StressLevelForm.jsx
│   │   │   └── StressTypeForm.jsx
│   │   │
│   │   ├── api/           # API services
│   │   │   └── stressApi.js
│   │   │
│   │   ├── utils/              # Utilities
│   │   │   ├── constants.js
│   │   │   └── validators.js
│   │   │
│   │   ├── App.jsx             # Main app component
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Global styles
│   │
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/                     # Flask Backend
│   ├── models/                 # ML models
│   │   └── predictor.py
│   │
│   ├── routes/                 # API routes
│   │   └── prediction.py
│   │
│   ├── utils/                  # Utilities
│   │   └── validator.py
│   │
│   ├── trained_models/         # Serialized models (generated)
│   │   ├── rf_d1.pkl
│   │   ├── rf_d2.pkl
│   │   ├── scaler_d1.pkl
│   │   ├── scaler_d2.pkl
│   │   ├── features_d1.pkl
│   │   ├── features_d2.pkl
│   │   └── metrics.pkl
│   │
│   ├── app.py                  # Flask app
│   ├── config.py               # Configuration
│   ├── backendCode.py          # ML training pipeline
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```bash
   FLASK_APP=app.py
   FLASK_ENV=development
   PORT=5000
   HOST=0.0.0.0
   ```

5. **Train models (if not already trained)**
   ```bash
   python backendCode.py
   ```
   This will create the `trained_models/` directory with all necessary model files.

6. **Run the Flask server**
   ```bash
   python app.py
   ```
   Server will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Update API URL (if needed)**
   Edit `src/utils/constants.js`:
   ```javascript
   export const API_BASE_URL = 'http://localhost:5000/api'
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5173`

## 📦 Dependencies

### Backend (Python)

```txt
flask==2.3.0
flask-cors==4.0.0
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.3.0
imbalanced-learn==0.11.0
joblib==1.3.0
scipy==1.11.0
matplotlib==3.7.0
seaborn==0.12.0
```

### Frontend (JavaScript)

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.292.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "vite": "^5.0.0"
  }
}
```

## 🔌 API Endpoints

### Health & Info

- `GET /api/health` - Check API status
- `GET /api/model-info` - Get model performance metrics

### Predictions

- `POST /api/predict/stress-level` - Predict stress level
  - Body: 20 numeric fields (see config.py for field names)
  - Response: prediction, confidence scores, recommendation

- `POST /api/predict/stress-type` - Predict stress type
  - Body: Gender, Age, + 23 Likert scale questions
  - Response: stress type, probabilities, recommendation

### Features

- `GET /api/features/stress-level` - Get D1 features and ranges
- `GET /api/features/stress-type` - Get D2 features

## 📊 Model Information

### Stress Level Model (Dataset 1)

**Input Features (20):**
- Mental Health: anxiety_level, depression, self_esteem, mental_health_history
- Physical: headache, blood_pressure, sleep_quality, breathing_problem
- Environment: noise_level, living_conditions, safety, basic_needs
- Academic: academic_performance, study_load, teacher_student_relationship, future_career_concerns
- Social: social_support, peer_pressure, extracurricular_activities, bullying

**Output:**
- 0: Low Stress
- 1: Moderate Stress
- 2: High Stress

### Stress Type Model (Dataset 2)

**Input Features (24):**
- Demographics: Gender (0/1), Age (15-60)
- Behavioral: 23 Likert scale questions (1-5)

**Output:**
- 0: Distress (negative stress)
- 1: Eustress (positive stress)
- 2: No Stress

### Model Training Pipeline

The `backendCode.py` script implements:
1. Data loading and validation
2. Quality control (outlier detection, straight-line response filtering)
3. Feature engineering (reverse coding, normalization)
4. Train/test split with stratification
5. SMOTE for class imbalance (Dataset 2)
6. Model training (Logistic Regression & Random Forest)
7. Evaluation (Accuracy, F1-Score, MCC)
8. Feature importance analysis
9. Model serialization

## 🎨 UI Components

### Pages
- **Home** - Landing page with model info and navigation
- **About** - Detailed information about the project
- **Stress Level Form** - 20-field assessment form
- **Stress Type Form** - 24-question Likert scale survey

### Components
- **Header** - Navigation bar with active state indicators
- **Footer** - Contact info and links
- **LoadingSpinner** - Loading state indicator
- **ResultCard** - Displays predictions with color-coded results

## 🔒 Input Validation

### Frontend Validation
- Required field checks
- Range validation
- Data type validation
- Real-time error feedback

### Backend Validation
- Field presence verification
- Data type checking
- Range enforcement
- Detailed error messages

## 🚧 Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

**Backend:**
```bash
cd backend
pip install gunicorn
gunicorn app:app
```

## 📝 Usage Example

### Using the API Directly

**Stress Level Prediction:**
```bash
curl -X POST http://localhost:5000/api/predict/stress-level \
  -H "Content-Type: application/json" \
  -d '{
    "anxiety_level": 15,
    "self_esteem": 20,
    "mental_health_history": 0,
    "depression": 10,
    "headache": 3,
    "blood_pressure": 2,
    "sleep_quality": 6,
    "breathing_problem": 2,
    "noise_level": 3,
    "living_conditions": 7,
    "safety": 8,
    "basic_needs": 8,
    "academic_performance": 3,
    "study_load": 7,
    "teacher_student_relationship": 6,
    "future_career_concerns": 8,
    "social_support": 7,
    "peer_pressure": 5,
    "extracurricular_activities": 4,
    "bullying": 1
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "prediction": 1,
    "stress_level": "Moderate Stress",
    "confidence": {
      "low": 15.23,
      "moderate": 68.45,
      "high": 16.32
    },
    "recommendation": "Your stress level is moderate. Consider stress management techniques...",
    "model_accuracy": 87.5
  }
}
```

## ⚠️ Important Notes

1. **Model Files Required**: Ensure `trained_models/` directory exists with all .pkl files before running the backend
2. **CORS Configuration**: Backend is configured for `localhost:5173` and `localhost:3000`
3. **Educational Purpose**: This tool is for educational purposes and should not replace professional medical advice
4. **Data Privacy**: No data is stored; all predictions are stateless

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name/Team Name

## 📞 Support

For support, email support@stresspredict.com or open an issue in the repository.

## 🙏 Acknowledgments

- Dataset sources
- Machine learning libraries: scikit-learn, imbalanced-learn
- Frontend framework: React
- Backend framework: Flask
- UI components: Tailwind CSS, Lucide React

---

**Made with ❤️ for Student Wellbeing**