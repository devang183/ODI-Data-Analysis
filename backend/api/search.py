from flask import Blueprint, request, jsonify
from models.database import Database

search_bp = Blueprint('search', __name__)

@search_bp.route('/matches', methods=['GET'])
def search_matches():
    """
    Search matches with various filters
    Query params: team, venue, date_from, date_to, player, season, match_type
    """
    try:
        # Get query parameters
        team = request.args.get('team', '')
        venue = request.args.get('venue', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        player = request.args.get('player', '')
        season = request.args.get('season', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        offset = (page - 1) * limit

        # Build query
        query = """
            SELECT
                id,
                metadata->'info'->>'match_type_number' as match_number,
                metadata->'info'->>'venue' as venue,
                metadata->'info'->>'city' as city,
                metadata->'info'->'dates'->0 as match_date,
                metadata->'info'->'teams' as teams,
                metadata->'info'->'outcome'->>'winner' as winner,
                metadata->'info'->'outcome'->'by' as win_margin,
                metadata->'info'->>'season' as season,
                metadata->'info'->'player_of_match' as player_of_match,
                metadata->'info'->'event'->>'name' as event_name
            FROM odiwc2023
            WHERE 1=1
        """

        params = []

        if team:
            query += " AND (metadata->'info'->'teams' @> %s)"
            params.append(f'["{team}"]')

        if venue:
            query += " AND LOWER(metadata->'info'->>'venue') LIKE LOWER(%s)"
            params.append(f'%{venue}%')

        if date_from:
            query += " AND metadata->'info'->'dates'->0 >= %s"
            params.append(f'"{date_from}"')

        if date_to:
            query += " AND metadata->'info'->'dates'->0 <= %s"
            params.append(f'"{date_to}"')

        if player:
            query += """ AND (
                metadata->'info'->'players' @> %s
                OR metadata->'info'->'player_of_match' @> %s
            )"""
            params.extend([f'{{"{player}": []}}', f'["{player}"]'])

        if season:
            query += " AND metadata->'info'->>'season' = %s"
            params.append(season)

        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM ({query}) as filtered"

        # Add pagination
        query += " ORDER BY metadata->'info'->'dates'->0 DESC"
        query += f" LIMIT {limit} OFFSET {offset}"

        with Database() as db:
            # Get total count
            total_results = db.execute_query(count_query, params)
            total = total_results[0]['total'] if total_results else 0

            # Get paginated results
            results = db.execute_query(query, params)

            return jsonify({
                'success': True,
                'data': results if results else [],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': total,
                    'pages': (total + limit - 1) // limit
                }
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/players', methods=['GET'])
def search_players():
    """Get list of all unique players"""
    try:
        query = """
            SELECT DISTINCT jsonb_object_keys(metadata->'info'->'registry'->'people') as player_name
            FROM odiwc2023
            ORDER BY player_name
        """

        with Database() as db:
            results = db.execute_query(query)
            players = [row['player_name'] for row in results] if results else []

            return jsonify({
                'success': True,
                'data': players
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/teams', methods=['GET'])
def search_teams():
    """Get list of all unique teams"""
    try:
        query = """
            SELECT DISTINCT jsonb_array_elements_text(metadata->'info'->'teams') as team_name
            FROM odiwc2023
            ORDER BY team_name
        """

        with Database() as db:
            results = db.execute_query(query)
            teams = [row['team_name'] for row in results] if results else []

            return jsonify({
                'success': True,
                'data': teams
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/venues', methods=['GET'])
def search_venues():
    """Get list of all unique venues"""
    try:
        query = """
            SELECT DISTINCT metadata->'info'->>'venue' as venue
            FROM odiwc2023
            WHERE metadata->'info'->>'venue' IS NOT NULL
            ORDER BY venue
        """

        with Database() as db:
            results = db.execute_query(query)
            venues = [row['venue'] for row in results] if results else []

            return jsonify({
                'success': True,
                'data': venues
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/seasons', methods=['GET'])
def search_seasons():
    """Get list of all unique seasons"""
    try:
        query = """
            SELECT DISTINCT metadata->'info'->>'season' as season
            FROM odiwc2023
            WHERE metadata->'info'->>'season' IS NOT NULL
            ORDER BY season DESC
        """

        with Database() as db:
            results = db.execute_query(query)
            seasons = [row['season'] for row in results] if results else []

            return jsonify({
                'success': True,
                'data': seasons
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/match/<match_id>', methods=['GET'])
def get_match_details(match_id):
    """Get complete details of a specific match"""
    try:
        query = """
            SELECT id, metadata
            FROM odiwc2023
            WHERE id = %s
        """

        with Database() as db:
            results = db.execute_query(query, (match_id,))

            if results and len(results) > 0:
                return jsonify({
                    'success': True,
                    'data': results[0]
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Match not found'
                }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
