from flask import Blueprint, request, jsonify
from models.database import Database

player_profile_bp = Blueprint('player_profile', __name__)

@player_profile_bp.route('/<player_name>', methods=['GET'])
def get_player_profile(player_name):
    """
    Get detailed player profile from cleaned_all_players table
    """
    try:
        query = """
        SELECT
            fullname,
            image_path,
            dateofbirth,
            gender,
            battingstyle,
            bowlingstyle,
            position,
            country_name,
            country_image_path,
            continent_name
        FROM cleaned_all_players
        WHERE fullname = %s
        LIMIT 1
        """

        with Database() as db:
            results = db.execute_query(query, (player_name,))

            if results and len(results) > 0:
                return jsonify({
                    'success': True,
                    'player': results[0]
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Player profile not found'
                }), 404

    except Exception as e:
        print(f"Error in player profile: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@player_profile_bp.route('/search', methods=['GET'])
def search_players():
    """
    Search for players by name
    """
    try:
        search_term = request.args.get('q', '')
        limit = int(request.args.get('limit', 20))

        query = """
        SELECT
            fullname,
            country_name,
            battingstyle,
            bowlingstyle,
            image_path
        FROM cleaned_all_players
        WHERE fullname ILIKE %s
        ORDER BY fullname
        LIMIT %s
        """

        with Database() as db:
            results = db.execute_query(query, (f'%{search_term}%', limit))

            return jsonify({
                'success': True,
                'players': results if results else []
            })

    except Exception as e:
        print(f"Error searching players: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
