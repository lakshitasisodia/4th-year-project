import React from 'react'
import { Heart, Github, Mail } from 'lucide-react'

function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-8 mt-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">StressPredict</h3>
            <p className="text-gray-300">
              AI-powered student stress prediction system using machine learning
            </p>
          </div>
          
          <div>
            <h3 className="text-xl font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="/" className="text-gray-300 hover:text-white transition-colors">Home</a></li>
              <li><a href="/stress-level" className="text-gray-300 hover:text-white transition-colors">Stress Level Test</a></li>
              <li><a href="/stress-type" className="text-gray-300 hover:text-white transition-colors">Stress Type Test</a></li>
              <li><a href="/about" className="text-gray-300 hover:text-white transition-colors">About</a></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-bold mb-4">Contact</h3>
            <div className="flex flex-col space-y-2">
              <a href="mailto:support@stresspredict.com" className="flex items-center space-x-2 text-gray-300 hover:text-white transition-colors">
                <Mail size={18} />
                <span>support@stresspredict.com</span>
              </a>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="flex items-center space-x-2 text-gray-300 hover:text-white transition-colors">
                <Github size={18} />
                <span>GitHub</span>
              </a>
            </div>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-6 text-center text-gray-400">
          <p className="flex items-center justify-center space-x-2">
            <span>Made with</span>
            <Heart size={18} className="text-red-500 fill-current" />
            <span>for Student Wellbeing</span>
          </p>
          <p className="mt-2">© 2024 StressPredict. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer