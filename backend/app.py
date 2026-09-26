from flask import Flask, jsonify
from flask_cors import CORS
from routes.prediction import prediction_bp
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    app.register_blueprint(prediction_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Stress Prediction API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'model_info': '/api/model-info',
                'predict_stress_level': '/api/predict/stress-level',
                'predict_stress_type': '/api/predict/stress-type',
                'get_stress_level_features': '/api/features/stress-level',
                'get_stress_type_features': '/api/features/stress-type'
            }
        }), 200
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)