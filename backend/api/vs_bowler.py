from flask import Blueprint, request, jsonify
from models.database import Database

vs_bowler_bp = Blueprint('vs_bowler', __name__)

@vs_bowler_bp.route('/batter/<batter_name>/bowler/<bowler_name>', methods=['GET'])
def get_batter_vs_bowler(batter_name, bowler_name):
    """
    Get head-to-head statistics between a batter and bowler
    """
    try:
        query = """
        WITH player_matches AS (
            SELECT o.id, o.metadata
            FROM odiwc2023 o
            WHERE o.metadata->'info'->'registry'->'people' ? %s
              AND o.metadata->'info'->'registry'->'people' ? %s
        ),
        all_deliveries AS (
            SELECT
                pm.id as match_id,
                pm.metadata->'info'->'dates'->0 as match_date,
                pm.metadata->'info'->>'venue' as venue,
                pm.metadata->'info'->'teams' as teams,
                innings_elem->>'team' as batting_team,
                innings_elem->'overs' as overs_array
            FROM player_matches pm,
            LATERAL jsonb_array_elements(pm.metadata->'innings') as innings_elem
        ),
        all_balls AS (
            SELECT
                ad.match_id,
                ad.match_date,
                ad.venue,
                ad.teams,
                ad.batting_team,
                delivery_elem
            FROM all_deliveries ad,
            LATERAL jsonb_array_elements(ad.overs_array) as over_elem,
            LATERAL jsonb_array_elements(over_elem->'deliveries') as delivery_elem
            WHERE delivery_elem->>'batter' = %s
              AND delivery_elem->>'bowler' = %s
        )
        SELECT
            COUNT(DISTINCT match_id) as matches,
            COUNT(*) as balls_faced,
            COALESCE(SUM((delivery_elem->'runs'->>'batter')::int), 0) as runs_scored,
            COALESCE(SUM(
                CASE WHEN delivery_elem->'wickets' IS NOT NULL
                     AND delivery_elem->'wickets'->0->>'player_out' = %s
                     THEN 1 ELSE 0 END
            ), 0) as dismissals,
            ROUND((COALESCE(SUM((delivery_elem->'runs'->>'batter')::int), 0)::numeric /
                   NULLIF(COUNT(*), 0) * 100), 2) as strike_rate,
            ROUND((COALESCE(SUM((delivery_elem->'runs'->>'batter')::int), 0)::numeric /
                   NULLIF(SUM(CASE WHEN delivery_elem->'wickets' IS NOT NULL
                                   AND delivery_elem->'wickets'->0->>'player_out' = %s
                                   THEN 1 ELSE 0 END), 0)), 2) as average,
            COALESCE(SUM(CASE WHEN (delivery_elem->'runs'->>'batter')::int = 4 THEN 1 ELSE 0 END), 0) as fours,
            COALESCE(SUM(CASE WHEN (delivery_elem->'runs'->>'batter')::int = 6 THEN 1 ELSE 0 END), 0) as sixes,
            COALESCE(SUM(CASE WHEN (delivery_elem->'runs'->>'batter')::int = 0 THEN 1 ELSE 0 END), 0) as dots
        FROM all_balls
        """

        # Get detailed encounters
        encounters_query = """
        WITH player_matches AS (
            SELECT o.id, o.metadata
            FROM odiwc2023 o
            WHERE o.metadata->'info'->'registry'->'people' ? %s
              AND o.metadata->'info'->'registry'->'people' ? %s
        ),
        all_deliveries AS (
            SELECT
                pm.id as match_id,
                pm.metadata->'info'->'dates'->0 as match_date,
                pm.metadata->'info'->>'venue' as venue,
                innings_elem->>'team' as batting_team,
                innings_elem->'overs' as overs_array
            FROM player_matches pm,
            LATERAL jsonb_array_elements(pm.metadata->'innings') as innings_elem
        ),
        all_balls AS (
            SELECT
                ad.match_id,
                ad.match_date,
                ad.venue,
                ad.batting_team,
                delivery_elem
            FROM all_deliveries ad,
            LATERAL jsonb_array_elements(ad.overs_array) as over_elem,
            LATERAL jsonb_array_elements(over_elem->'deliveries') as delivery_elem
            WHERE delivery_elem->>'batter' = %s
              AND delivery_elem->>'bowler' = %s
        ),
        match_encounters AS (
            SELECT
                match_id,
                match_date,
                venue,
                batting_team,
                COUNT(*) as balls_faced,
                COALESCE(SUM((delivery_elem->'runs'->>'batter')::int), 0) as runs_scored,
                MAX(CASE WHEN delivery_elem->'wickets' IS NOT NULL
                         AND delivery_elem->'wickets'->0->>'player_out' = %s
                         THEN 1 ELSE 0 END) as dismissed
            FROM all_balls
            GROUP BY match_id, match_date, venue, batting_team
        )
        SELECT
            match_id,
            match_date,
            venue,
            batting_team,
            balls_faced,
            runs_scored,
            ROUND((runs_scored::numeric / NULLIF(balls_faced, 0) * 100), 2) as strike_rate,
            CASE WHEN dismissed = 1 THEN 'Dismissed' ELSE 'Not Out' END as result
        FROM match_encounters
        ORDER BY match_date DESC
        """

        with Database() as db:
            stats = db.execute_query(query, (batter_name, bowler_name, batter_name, bowler_name, batter_name, batter_name))
            encounters = db.execute_query(encounters_query, (batter_name, bowler_name, batter_name, bowler_name, batter_name))

            if stats and len(stats) > 0 and stats[0]['balls_faced'] > 0:
                return jsonify({
                    'success': True,
                    'batter': batter_name,
                    'bowler': bowler_name,
                    'overall_stats': stats[0],
                    'encounters': encounters if encounters else []
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No data found for this matchup'
                }), 404

    except Exception as e:
        print(f"Error in vs_bowler: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@vs_bowler_bp.route('/batter/<batter_name>/bowlers', methods=['GET'])
def get_batter_vs_all_bowlers(batter_name):
    """
    Get statistics of a batter against all bowlers - simplified
    """
    try:
        return jsonify({
            'success': True,
            'batter': batter_name,
            'stats': []
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@vs_bowler_bp.route('/bowler/<bowler_name>/batters', methods=['GET'])
def get_bowler_vs_all_batters(bowler_name):
    """
    Get statistics of a bowler against all batters - simplified
    """
    try:
        return jsonify({
            'success': True,
            'bowler': bowler_name,
            'stats': []
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
