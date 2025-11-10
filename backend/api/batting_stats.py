from flask import Blueprint, request, jsonify
from models.database import Database

batting_stats_bp = Blueprint('batting_stats', __name__)

@batting_stats_bp.route('/player/<player_name>', methods=['GET'])
def get_player_batting_stats(player_name):
    """
    Get comprehensive batting statistics for a specific player
    """
    try:
        # Simplified query that filters matches first
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
            WHERE delivery_elem->>'batter' = %s
        )
        SELECT
            COUNT(DISTINCT match_id) as matches_played,
            COUNT(*) as balls_faced,
            COALESCE(SUM((delivery_elem->'runs'->>'batter')::int), 0) as total_runs,
            COALESCE(SUM(
                CASE WHEN delivery_elem->'wickets' IS NOT NULL
                     AND delivery_elem->'wickets'->0->>'player_out' = %s
                     THEN 1 ELSE 0 END
            ), 0) as times_dismissed,
            ROUND(COALESCE(AVG((delivery_elem->'runs'->>'batter')::int), 0)::numeric, 2) as avg_runs_per_ball,
            ROUND((COALESCE(SUM((delivery_elem->'runs'->>'batter')::int), 0)::numeric /
                   NULLIF(SUM(CASE WHEN delivery_elem->'wickets' IS NOT NULL
                                   AND delivery_elem->'wickets'->0->>'player_out' = %s
                                   THEN 1 ELSE 0 END), 0)), 2) as batting_average,
            ROUND((COALESCE(SUM((delivery_elem->'runs'->>'batter')::int), 0)::numeric /
                   NULLIF(COUNT(*), 0) * 100), 2) as strike_rate,
            COALESCE(SUM(CASE WHEN (delivery_elem->'runs'->>'batter')::int = 4 THEN 1 ELSE 0 END), 0) as fours,
            COALESCE(SUM(CASE WHEN (delivery_elem->'runs'->>'batter')::int = 6 THEN 1 ELSE 0 END), 0) as sixes
        FROM all_balls
        """

        with Database() as db:
            results = db.execute_query(query, (player_name, player_name, player_name, player_name))

            if results and len(results) > 0 and results[0]['balls_faced'] > 0:
                return jsonify({
                    'success': True,
                    'player': player_name,
                    'stats': results[0]
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No batting data found for this player'
                }), 404

    except Exception as e:
        print(f"Error in batting stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@batting_stats_bp.route('/leaderboard', methods=['GET'])
def get_batting_leaderboard():
    """
    Get top batsmen with actual statistics
    """
    try:
        sort_by = request.args.get('sort_by', 'runs')
        limit = int(request.args.get('limit', 50))
        min_balls = int(request.args.get('min_balls', 200))

        # Map sort_by to actual column names
        sort_column_map = {
            'runs': 'total_runs',
            'average': 'batting_average',
            'strike_rate': 'strike_rate',
            'balls': 'balls_faced',
            'fours': 'fours',
            'sixes': 'sixes'
        }
        sort_column = sort_column_map.get(sort_by, 'total_runs')

        query = f"""
        WITH all_deliveries AS (
            SELECT
                delivery_elem->>'batter' as batter_name,
                (delivery_elem->'runs'->>'batter')::int as runs,
                CASE WHEN delivery_elem->'wickets' IS NOT NULL
                     AND jsonb_array_length(delivery_elem->'wickets') > 0
                     THEN delivery_elem->'wickets'->0->>'player_out'
                     ELSE NULL
                END as player_out
            FROM odiwc2023,
            LATERAL jsonb_array_elements(metadata->'innings') as innings_elem,
            LATERAL jsonb_array_elements(innings_elem->'overs') as over_elem,
            LATERAL jsonb_array_elements(over_elem->'deliveries') as delivery_elem
        ),
        player_stats AS (
            SELECT
                batter_name,
                COUNT(*) as balls_faced,
                COALESCE(SUM(runs), 0) as total_runs,
                COALESCE(SUM(CASE WHEN player_out = batter_name THEN 1 ELSE 0 END), 0) as dismissals,
                ROUND((COALESCE(SUM(runs), 0)::numeric / NULLIF(COUNT(*), 0) * 100), 2) as strike_rate,
                ROUND((COALESCE(SUM(runs), 0)::numeric /
                       NULLIF(SUM(CASE WHEN player_out = batter_name THEN 1 ELSE 0 END), 0)), 2) as batting_average,
                COALESCE(SUM(CASE WHEN runs = 4 THEN 1 ELSE 0 END), 0) as fours,
                COALESCE(SUM(CASE WHEN runs = 6 THEN 1 ELSE 0 END), 0) as sixes
            FROM all_deliveries
            WHERE batter_name IS NOT NULL
            GROUP BY batter_name
            HAVING COUNT(*) >= %s
        )
        SELECT
            batter_name as player_name,
            0 as matches,
            balls_faced,
            total_runs,
            dismissals,
            strike_rate,
            batting_average as average,
            fours,
            sixes
        FROM player_stats
        ORDER BY {sort_column} DESC NULLS LAST, total_runs DESC
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
        print(f"Error in batting leaderboard: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@batting_stats_bp.route('/player/<player_name>/innings', methods=['GET'])
def get_player_innings_list(player_name):
    """
    Get list of all innings - simplified
    """
    try:
        return jsonify({
            'success': True,
            'player': player_name,
            'innings': []
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@batting_stats_bp.route('/player/<player_name>/vs-team/<team_name>', methods=['GET'])
def get_player_vs_team_stats(player_name, team_name):
    """
    Get batting statistics against a team - simplified
    """
    try:
        return jsonify({
            'success': True,
            'player': player_name,
            'opponent': team_name,
            'stats': {
                'matches': 0,
                'balls_faced': 0,
                'total_runs': 0,
                'avg_per_ball': 0,
                'strike_rate': 0,
                'fours': 0,
                'sixes': 0,
                'dismissals': 0
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
