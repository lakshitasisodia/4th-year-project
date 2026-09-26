import React from 'react'
import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  TrendingUp,
  TrendingDown,
  Activity
} from 'lucide-react'

function ResultCard({ result, type }) {
  const getStressLevelConfig = (level) => {
    switch (level) {
      case 'Low Stress':
        return {
          icon: CheckCircle,
          color: 'text-green-600',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200'
        }
      case 'Moderate Stress':
        return {
          icon: AlertTriangle,
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200'
        }
      case 'High Stress':
        return {
          icon: XCircle,
          color: 'text-red-600',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200'
        }
      default:
        return {
          icon: Activity,
          color: 'text-gray-600',
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-200'
        }
    }
  }

  const getStressTypeConfig = (stressType) => {
    switch (stressType) {
      case 'Distress':
        return {
          icon: TrendingDown,
          color: 'text-red-600',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200'
        }
      case 'Eustress':
        return {
          icon: TrendingUp,
          color: 'text-green-600',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200'
        }
      case 'No Stress':
        return {
          icon: CheckCircle,
          color: 'text-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200'
        }
      default:
        return {
          icon: Activity,
          color: 'text-gray-600',
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-200'
        }
    }
  }

  /* ================= STRESS LEVEL CARD ================= */
  if (type === 'stress-level') {
    const config = getStressLevelConfig(result.stress_level)
    const Icon = config.icon

    return (
      <div className={`card ${config.bgColor} border-2 ${config.borderColor}`}>
        <div className="flex items-center space-x-4 mb-6">
          <Icon className={config.color} size={48} />
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              {result.stress_level}
            </h2>
            <p className="text-gray-600">Prediction Result</p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-white rounded-lg shadow-sm">
            <p className="text-sm text-gray-600 mb-1">Low</p>
            <p className="text-2xl font-bold text-green-600">
              {result.confidence.low}%
            </p>
          </div>

          <div className="text-center p-4 bg-white rounded-lg shadow-sm">
            <p className="text-sm text-gray-600 mb-1">Moderate</p>
            <p className="text-2xl font-bold text-yellow-600">
              {result.confidence.moderate}%
            </p>
          </div>

          <div className="text-center p-4 bg-white rounded-lg shadow-sm">
            <p className="text-sm text-gray-600 mb-1">High</p>
            <p className="text-2xl font-bold text-red-600">
              {result.confidence.high}%
            </p>
          </div>
        </div>
      </div>
    )
  }

  /* ================= STRESS TYPE CARD ================= */
  if (type === 'stress-type') {
    const config = getStressTypeConfig(result.stress_type)
    const Icon = config.icon

    return (
      <div className={`card ${config.bgColor} border-2 ${config.borderColor}`}>
        <div className="flex items-center space-x-4">
          <Icon className={config.color} size={48} />
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              {result.stress_type}
            </h2>
            <p className="text-gray-600">Stress Classification</p>
          </div>
        </div>
      </div>
    )
  }

  return null
}

export default ResultCard
