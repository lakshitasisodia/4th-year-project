import React, { useState } from 'react';
import { Activity, Brain, GraduationCap, Heart, AlertCircle } from 'lucide-react';

const StressPredictorDemo = () => {
  const [dataset, setDataset] = useState('d1');
  const [formData, setFormData] = useState({
    // Dataset 1 fields
    anxiety_level: 3,
    self_esteem: 3,
    mental_health_history: 2,
    depression: 2,
    headache: 2,
    blood_pressure: 2,
    sleep_quality: 3,
    breathing_problem: 1,
    study_load: 3,
    future_career_concerns: 3,
    social_support: 3,
    safety: 4,
    basic_needs: 4,
    academic_performance: 3,
    teacher_student_relationship: 3,
    
    // Dataset 2 fields
    age: 20,
    gender: 'Male',
    anxiety_tension: 3,
    headaches_often: 2,
    irritability: 2,
    concentration_difficulty: 3,
    sadness_low_mood: 2,
    illness_health_issues: 1,
    lonely_isolated: 2,
    academic_overload: 3,
    academic_confidence_lack: 2,
    subject_confidence_lack: 2,
    activity_conflict: 2,
    classes_regularity: 4
  });

  const [prediction, setPrediction] = useState(null);

  // Simulated prediction logic (replace with actual model when deployed)
  const predictStress = () => {
    if (dataset === 'd1') {
      // Dataset 1: Stress levels 0-2
      const mentalHealthScore = (
        formData.anxiety_level + 
        formData.depression + 
        formData.headache + 
        (6 - formData.sleep_quality) // reversed
      ) / 4;
      
      const academicScore = (
        formData.study_load + 
        formData.future_career_concerns +
        (6 - formData.academic_performance) // reversed
      ) / 3;
      
      const protectiveScore = (
        (6 - formData.self_esteem) + 
        (6 - formData.social_support) +
        (6 - formData.safety)
      ) / 3;
      
      const totalScore = (mentalHealthScore + academicScore + protectiveScore) / 3;
      
      let level = 0;
      let label = "Low Stress";
      let color = "bg-green-100 border-green-500 text-green-800";
      let advice = "You're managing well! Keep maintaining healthy habits.";
      
      if (totalScore > 3.5) {
        level = 2;
        label = "High Stress";
        color = "bg-red-100 border-red-500 text-red-800";
        advice = "Consider seeking support from counselors or mental health professionals.";
      } else if (totalScore > 2.5) {
        level = 1;
        label = "Moderate Stress";
        color = "bg-yellow-100 border-yellow-500 text-yellow-800";
        advice = "Try stress management techniques like exercise, meditation, or talking to friends.";
      }
      
      setPrediction({
        level,
        label,
        color,
        confidence: (85 + Math.random() * 10).toFixed(1),
        scores: {
          mental: mentalHealthScore.toFixed(2),
          academic: academicScore.toFixed(2),
          protective: protectiveScore.toFixed(2)
        },
        advice
      });
    } else {
      // Dataset 2: Stress types
      const mentalScore = (
        formData.anxiety_tension +
        formData.sadness_low_mood +
        formData.concentration_difficulty
      ) / 3;
      
      const academicScore = (
        formData.academic_overload +
        formData.academic_confidence_lack +
        formData.subject_confidence_lack
      ) / 3;
      
      let type = "Academic Stress";
      let color = "bg-blue-100 border-blue-500 text-blue-800";
      let advice = "Focus on time management and break tasks into smaller steps.";
      
      if (mentalScore > academicScore && mentalScore > 3.5) {
        type = "Psychological Stress";
        color = "bg-purple-100 border-purple-500 text-purple-800";
        advice = "Consider talking to a counselor about anxiety management techniques.";
      } else if (formData.lonely_isolated > 3) {
        type = "Social Stress";
        color = "bg-orange-100 border-orange-500 text-orange-800";
        advice = "Try joining student groups or reaching out to friends and family.";
      }
      
      setPrediction({
        type,
        color,
        confidence: (82 + Math.random() * 12).toFixed(1),
        scores: {
          mental: mentalScore.toFixed(2),
          academic: academicScore.toFixed(2),
          social: formData.lonely_isolated
        },
        advice
      });
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const ScaleInput = ({ label, field, icon: Icon }) => (
    <div className="mb-4">
      <div className="flex items-center mb-2">
        <Icon className="w-4 h-4 mr-2 text-gray-600" />
        <label className="text-sm font-medium text-gray-700">{label}</label>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-500">Low</span>
        <input
          type="range"
          min="1"
          max="5"
          value={formData[field]}
          onChange={(e) => handleInputChange(field, parseInt(e.target.value))}
          className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
        <span className="text-xs text-gray-500">High</span>
        <span className="ml-2 w-8 text-center font-semibold text-blue-600">{formData[field]}</span>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Brain className="w-12 h-12 text-indigo-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-800">Student Stress Predictor</h1>
          </div>
          <p className="text-gray-600">Machine Learning-Based Stress Level Assessment</p>
        </div>

        {/* Dataset Selection */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <GraduationCap className="w-5 h-5 mr-2 text-indigo-600" />
            Select Assessment Type
          </h2>
          <div className="flex gap-4">
            <button
              onClick={() => setDataset('d1')}
              className={`flex-1 p-4 rounded-lg border-2 transition-all ${
                dataset === 'd1'
                  ? 'border-indigo-500 bg-indigo-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="font-semibold">Comprehensive Assessment</div>
              <div className="text-sm text-gray-600 mt-1">Mental health, academic, and social factors</div>
            </button>
            <button
              onClick={() => setDataset('d2')}
              className={`flex-1 p-4 rounded-lg border-2 transition-all ${
                dataset === 'd2'
                  ? 'border-indigo-500 bg-indigo-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="font-semibold">Stress Type Classifier</div>
              <div className="text-sm text-gray-600 mt-1">Identify specific stress categories</div>
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Input Form */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-indigo-600" />
              Input Your Information
            </h2>
            
            <div className="max-h-[600px] overflow-y-auto pr-2">
              {dataset === 'd1' ? (
                <>
                  <h3 className="font-semibold text-gray-700 mb-3 mt-4">Mental Health Indicators</h3>
                  <ScaleInput label="Anxiety Level" field="anxiety_level" icon={Heart} />
                  <ScaleInput label="Depression Level" field="depression" icon={Heart} />
                  <ScaleInput label="Headaches Frequency" field="headache" icon={Heart} />
                  <ScaleInput label="Sleep Quality (1=Poor, 5=Excellent)" field="sleep_quality" icon={Heart} />
                  
                  <h3 className="font-semibold text-gray-700 mb-3 mt-6">Academic Factors</h3>
                  <ScaleInput label="Study Load" field="study_load" icon={GraduationCap} />
                  <ScaleInput label="Career Concerns" field="future_career_concerns" icon={GraduationCap} />
                  <ScaleInput label="Academic Performance (1=Poor, 5=Excellent)" field="academic_performance" icon={GraduationCap} />
                  
                  <h3 className="font-semibold text-gray-700 mb-3 mt-6">Protective Factors</h3>
                  <ScaleInput label="Self Esteem (1=Low, 5=High)" field="self_esteem" icon={Brain} />
                  <ScaleInput label="Social Support (1=Low, 5=High)" field="social_support" icon={Brain} />
                  <ScaleInput label="Safety (1=Unsafe, 5=Very Safe)" field="safety" icon={Brain} />
                </>
              ) : (
                <>
                  <div className="mb-4">
                    <label className="text-sm font-medium text-gray-700 block mb-2">Age</label>
                    <input
                      type="number"
                      value={formData.age}
                      onChange={(e) => handleInputChange('age', parseInt(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      min="15"
                      max="60"
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="text-sm font-medium text-gray-700 block mb-2">Gender</label>
                    <select
                      value={formData.gender}
                      onChange={(e) => handleInputChange('gender', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    >
                      <option>Male</option>
                      <option>Female</option>
                      <option>Other</option>
                    </select>
                  </div>
                  
                  <h3 className="font-semibold text-gray-700 mb-3 mt-4">Psychological Symptoms</h3>
                  <ScaleInput label="Anxiety/Tension" field="anxiety_tension" icon={Heart} />
                  <ScaleInput label="Sadness/Low Mood" field="sadness_low_mood" icon={Heart} />
                  <ScaleInput label="Difficulty Concentrating" field="concentration_difficulty" icon={Brain} />
                  <ScaleInput label="Feeling Lonely/Isolated" field="lonely_isolated" icon={Heart} />
                  
                  <h3 className="font-semibold text-gray-700 mb-3 mt-6">Academic Stressors</h3>
                  <ScaleInput label="Academic Overload" field="academic_overload" icon={GraduationCap} />
                  <ScaleInput label="Lack of Academic Confidence" field="academic_confidence_lack" icon={GraduationCap} />
                  <ScaleInput label="Subject Confidence Issues" field="subject_confidence_lack" icon={GraduationCap} />
                  <ScaleInput label="Class Attendance (1=Poor, 5=Excellent)" field="classes_regularity" icon={GraduationCap} />
                </>
              )}
            </div>

            <button
              onClick={predictStress}
              className="w-full mt-6 bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors flex items-center justify-center"
            >
              <Brain className="w-5 h-5 mr-2" />
              Predict Stress Level
            </button>
          </div>

          {/* Results */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <AlertCircle className="w-5 h-5 mr-2 text-indigo-600" />
              Prediction Results
            </h2>
            
            {prediction ? (
              <div className="space-y-4">
                <div className={`p-6 rounded-lg border-2 ${prediction.color}`}>
                  <div className="text-2xl font-bold mb-2">
                    {dataset === 'd1' ? prediction.label : prediction.type}
                  </div>
                  <div className="text-sm opacity-80">
                    Confidence: {prediction.confidence}%
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="font-semibold mb-3">Component Scores</h3>
                  <div className="space-y-2">
                    {dataset === 'd1' ? (
                      <>
                        <div className="flex justify-between">
                          <span>Mental Health:</span>
                          <span className="font-semibold">{prediction.scores.mental} / 5.0</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Academic Load:</span>
                          <span className="font-semibold">{prediction.scores.academic} / 5.0</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Risk Factors:</span>
                          <span className="font-semibold">{prediction.scores.protective} / 5.0</span>
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="flex justify-between">
                          <span>Mental Health:</span>
                          <span className="font-semibold">{prediction.scores.mental} / 5.0</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Academic Stress:</span>
                          <span className="font-semibold">{prediction.scores.academic} / 5.0</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Social Isolation:</span>
                          <span className="font-semibold">{prediction.scores.social} / 5.0</span>
                        </div>
                      </>
                    )}
                  </div>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                  <h3 className="font-semibold text-blue-900 mb-2">Recommendations</h3>
                  <p className="text-blue-800 text-sm">{prediction.advice}</p>
                </div>

                <div className="text-xs text-gray-500 mt-4">
                  ⚠️ This is a demonstration interface. For production use, integrate with your trained Random Forest models saved from the Jupyter notebook.
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <Brain className="w-16 h-16 mx-auto mb-4 opacity-30" />
                <p>Enter your information and click "Predict Stress Level" to see results</p>
              </div>
            )}
          </div>
        </div>

        {/* Info Box */}
        <div className="mt-6 bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="flex items-start">
            <AlertCircle className="w-5 h-5 text-amber-600 mr-3 mt-0.5 flex-shrink-0" />
            <div className="text-sm text-amber-800">
              <strong>Note:</strong> This interface demonstrates how your ML pipeline would work. To use your actual trained models:
              <ul className="list-disc ml-5 mt-2 space-y-1">
                <li>Save models using <code className="bg-amber-100 px-1 rounded">joblib.dump()</code></li>
                <li>Create a Flask/FastAPI backend to load models and make predictions</li>
                <li>Connect this frontend to your API endpoint</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StressPredictorDemo;