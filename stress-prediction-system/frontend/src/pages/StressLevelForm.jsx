import React, { useState } from 'react'
import { Activity, AlertCircle, CheckCircle, Info } from 'lucide-react'
import { predictStressLevel } from '../api/stressApi'
import { validateStressLevelInput } from '../utils/validators'
import { STRESS_LEVEL_FIELDS } from '../utils/constants'
import LoadingSpinner from '../components/LoadingSpinner'
import ResultCard from '../components/ResultCard'

function StressLevelForm() {
  const [formData, setFormData] = useState(() => {
    const initialData = {}
    STRESS_LEVEL_FIELDS.forEach(field => {
      initialData[field.name] = ''
    })
    return initialData
  })
  
  const [errors, setErrors] = useState({})
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [serverError, setServerError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value === '' ? '' : Number(value)
    }))
    
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[name]
        return newErrors
      })
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setServerError(null)
    setResult(null)
    
    // Validate input
    const validation = validateStressLevelInput(formData)
    
    if (!validation.isValid) {
      setErrors(validation.errors)
      window.scrollTo({ top: 0, behavior: 'smooth' })
      return
    }
    
    setErrors({})
    setLoading(true)
    
    try {
      const response = await predictStressLevel(formData)
      
      if (response.success) {
        setResult(response.data)
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } else {
        setServerError(response.error || 'Prediction failed')
      }
    } catch (error) {
      console.error('Prediction error:', error)
      setServerError(
        error.response?.data?.error || 
        'Failed to connect to the server. Please ensure the backend is running.'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    const resetData = {}
    STRESS_LEVEL_FIELDS.forEach(field => {
      resetData[field.name] = ''
    })
    setFormData(resetData)
    setErrors({})
    setResult(null)
    setServerError(null)
  }

  const renderField = (field) => {
    const hasError = errors[field.name]
    
    if (field.type === 'select') {
      return (
        <div key={field.name} className="space-y-2">
          <label className="block text-sm font-semibold text-gray-700">
            {field.label}
            <span className="text-red-500 ml-1">*</span>
          </label>
          <select
            name={field.name}
            value={formData[field.name]}
            onChange={handleChange}
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              hasError ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            <option value="">Select...</option>
            {field.options.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {hasError && (
            <p className="text-red-500 text-xs mt-1 flex items-center space-x-1">
              <AlertCircle size={12} />
              <span>{errors[field.name]}</span>
            </p>
          )}
        </div>
      )
    }
    
    return (
      <div key={field.name} className="space-y-2">
        <label className="block text-sm font-semibold text-gray-700">
          {field.label}
          <span className="text-red-500 ml-1">*</span>
        </label>
        <div className="relative">
          <input
            type="number"
            name={field.name}
            value={formData[field.name]}
            onChange={handleChange}
            min={field.min}
            max={field.max}
            placeholder={`${field.min} - ${field.max}`}
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              hasError ? 'border-red-500' : 'border-gray-300'
            }`}
          />
          <span className="absolute right-3 top-2 text-xs text-gray-500">
            {field.min}-{field.max}
          </span>
        </div>
        {hasError && (
          <p className="text-red-500 text-xs mt-1 flex items-center space-x-1">
            <AlertCircle size={12} />
            <span>{errors[field.name]}</span>
          </p>
        )}
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <Activity size={48} className="text-blue-600" />
        </div>
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          Stress Level Assessment
        </h1>
        <p className="text-gray-600">
          Complete all fields to get your stress level prediction
        </p>
      </div>

      {/* Info Card */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-8 rounded-lg">
        <div className="flex items-start space-x-3">
          <Info size={20} className="text-blue-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-blue-800">
            <p className="font-semibold mb-1">Assessment Information</p>
            <p>
              This assessment uses 20 factors to predict whether your stress level is Low, Moderate, or High.
              Please answer all questions honestly for the most accurate results. All fields are required.
            </p>
          </div>
        </div>
      </div>

      {/* Server Error */}
      {serverError && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-lg">
          <div className="flex items-start space-x-3">
            <AlertCircle size={20} className="text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-red-800">Error</p>
              <p className="text-sm text-red-700">{serverError}</p>
            </div>
          </div>
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="mb-8 animate-fadeIn">
          <ResultCard result={result} type="stress-level" />
          
          {/* Recommendation Card */}
          <div className="mt-6 bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
            <h3 className="text-xl font-bold text-gray-800 mb-3 flex items-center space-x-2">
              <CheckCircle className="text-blue-600" size={24} />
              <span>Recommendation</span>
            </h3>
            <p className="text-gray-700 mb-4">{result.recommendation}</p>
            <div className="text-sm text-gray-600">
              <p>Model Accuracy: <span className="font-semibold">{result.model_accuracy}%</span></p>
            </div>
          </div>

          <div className="mt-4 text-center">
            <button
              onClick={handleReset}
              className="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
            >
              Take Another Assessment
            </button>
          </div>
        </div>
      )}

      {/* Form */}
      {!result && (
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-8">
          {loading ? (
            <LoadingSpinner message="Analyzing your stress level..." />
          ) : (
            <>
              {/* Form Fields */}
              <div className="space-y-6">
                {/* Mental Health Section */}
                <div>
                  <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-blue-500">
                    Mental Health Indicators
                  </h2>
                  <div className="grid md:grid-cols-2 gap-6">
                    {STRESS_LEVEL_FIELDS.filter(f => 
                      ['anxiety_level', 'self_esteem', 'mental_health_history', 'depression'].includes(f.name)
                    ).map(renderField)}
                  </div>
                </div>

                {/* Physical Symptoms Section */}
                <div>
                  <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-green-500">
                    Physical Symptoms
                  </h2>
                  <div className="grid md:grid-cols-2 gap-6">
                    {STRESS_LEVEL_FIELDS.filter(f => 
                      ['headache', 'blood_pressure', 'sleep_quality', 'breathing_problem'].includes(f.name)
                    ).map(renderField)}
                  </div>
                </div>

                {/* Environmental Factors Section */}
                <div>
                  <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-purple-500">
                    Environmental Factors
                  </h2>
                  <div className="grid md:grid-cols-2 gap-6">
                    {STRESS_LEVEL_FIELDS.filter(f => 
                      ['noise_level', 'living_conditions', 'safety', 'basic_needs'].includes(f.name)
                    ).map(renderField)}
                  </div>
                </div>

                {/* Academic & Social Section */}
                <div>
                  <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-orange-500">
                    Academic & Social Factors
                  </h2>
                  <div className="grid md:grid-cols-2 gap-6">
                    {STRESS_LEVEL_FIELDS.filter(f => 
                      ['academic_performance', 'study_load', 'teacher_student_relationship', 
                       'future_career_concerns', 'social_support', 'peer_pressure', 
                       'extracurricular_activities', 'bullying'].includes(f.name)
                    ).map(renderField)}
                  </div>
                </div>
              </div>

              {/* Validation Error Summary */}
              {Object.keys(errors).length > 0 && (
                <div className="mt-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <AlertCircle size={20} className="text-red-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-red-800 mb-1">
                        Please fix the following errors:
                      </p>
                      <ul className="text-sm text-red-700 list-disc list-inside">
                        {Object.values(errors).slice(0, 5).map((error, index) => (
                          <li key={index}>{error}</li>
                        ))}
                        {Object.values(errors).length > 5 && (
                          <li>... and {Object.values(errors).length - 5} more</li>
                        )}
                      </ul>
                    </div>
                  </div>
                </div>
              )}

              {/* Submit Buttons */}
              <div className="mt-8 flex justify-between">
                <button
                  type="button"
                  onClick={handleReset}
                  className="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
                >
                  Reset Form
                </button>
                <button
                  type="submit"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors flex items-center space-x-2"
                >
                  <Activity size={20} />
                  <span>Get Prediction</span>
                </button>
              </div>
            </>
          )}
        </form>
      )}

      {/* Footer Note */}
      <div className="mt-6 text-center text-sm text-gray-500">
        <p>
          This assessment is for educational purposes only and should not replace professional medical advice.
        </p>
      </div>
    </div>
  )
}

export default StressLevelForm