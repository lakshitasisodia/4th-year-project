import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Brain, Home, Activity, FileText, Info } from 'lucide-react'

function Header() {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path
  
  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2 text-2xl font-bold text-blue-600">
            <Brain size={32} />
            <span>StressPredict</span>
          </Link>
          
          <div className="flex items-center space-x-6">
            <Link 
              to="/" 
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                isActive('/') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Home size={20} />
              <span>Home</span>
            </Link>
            
            <Link 
              to="/stress-level" 
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                isActive('/stress-level') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Activity size={20} />
              <span>Stress Level</span>
            </Link>
            
            <Link 
              to="/stress-type" 
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                isActive('/stress-type') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <FileText size={20} />
              <span>Stress Type</span>
            </Link>
            
            <Link 
              to="/about" 
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                isActive('/about') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Info size={20} />
              <span>About</span>
            </Link>
          </div>
        </div>
      </nav>
    </header>
  )
}

export default Header