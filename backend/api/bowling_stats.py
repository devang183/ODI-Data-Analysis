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
            (FLOOR(COUNT(*) / 6) + MOD(COUNT(*), 6)::numeric / 10) as overs_bowled,
            COALESCE(SUM((delivery_elem->'runs'->>'total')::int), 0) as total_runs_conceded,
            COALESCE(SUM(
                CASE WHEN delivery_elem->'wickets' IS NOT NULL
                     AND delivery_elem->'wickets'->0->>'kind' NOT IN ('run out', 'retired hurt', 'obstructing the field')
                     THEN 1 ELSE 0 END
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
    Get top bowlers leaderboard
    Query params: sort_by (wickets, average, economy, strike_rate), limit
    """
    try:
        sort_by = request.args.get('sort_by', 'wickets')
        limit = int(request.args.get('limit', 50))
        min_balls = int(request.args.get('min_balls', 50))

        # Map sort_by to actual column names
        sort_column_map = {
            'wickets': 'total_wickets',
            'average': 'bowling_average',
            'economy': 'economy_rate',
            'strike_rate': 'bowling_strike_rate',
            'matches': 'matches_played',
            'overs': 'overs_bowled'
        }
        sort_column = sort_column_map.get(sort_by, 'total_wickets')

        query = f"""
        WITH all_deliveries AS (
            SELECT
                delivery_elem->>'bowler' as bowler_name,
                o.id as match_id,
                (delivery_elem->'runs'->>'total')::int as runs_total,
                CASE WHEN delivery_elem->'wickets' IS NOT NULL
                     AND delivery_elem->'wickets'->0->>'kind' NOT IN ('run out', 'retired hurt', 'obstructing the field')
                     THEN 1 ELSE 0 END as is_wicket,
                CASE WHEN (delivery_elem->'runs'->>'total')::int = 0 THEN 1 ELSE 0 END as is_dot
            FROM odiwc2023 o,
            LATERAL jsonb_array_elements(o.metadata->'innings') as innings_elem,
            LATERAL jsonb_array_elements(innings_elem->'overs') as over_elem,
            LATERAL jsonb_array_elements(over_elem->'deliveries') as delivery_elem
            WHERE delivery_elem->>'bowler' IS NOT NULL
        ),
        bowler_stats AS (
            SELECT
                bowler_name,
                COUNT(DISTINCT match_id) as matches_played,
                COUNT(*) as balls_bowled,
                (FLOOR(COUNT(*) / 6) + MOD(COUNT(*), 6)::numeric / 10) as overs_bowled,
                COALESCE(SUM(runs_total), 0) as total_runs_conceded,
                COALESCE(SUM(is_wicket), 0) as total_wickets,
                COALESCE(SUM(is_dot), 0) as dot_balls,
                ROUND((COALESCE(SUM(runs_total), 0)::numeric /
                       NULLIF(SUM(is_wicket), 0)), 2) as bowling_average,
                ROUND((COUNT(*)::numeric /
                       NULLIF(SUM(is_wicket), 0)), 2) as bowling_strike_rate,
                ROUND((COALESCE(SUM(runs_total), 0)::numeric /
                       NULLIF(COUNT(*), 0) * 6), 2) as economy_rate,
                ROUND((COALESCE(SUM(is_dot), 0)::numeric /
                       NULLIF(COUNT(*), 0) * 100), 2) as dot_ball_percentage
            FROM all_deliveries
            WHERE bowler_name IS NOT NULL
            GROUP BY bowler_name
            HAVING COUNT(*) >= %s
                AND SUM(is_wicket) > 0
                AND COUNT(DISTINCT match_id) >= 80
        )
        SELECT
            bowler_name as player_name,
            matches_played,
            overs_bowled,
            total_wickets as wickets,
            total_runs_conceded as runs_conceded,
            bowling_average as average,
            economy_rate as economy,
            bowling_strike_rate as strike_rate,
            dot_ball_percentage
        FROM bowler_stats
        ORDER BY {sort_column} {'ASC' if sort_by in ['average', 'economy', 'strike_rate'] else 'DESC'}
        LIMIT %s
        """

        with Database() as db:
            results = db.execute_query(query, (min_balls, limit))

            return jsonify({
                'success': True,
                'sort_by': sort_by,
                'data': results if results else []
            })

    except Exception as e:
        print(f"Error in bowling leaderboard: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
