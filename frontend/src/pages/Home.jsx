import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Brain, Activity, FileText, TrendingUp, Shield, Target, ArrowRight } from 'lucide-react'
import { healthCheck, getModelInfo } from '../api/stressApi'

function Home() {
  const [apiStatus, setApiStatus] = useState(null)
  const [modelInfo, setModelInfo] = useState(null)

  useEffect(() => {
    const checkStatus = async () => {
      try {
        await healthCheck()
        setApiStatus('connected')
        const info = await getModelInfo()
        setModelInfo(info.data)
      } catch (error) {
        setApiStatus('disconnected')
        console.error('API connection failed:', error)
      }
    }
    checkStatus()
  }, [])

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12">
        <div className="flex justify-center mb-6">
          <Brain size={80} className="text-blue-600" />
        </div>
        <h1 className="text-5xl font-bold text-gray-800 mb-4">
          Welcome to StressPredict
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          AI-powered stress prediction system designed to help students understand and manage their stress levels using advanced machine learning technology.
        </p>
        
        {/* API Status Badge */}
        {apiStatus && (
          <div className="flex justify-center mb-8">
            <div className={`inline-flex items-center px-4 py-2 rounded-full ${
              apiStatus === 'connected' 
                ? 'bg-green-100 text-green-700' 
                : 'bg-red-100 text-red-700'
            }`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${
                apiStatus === 'connected' ? 'bg-green-500' : 'bg-red-500'
              }`} />
              {apiStatus === 'connected' ? 'API Connected' : 'API Disconnected'}
            </div>
          </div>
        )}
      </section>

      {/* Prediction Types */}
      <section className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        {/* Stress Level Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-xl transition-shadow border-2 border-blue-100">
          <div className="flex items-center space-x-4 mb-6">
            <div className="bg-blue-100 p-4 rounded-lg">
              <Activity size={32} className="text-blue-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Stress Level Test</h2>
          </div>
          
          <p className="text-gray-600 mb-6">
            Assess your overall stress level based on mental health, physical symptoms, environment, and academic factors. Get classified as Low, Moderate, or High stress.
          </p>
          
          <div className="space-y-3 mb-6">
            <div className="flex items-start space-x-2">
              <Target size={18} className="text-blue-600 mt-1 flex-shrink-0" />
              <span className="text-sm text-gray-600">20 comprehensive questions</span>
            </div>
            <div className="flex items-start space-x-2">
              <Shield size={18} className="text-blue-600 mt-1 flex-shrink-0" />
              <span className="text-sm text-gray-600">
                Accuracy: {modelInfo?.dataset_1?.accuracy || '...'}%
              </span>
            </div>
            <div className="flex items-start space-x-2">
              <TrendingUp size={18} className="text-blue-600 mt-1 flex-shrink-0" />
              <span className="text-sm text-gray-600">Personalized recommendations</span>
            </div>
          </div>

          <Link 
            to="/stress-level" 
            className="block w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center space-x-2"
          >
            <span>Take Stress Level Test</span>
            <ArrowRight size={20} />
          </Link>
        </div>

        {/* Stress Type Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-xl transition-shadow border-2 border-purple-100">
          <div className="flex items-center space-x-4 mb-6">
            <div className="bg-purple-100 p-4 rounded-lg">
              <FileText size={32} className="text-purple-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Stress Type Test</h2>
          </div>
          
          <p className="text-gray-600 mb-6">
            Identify whether you're experiencing distress (negative), eustress (positive), or no stress. Understand the nature of your stress through detailed behavioral analysis.
          </p>
          
          <div className="space-y-3 mb-6">
            <div className="flex items-start space-x-2">
              <Target size={18} className="text-purple-600 mt-1 flex-shrink-0" />
              <span className="text-sm text-gray-600">24 targeted questions</span>
            </div>
            <div className="flex items-start space-x-2">
              <Shield size={18} className="text-purple-600 mt-1 flex-shrink-0" />
              <span className="text-sm text-gray-600">
                Accuracy: {modelInfo?.dataset_2?.accuracy || '...'}%
              </span>
            </div>
            <div className="flex items-start space-x-2">
              <TrendingUp size={18} className="text-purple-600 mt-1 flex-shrink-0" />
              <span className="text-sm text-gray-600">Stress classification insights</span>
            </div>
          </div>

          <Link 
            to="/stress-type" 
            className="block w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center space-x-2"
          >
            <span>Take Stress Type Test</span>
            <ArrowRight size={20} />
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-white rounded-2xl shadow-lg p-8 max-w-5xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
          Why Use StressPredict?
        </h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Brain size={32} className="text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              AI-Powered
            </h3>
            <p className="text-gray-600">
              Advanced machine learning models trained on extensive student stress data
            </p>
          </div>

          <div className="text-center">
            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield size={32} className="text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Evidence-Based
            </h3>
            <p className="text-gray-600">
              High accuracy predictions validated through rigorous testing
            </p>
          </div>

          <div className="text-center">
            <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Target size={32} className="text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Actionable Insights
            </h3>
            <p className="text-gray-600">
              Receive personalized recommendations based on your results
            </p>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="text-center py-8">
        <p className="text-lg text-gray-600 mb-4">
          Take control of your mental wellbeing today
        </p>
        <div className="flex justify-center space-x-4">
          <Link 
            to="/stress-level" 
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
          >
            Start Assessment
          </Link>
          <Link 
            to="/about" 
            className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-8 rounded-lg transition-colors"
          >
            Learn More
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Home