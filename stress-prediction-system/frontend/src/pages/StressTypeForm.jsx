import React, { useState } from 'react'
import { FileText, AlertCircle, CheckCircle, Info } from 'lucide-react'
import { predictStressType } from '../api/stressApi'
import { validateStressTypeInput } from '../utils/validators'
import { STRESS_TYPE_FIELDS, SCALE_LABELS } from '../utils/constants'
import LoadingSpinner from '../components/LoadingSpinner'
import ResultCard from '../components/ResultCard'

function StressTypeForm() {
  const [formData, setFormData] = useState(() => {
    const initialData = {}
    STRESS_TYPE_FIELDS.forEach(field => {
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
    
    // Clear error for this field
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
    const validation = validateStressTypeInput(formData)
    
    if (!validation.isValid) {
      setErrors(validation.errors)
      window.scrollTo({ top: 0, behavior: 'smooth' })
      return
    }
    
    setErrors({})
    setLoading(true)
    
    try {
      const response = await predictStressType(formData)
      
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
    STRESS_TYPE_FIELDS.forEach(field => {
      resetData[field.name] = ''
    })
    setFormData(resetData)
    setErrors({})
    setResult(null)
    setServerError(null)
  }

  const renderField = (field) => {
    const hasError = errors[field.name]
    
    // Demographics fields (Gender and Age)
    if (field.name === 'Gender') {
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
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
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
    
    if (field.name === 'Age') {
      return (
        <div key={field.name} className="space-y-2">
          <label className="block text-sm font-semibold text-gray-700">
            {field.label}
            <span className="text-red-500 ml-1">*</span>
          </label>
          <input
            type="number"
            name={field.name}
            value={formData[field.name]}
            onChange={handleChange}
            min={field.min}
            max={field.max}
            placeholder={`${field.min} - ${field.max}`}
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
              hasError ? 'border-red-500' : 'border-gray-300'
            }`}
          />
          {hasError && (
            <p className="text-red-500 text-xs mt-1 flex items-center space-x-1">
              <AlertCircle size={12} />
              <span>{errors[field.name]}</span>
            </p>
          )}
        </div>
      )
    }
    
    // Likert scale questions
    return (
      <div key={field.name} className="space-y-3 p-4 bg-gray-50 rounded-lg">
        <label className="block text-sm font-semibold text-gray-700">
          {field.label}
          <span className="text-red-500 ml-1">*</span>
        </label>
        
        <div className="flex justify-between items-center space-x-2">
          {[1, 2, 3, 4, 5].map(value => (
            <label
              key={value}
              className={`flex-1 text-center cursor-pointer transition-all ${
                formData[field.name] === value
                  ? 'bg-purple-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-purple-100'
              } border-2 ${
                hasError ? 'border-red-500' : 'border-gray-300'
              } rounded-lg p-3`}
            >
              <input
                type="radio"
                name={field.name}
                value={value}
                checked={formData[field.name] === value}
                onChange={handleChange}
                className="sr-only"
              />
              <div className="font-bold text-lg mb-1">{value}</div>
              <div className="text-xs">{SCALE_LABELS[value]}</div>
            </label>
          ))}
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
          <FileText size={48} className="text-purple-600" />
        </div>
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          Stress Type Assessment
        </h1>
        <p className="text-gray-600">
          Identify whether you're experiencing distress, eustress, or no stress
        </p>
      </div>

      {/* Info Card */}
      <div className="bg-purple-50 border-l-4 border-purple-500 p-4 mb-8 rounded-lg">
        <div className="flex items-start space-x-3">
          <Info size={20} className="text-purple-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-purple-800">
            <p className="font-semibold mb-1">Assessment Information</p>
            <p>
              This assessment classifies your stress into three types: <strong>Distress</strong> (negative stress), 
              <strong> Eustress</strong> (positive/motivating stress), or <strong>No Stress</strong>. 
              Answer all questions using the 1-5 scale where 1 = Never and 5 = Always.
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
          <ResultCard result={result} type="stress-type" />
          
          {/* Detailed Results */}
          <div className="mt-6 bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">
              Detailed Analysis
            </h3>
            
            <div className="grid md:grid-cols-3 gap-4 mb-6">
              <div className="text-center p-4 bg-red-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Distress</p>
                <p className="text-3xl font-bold text-red-600">
                  {result.probabilities.distress}%
                </p>
              </div>
              
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Eustress</p>
                <p className="text-3xl font-bold text-green-600">
                  {result.probabilities.eustress}%
                </p>
              </div>
              
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">No Stress</p>
                <p className="text-3xl font-bold text-blue-600">
                  {result.probabilities.no_stress}%
                </p>
              </div>
            </div>

            <div className="border-t pt-4">
              <div className="flex items-start space-x-3">
                <CheckCircle className="text-purple-600 flex-shrink-0 mt-1" size={24} />
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Recommendation</h4>
                  <p className="text-gray-700 mb-3">{result.recommendation}</p>
                  <p className="text-sm text-gray-600">
                    Model Accuracy: <span className="font-semibold">{result.model_accuracy}%</span>
                  </p>
                </div>
              </div>
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
            <LoadingSpinner message="Analyzing your stress type..." />
          ) : (
            <>
              {/* Demographics Section */}
              <div className="mb-8">
                <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-purple-500">
                  Demographics
                </h2>
                <div className="grid md:grid-cols-2 gap-6">
                  {STRESS_TYPE_FIELDS.filter(f => 
                    ['Gender', 'Age'].includes(f.name)
                  ).map(renderField)}
                </div>
              </div>

              {/* Stress Experience Section */}
              <div className="mb-8">
                <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-red-500">
                  Stress Experience & Physical Symptoms
                </h2>
                <div className="space-y-4">
                  {STRESS_TYPE_FIELDS.filter(f => 
                    f.type === 'scale' && [
                      'Have you recently experienced stress in your life?',
                      'Have you noticed a rapid heartbeat or palpitations?',
                      'Have you been dealing with anxiety or tension recently?',
                      'Do you face any sleep problems or difficulties falling asleep?',
                      'Have you been dealing with anxiety or tension recently?.1',
                      'Have you been getting headaches more often than usual?'
                    ].includes(f.name)
                  ).map(renderField)}
                </div>
              </div>

              {/* Emotional & Behavioral Section */}
              <div className="mb-8">
                <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-blue-500">
                  Emotional & Behavioral Indicators
                </h2>
                <div className="space-y-4">
                  {STRESS_TYPE_FIELDS.filter(f => 
                    f.type === 'scale' && [
                      'Do you get irritated easily?',
                      'Do you have trouble concentrating on your academic tasks?',
                      'Have you been feeling sadness or low mood?',
                      'Have you been experiencing any illness or health issues?',
                      'Do you often feel lonely or isolated?',
                      'Have you gained/lost weight?'
                    ].includes(f.name)
                  ).map(renderField)}
                </div>
              </div>

              {/* Academic & Environmental Section */}
              <div className="mb-8">
                <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-green-500">
                  Academic & Environmental Factors
                </h2>
                <div className="space-y-4">
                  {STRESS_TYPE_FIELDS.filter(f => 
                    f.type === 'scale' && [
                      'Do you feel overwhelmed with your academic workload?',
                      'Are you in competition with your peers, and does it affect you?',
                      'Do you find that your relationship often causes you stress?',
                      'Are you facing any difficulties with your professors or instructors?',
                      'Is your working environment unpleasant or stressful?',
                      'Do you struggle to find time for relaxation and leisure activities?',
                      'Is your hostel or home environment causing you difficulties?',
                      'Do you lack confidence in your academic performance?',
                      'Do you lack confidence in your choice of academic subjects?',
                      'Academic and extracurricular activities conflicting for you?',
                      'Do you attend classes regularly?'
                    ].includes(f.name)
                  ).map(renderField)}
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
                  className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors flex items-center space-x-2"
                >
                  <FileText size={20} />
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

export default StressTypeForm