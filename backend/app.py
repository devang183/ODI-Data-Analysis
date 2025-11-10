from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import API blueprints
from api.search import search_bp
from api.phase_performance import phase_performance_bp
from api.dismissal_patterns import dismissal_patterns_bp
from api.batting_stats import batting_stats_bp
from api.bowling_stats import bowling_stats_bp
from api.vs_bowler import vs_bowler_bp
from api.motm import motm_bp
from api.admin import admin_bp
from api.player_profile import player_profile_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(search_bp, url_prefix='/api/search')
app.register_blueprint(phase_performance_bp, url_prefix='/api/phase-performance')
app.register_blueprint(dismissal_patterns_bp, url_prefix='/api/dismissal-patterns')
app.register_blueprint(batting_stats_bp, url_prefix='/api/batting-stats')
app.register_blueprint(bowling_stats_bp, url_prefix='/api/bowling-stats')
app.register_blueprint(vs_bowler_bp, url_prefix='/api/vs-bowler')
app.register_blueprint(motm_bp, url_prefix='/api/motm')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(player_profile_bp, url_prefix='/api/player-profile')

@app.route('/')
def home():
    return jsonify({
        'message': 'ODI Cricket Analytics API',
        'version': '1.0.0',
        'endpoints': {
            'search': '/api/search',
            'phase_performance': '/api/phase-performance',
            'dismissal_patterns': '/api/dismissal-patterns',
            'batting_stats': '/api/batting-stats',
            'bowling_stats': '/api/bowling-stats',
            'vs_bowler': '/api/vs-bowler',
            'motm': '/api/motm',
            'admin': '/api/admin',
            'player_profile': '/api/player-profile'
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'odi-analytics-api'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
