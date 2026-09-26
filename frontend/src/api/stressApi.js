import axios from 'axios'
import { API_BASE_URL } from '../utils/constants'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

export const getModelInfo = async () => {
  const response = await api.get('/model-info')
  return response.data
}

export const predictStressLevel = async (data) => {
  const response = await api.post('/predict/stress-level', data)
  return response.data
}

export const predictStressType = async (data) => {
  const response = await api.post('/predict/stress-type', data)
  return response.data
}

export const getStressLevelFeatures = async () => {
  const response = await api.get('/features/stress-level')
  return response.data
}

export const getStressTypeFeatures = async () => {
  const response = await api.get('/features/stress-type')
  return response.data
}

export default api