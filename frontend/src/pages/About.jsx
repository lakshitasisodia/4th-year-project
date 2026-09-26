import React from 'react'
import { Brain, Code, Database, TrendingUp, Users, Heart, Shield, Target } from 'lucide-react'

function About() {
  return (
    <div className="space-y-12 max-w-5xl mx-auto">
      {/* Hero Section */}
      <section className="text-center py-8">
        <div className="flex justify-center mb-6">
          <Brain size={64} className="text-blue-600" />
        </div>
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          About StressPredict
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          An AI-powered platform dedicated to helping students understand, monitor, and manage their stress levels through advanced machine learning technology.
        </p>
      </section>

      {/* Mission Section */}
      <section className="bg-white rounded-2xl shadow-lg p-8">
        <div className="flex items-center space-x-3 mb-6">
          <Heart size={32} className="text-red-500" />
          <h2 className="text-3xl font-bold text-gray-800">Our Mission</h2>
        </div>
        <p className="text-gray-600 text-lg leading-relaxed">
          Student mental health is a critical concern in today's academic environment. StressPredict was created to provide students with an accessible, evidence-based tool to assess their stress levels and receive personalized guidance. By leveraging machine learning and comprehensive stress research, we aim to make mental health monitoring as easy as checking your email.
        </p>
      </section>

      {/* How It Works */}
      <section className="bg-white rounded-2xl shadow-lg p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
          How It Works
        </h2>
        
        <div className="grid md:grid-cols-2 gap-8">
          {/* Step 1 */}
          <div className="flex space-x-4">
            <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-2xl font-bold text-blue-600">1</span>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                Choose Your Assessment
              </h3>
              <p className="text-gray-600">
                Select between Stress Level or Stress Type assessment based on what you want to understand about your current state.
              </p>
            </div>
          </div>

          {/* Step 2 */}
          <div className="flex space-x-4">
            <div className="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-2xl font-bold text-purple-600">2</span>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                Answer Questions
              </h3>
              <p className="text-gray-600">
                Respond honestly to questions about your mental health, physical symptoms, environment, and academic life.
              </p>
            </div>
          </div>

          {/* Step 3 */}
          <div className="flex space-x-4">
            <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-2xl font-bold text-green-600">3</span>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                Get AI Analysis
              </h3>
              <p className="text-gray-600">
                Our machine learning model analyzes your responses and provides an accurate stress prediction with confidence scores.
              </p>
            </div>
          </div>

          {/* Step 4 */}
          <div className="flex space-x-4">
            <div className="bg-yellow-100 w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-2xl font-bold text-yellow-600">4</span>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                Receive Recommendations
              </h3>
              <p className="text-gray-600">
                Get personalized recommendations and insights to help you better manage your stress and improve your wellbeing.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="bg-white rounded-2xl shadow-lg p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
          Technology & Methodology
        </h2>
        
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center p-6 bg-blue-50 rounded-lg">
            <Database size={40} className="text-blue-600 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Machine Learning
            </h3>
            <p className="text-gray-600 text-sm">
              Random Forest Classifier trained on extensive student stress datasets with high accuracy
            </p>
          </div>

          <div className="text-center p-6 bg-purple-50 rounded-lg">
            <Code size={40} className="text-purple-600 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Modern Stack
            </h3>
            <p className="text-gray-600 text-sm">
              Built with React, Flask, scikit-learn, and deployed with robust API architecture
            </p>
          </div>

          <div className="text-center p-6 bg-green-50 rounded-lg">
            <Shield size={40} className="text-green-600 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Evidence-Based
            </h3>
            <p className="text-gray-600 text-sm">
              Validated through rigorous testing with metrics including accuracy, F1-score, and MCC
            </p>
          </div>
        </div>
      </section>

      {/* The Models */}
      <section className="bg-white rounded-2xl shadow-lg p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
          Our Prediction Models
        </h2>
        
        <div className="space-y-6">
          {/* Stress Level Model */}
          <div className="border-l-4 border-blue-500 pl-6 py-4">
            <h3 className="text-2xl font-semibold text-gray-800 mb-3">
              Stress Level Predictor
            </h3>
            <p className="text-gray-600 mb-4">
              This model classifies stress into three categories: Low, Moderate, and High. It analyzes 20 different factors including:
            </p>
            <div className="grid md:grid-cols-2 gap-2 text-sm text-gray-600">
              <ul className="space-y-1">
                <li>• Mental health indicators (anxiety, depression)</li>
                <li>• Physical symptoms (headaches, breathing problems)</li>
                <li>• Sleep quality and patterns</li>
                <li>• Environmental factors (noise, living conditions)</li>
              </ul>
              <ul className="space-y-1">
                <li>• Academic performance and study load</li>
                <li>• Social support and peer relationships</li>
                <li>• Safety and basic needs fulfillment</li>
                <li>• Extracurricular involvement</li>
              </ul>
            </div>
          </div>

          {/* Stress Type Model */}
          <div className="border-l-4 border-purple-500 pl-6 py-4">
            <h3 className="text-2xl font-semibold text-gray-800 mb-3">
              Stress Type Classifier
            </h3>
            <p className="text-gray-600 mb-4">
              This model identifies the nature of stress: Distress (negative), Eustress (positive), or No Stress. It evaluates 24 behavioral and experiential factors:
            </p>
            <div className="grid md:grid-cols-2 gap-2 text-sm text-gray-600">
              <ul className="space-y-1">
                <li>• Recent stress experiences</li>
                <li>• Physical stress symptoms</li>
                <li>• Emotional state indicators</li>
                <li>• Sleep and concentration issues</li>
              </ul>
              <ul className="space-y-1">
                <li>• Academic workload perception</li>
                <li>• Social and relationship factors</li>
                <li>• Environment satisfaction</li>
                <li>• Academic confidence levels</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-white rounded-2xl shadow-lg p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
          Key Features
        </h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="flex space-x-4 p-4 bg-gray-50 rounded-lg">
            <Target size={24} className="text-blue-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-gray-800 mb-1">
                High Accuracy Predictions
              </h3>
              <p className="text-gray-600 text-sm">
                Models trained with advanced ML techniques achieving high accuracy through cross-validation and optimization
              </p>
            </div>
          </div>

          <div className="flex space-x-4 p-4 bg-gray-50 rounded-lg">
            <TrendingUp size={24} className="text-green-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-gray-800 mb-1">
                Confidence Scores
              </h3>
              <p className="text-gray-600 text-sm">
                See probability distributions across all categories to understand prediction certainty
              </p>
            </div>
          </div>

          <div className="flex space-x-4 p-4 bg-gray-50 rounded-lg">
            <Heart size={24} className="text-red-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-gray-800 mb-1">
                Personalized Recommendations
              </h3>
              <p className="text-gray-600 text-sm">
                Receive tailored advice based on your specific stress profile and classification
              </p>
            </div>
          </div>

          <div className="flex space-x-4 p-4 bg-gray-50 rounded-lg">
            <Users size={24} className="text-purple-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-gray-800 mb-1">
                Student-Focused Design
              </h3>
              <p className="text-gray-600 text-sm">
                Built specifically for academic environments with questions relevant to student life
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-800 mb-2 flex items-center space-x-2">
          <Shield size={20} className="text-yellow-600" />
          <span>Important Note</span>
        </h3>
        <p className="text-gray-700 text-sm">
          StressPredict is an educational tool designed to provide insights into stress levels. It is NOT a substitute for professional mental health diagnosis or treatment. If you're experiencing severe stress, anxiety, or depression, please consult with a qualified mental health professional or counselor. Your wellbeing is important, and professional support can make a significant difference.
        </p>
      </section>

      {/* CTA */}
      <section className="text-center py-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          Ready to Assess Your Stress?
        </h2>
        <p className="text-gray-600 mb-6">
          Choose an assessment and take the first step toward better stress management
        </p>
        <div className="flex justify-center space-x-4">
          <a 
            href="/stress-level" 
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
          >
            Stress Level Test
          </a>
          <a 
            href="/stress-type" 
            className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
          >
            Stress Type Test
          </a>
        </div>
      </section>
    </div>
  )
}

export default About