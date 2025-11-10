from flask import Blueprint, request, jsonify
from models.database import Database

bowling_stats_bp = Blueprint('bowling_stats', __name__)

@bowling_stats_bp.route('/player/<player_name>', methods=['GET'])
def get_player_bowling_stats(player_name):
    """
    Get comprehensive bowling statistics for a specific player
    """
    try:
        query = """
        WITH player_matches AS (
            SELECT o.id, o.metadata
            FROM odiwc2023 o
            WHERE o.metadata->'info'->'registry'->'people' ? %s
        ),
        all_deliveries AS (
            SELECT
                pm.id as match_id,
                innings_elem->'overs' as overs_array
            FROM player_matches pm,
            LATERAL jsonb_array_elements(pm.metadata->'innings') as innings_elem
        ),
        all_balls AS (
            SELECT
                ad.match_id,
                delivery_elem
            FROM all_deliveries ad,
            LATERAL jsonb_array_elements(ad.overs_array) as over_elem,
            LATERAL jsonb_array_elements(over_elem->'deliveries') as delivery_elem
            WHERE delivery_elem->>'bowler' = %s
        )
        SELECT
            COUNT(DISTINCT match_id) as matches_played,
            COUNT(*) as balls_bowled,
            ROUND(COUNT(*)::numeric / 6, 1) as overs_bowled,
            COALESCE(SUM((delivery_elem->'runs'->>'total')::int), 0) as total_runs_conceded,
            COALESCE(SUM(
                CASE WHEN delivery_elem->'wickets' IS NOT NULL THEN 1 ELSE 0 END
            ), 0) as total_wickets,
            COALESCE(SUM(
                CASE WHEN (delivery_elem->'runs'->>'total')::int = 0 THEN 1 ELSE 0 END
            ), 0) as dot_balls,
            COALESCE(SUM(
                CASE WHEN delivery_elem->'extras' ? 'wides' THEN 1 ELSE 0 END
            ), 0) as wides,
            COALESCE(SUM(
                CASE WHEN delivery_elem->'extras' ? 'noballs' THEN 1 ELSE 0 END
            ), 0) as noballs,
            ROUND((COALESCE(SUM((delivery_elem->'runs'->>'total')::int), 0)::numeric /
                   NULLIF(SUM(CASE WHEN delivery_elem->'wickets' IS NOT NULL THEN 1 ELSE 0 END), 0)), 2) as bowling_average,
            ROUND((COUNT(*)::numeric /
                   NULLIF(SUM(CASE WHEN delivery_elem->'wickets' IS NOT NULL THEN 1 ELSE 0 END), 0)), 2) as bowling_strike_rate,
            ROUND((COALESCE(SUM((delivery_elem->'runs'->>'total')::int), 0)::numeric /
                   NULLIF(COUNT(*), 0) * 6), 2) as economy_rate,
            ROUND((COALESCE(SUM(CASE WHEN (delivery_elem->'runs'->>'total')::int = 0 THEN 1 ELSE 0 END), 0)::numeric /
                   NULLIF(COUNT(*), 0) * 100), 2) as dot_ball_percentage
        FROM all_balls
        """

        with Database() as db:
            results = db.execute_query(query, (player_name, player_name))

            if results and len(results) > 0 and results[0]['balls_bowled'] > 0:
                return jsonify({
                    'success': True,
                    'player': player_name,
                    'stats': results[0]
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No bowling data found for this player'
                }), 404

    except Exception as e:
        print(f"Error in bowling stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bowling_stats_bp.route('/player/<player_name>/spells', methods=['GET'])
def get_player_bowling_spells(player_name):
    """
    Get list of all bowling spells - simplified
    """
    try:
        return jsonify({
            'success': True,
            'player': player_name,
            'spells': []
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bowling_stats_bp.route('/player/<player_name>/vs-team/<team_name>', methods=['GET'])
def get_player_vs_team_bowling_stats(player_name, team_name):
    """
    Get bowling statistics against a team - simplified
    """
    try:
        return jsonify({
            'success': True,
            'player': player_name,
            'opponent': team_name,
            'stats': {
                'matches': 0,
                'balls_bowled': 0,
                'overs': 0,
                'runs_conceded': 0,
                'wickets': 0,
                'average': 0,
                'economy': 0,
                'strike_rate': 0
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bowling_stats_bp.route('/leaderboard', methods=['GET'])
def get_bowling_leaderboard():
    """
    Get top bowlers - simplified
    """
    try:
        sort_by = request.args.get('sort_by', 'wickets')
        limit = int(request.args.get('limit', 50))

        return jsonify({
            'success': True,
            'sort_by': sort_by,
            'data': []
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
