from flask import Blueprint, request, jsonify
from models.database import Database
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats/overview', methods=['GET'])
def get_database_overview():
    """
    Get overview statistics of the database
    """
    try:
        query = """
        SELECT
            COUNT(*) as total_matches,
            COUNT(DISTINCT metadata->'info'->>'season') as total_seasons,
            COUNT(DISTINCT metadata->'info'->>'venue') as total_venues,
            MIN(metadata->'info'->'dates'->0) as earliest_match,
            MAX(metadata->'info'->'dates'->0) as latest_match
        FROM odiwc2023
        """

        # Get team statistics
        teams_query = """
        SELECT
            jsonb_array_elements_text(metadata->'info'->'teams') as team_name,
            COUNT(*) as matches_played
        FROM odiwc2023
        GROUP BY team_name
        ORDER BY matches_played DESC
        """

        # Get total players
        players_query = """
        SELECT COUNT(DISTINCT player_name) as total_players
        FROM (
            SELECT jsonb_object_keys(metadata->'info'->'registry'->'people') as player_name
            FROM odiwc2023
        ) as players
        """

        with Database() as db:
            overview = db.execute_query(query)
            teams = db.execute_query(teams_query)
            players = db.execute_query(players_query)

            return jsonify({
                'success': True,
                'overview': overview[0] if overview else {},
                'teams': teams if teams else [],
                'total_players': players[0]['total_players'] if players else 0
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/data/validate', methods=['GET'])
def validate_data():
    """
    Validate data integrity and find issues
    """
    try:
        # Check for matches without innings data
        no_innings_query = """
        SELECT
            id,
            metadata->'info'->'dates'->0 as match_date,
            metadata->'info'->>'venue' as venue
        FROM odiwc2023
        WHERE metadata->'innings' IS NULL
            OR jsonb_array_length(metadata->'innings') = 0
        LIMIT 10
        """

        # Check for matches without outcome
        no_outcome_query = """
        SELECT
            id,
            metadata->'info'->'dates'->0 as match_date,
            metadata->'info'->>'venue' as venue
        FROM odiwc2023
        WHERE metadata->'info'->'outcome' IS NULL
        LIMIT 10
        """

        # Check for matches with incomplete metadata
        incomplete_query = """
        SELECT
            id,
            CASE WHEN metadata->'info'->>'venue' IS NULL THEN 'Missing venue' ELSE NULL END as issue
        FROM odiwc2023
        WHERE metadata->'info'->>'venue' IS NULL
        LIMIT 10
        """

        with Database() as db:
            no_innings = db.execute_query(no_innings_query)
            no_outcome = db.execute_query(no_outcome_query)
            incomplete = db.execute_query(incomplete_query)

            issues = {
                'matches_without_innings': len(no_innings) if no_innings else 0,
                'matches_without_outcome': len(no_outcome) if no_outcome else 0,
                'matches_with_incomplete_data': len(incomplete) if incomplete else 0
            }

            return jsonify({
                'success': True,
                'validation': issues,
                'samples': {
                    'no_innings': no_innings[:5] if no_innings else [],
                    'no_outcome': no_outcome[:5] if no_outcome else [],
                    'incomplete': incomplete[:5] if incomplete else []
                }
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/data/export', methods=['POST'])
def export_data():
    """
    Export filtered data based on criteria
    """
    try:
        data = request.get_json()
        team = data.get('team', '')
        season = data.get('season', '')
        date_from = data.get('date_from', '')
        date_to = data.get('date_to', '')

        query = "SELECT metadata FROM odiwc2023 WHERE 1=1"
        params = []

        if team:
            query += " AND metadata->'info'->'teams' @> %s"
            params.append(f'["{team}"]')

        if season:
            query += " AND metadata->'info'->>'season' = %s"
            params.append(season)

        if date_from:
            query += " AND metadata->'info'->'dates'->0 >= %s"
            params.append(f'"{date_from}"')

        if date_to:
            query += " AND metadata->'info'->'dates'->0 <= %s"
            params.append(f'"{date_to}"')

        query += " LIMIT 1000"  # Limit export size

        with Database() as db:
            results = db.execute_query(query, params)

            if results:
                # Extract metadata from results
                export_data = [row['metadata'] for row in results]
                return jsonify({
                    'success': True,
                    'count': len(export_data),
                    'data': export_data
                })
            else:
                return jsonify({
                    'success': True,
                    'count': 0,
                    'data': []
                })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """
    Clear application cache (placeholder for future caching implementation)
    """
    try:
        # This is a placeholder for when caching is implemented
        return jsonify({
            'success': True,
            'message': 'Cache cleared successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/logs', methods=['GET'])
def get_logs():
    """
    Get application logs (placeholder)
    """
    try:
        # This is a placeholder for logging functionality
        return jsonify({
            'success': True,
            'logs': []
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
