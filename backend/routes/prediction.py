from flask import Blueprint, request, jsonify
from models.predictor import StressPredictor
from utils.validator import InputValidator

prediction_bp = Blueprint('prediction', __name__)
predictor = StressPredictor()
validator = InputValidator()

@prediction_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Stress prediction API is running'
    }), 200

@prediction_bp.route('/model-info', methods=['GET'])
def model_info():
    try:
        info = predictor.get_model_info()
        return jsonify({
            'success': True,
            'data': info
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prediction_bp.route('/predict/stress-level', methods=['POST'])
def predict_stress_level():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No input data provided'
            }), 400
        
        is_valid, errors = validator.validate_d1_input(data)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        result = predictor.predict_stress_level(data)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prediction_bp.route('/predict/stress-type', methods=['POST'])
def predict_stress_type():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No input data provided'
            }), 400
        
        is_valid, errors = validator.validate_d2_input(data)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        result = predictor.predict_stress_type(data)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prediction_bp.route('/features/stress-level', methods=['GET'])
def get_stress_level_features():
    from config import Config
    return jsonify({
        'success': True,
        'features': Config.D1_FEATURES,
        'field_ranges': Config.FIELD_RANGES
    }), 200

@prediction_bp.route('/features/stress-type', methods=['GET'])
def get_stress_type_features():
    from config import Config
    return jsonify({
        'success': True,
        'features': Config.D2_FEATURES
    }), 200