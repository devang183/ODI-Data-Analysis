from flask import Blueprint, request, jsonify
from models.database import Database

dismissal_patterns_bp = Blueprint('dismissal_patterns', __name__)

@dismissal_patterns_bp.route('/player/<player_name>', methods=['GET'])
def get_player_dismissal_patterns(player_name):
    """
    Get dismissal patterns for a player (how they get out most often)
    """
    try:
        query = """
        WITH deliveries AS (
            SELECT
                id as match_id,
                jsonb_array_elements(metadata->'innings') as innings_data
        ),
        player_deliveries AS (
            SELECT
                match_id,
                jsonb_array_elements(innings_data->'overs') as over_data
        ),
        ball_by_ball AS (
            SELECT
                match_id,
                jsonb_array_elements(over_data->'deliveries') as delivery
        ),
        dismissals AS (
            SELECT
                delivery->'wickets'->0->>'kind' as dismissal_type,
                delivery->>'bowler' as bowler,
                COUNT(*) as count
            FROM ball_by_ball
            WHERE delivery->'wickets' IS NOT NULL
                AND delivery->'wickets'->0->>'player_out' = %s
            GROUP BY dismissal_type, bowler
        )
        SELECT
            dismissal_type,
            bowler,
            count,
            ROUND((count::numeric / SUM(count) OVER () * 100), 2) as percentage
        FROM dismissals
        ORDER BY count DESC
        """

        with Database() as db:
            results = db.execute_query(query, (player_name,))

            # Also get dismissal type summary
            summary_query = """
            WITH deliveries AS (
                SELECT
                    id as match_id,
                    jsonb_array_elements(metadata->'innings') as innings_data
            ),
            player_deliveries AS (
                SELECT
                    match_id,
                    jsonb_array_elements(innings_data->'overs') as over_data
            ),
            ball_by_ball AS (
                SELECT
                    match_id,
                    jsonb_array_elements(over_data->'deliveries') as delivery
            ),
            dismissals AS (
                SELECT
                    delivery->'wickets'->0->>'kind' as dismissal_type,
                    COUNT(*) as count
                FROM ball_by_ball
                WHERE delivery->'wickets' IS NOT NULL
                    AND delivery->'wickets'->0->>'player_out' = %s
                GROUP BY dismissal_type
            )
            SELECT
                dismissal_type,
                count,
                ROUND((count::numeric / SUM(count) OVER () * 100), 2) as percentage
            FROM dismissals
            ORDER BY count DESC
            """

            summary = db.execute_query(summary_query, (player_name,))

            return jsonify({
                'success': True,
                'player': player_name,
                'dismissal_summary': summary if summary else [],
                'dismissal_details': results if results else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dismissal_patterns_bp.route('/player/<player_name>/by-phase', methods=['GET'])
def get_player_dismissal_by_phase(player_name):
    """
    Get dismissal patterns by match phase
    """
    try:
        query = """
        WITH deliveries AS (
            SELECT
                id as match_id,
                jsonb_array_elements(metadata->'innings') as innings_data
        ),
        player_deliveries AS (
            SELECT
                match_id,
                jsonb_array_elements(innings_data->'overs') as over_data
        ),
        ball_by_ball AS (
            SELECT
                match_id,
                (over_data->>'over')::int as over_num,
                jsonb_array_elements(over_data->'deliveries') as delivery
        ),
        dismissals AS (
            SELECT
                CASE
                    WHEN over_num < 10 THEN 'Powerplay'
                    WHEN over_num >= 10 AND over_num < 40 THEN 'Middle Overs'
                    ELSE 'Death Overs'
                END as phase,
                delivery->'wickets'->0->>'kind' as dismissal_type,
                COUNT(*) as count
            FROM ball_by_ball
            WHERE delivery->'wickets' IS NOT NULL
                AND delivery->'wickets'->0->>'player_out' = %s
            GROUP BY phase, dismissal_type
        )
        SELECT
            phase,
            dismissal_type,
            count,
            ROUND((count::numeric / SUM(count) OVER (PARTITION BY phase) * 100), 2) as percentage_in_phase
        FROM dismissals
        ORDER BY
            CASE phase
                WHEN 'Powerplay' THEN 1
                WHEN 'Middle Overs' THEN 2
                WHEN 'Death Overs' THEN 3
            END,
            count DESC
        """

        with Database() as db:
            results = db.execute_query(query, (player_name,))

            return jsonify({
                'success': True,
                'player': player_name,
                'data': results if results else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dismissal_patterns_bp.route('/bowler/<bowler_name>/victims', methods=['GET'])
def get_bowler_victims(bowler_name):
    """
    Get list of batsmen dismissed most by a bowler
    """
    try:
        query = """
        WITH deliveries AS (
            SELECT
                id as match_id,
                jsonb_array_elements(metadata->'innings') as innings_data
        ),
        player_deliveries AS (
            SELECT
                match_id,
                jsonb_array_elements(innings_data->'overs') as over_data
        ),
        ball_by_ball AS (
            SELECT
                match_id,
                jsonb_array_elements(over_data->'deliveries') as delivery
        ),
        wickets AS (
            SELECT
                delivery->'wickets'->0->>'player_out' as batsman,
                delivery->'wickets'->0->>'kind' as dismissal_type,
                COUNT(*) as times_dismissed
            FROM ball_by_ball
            WHERE delivery->'wickets' IS NOT NULL
                AND delivery->>'bowler' = %s
            GROUP BY batsman, dismissal_type
        )
        SELECT
            batsman,
            dismissal_type,
            times_dismissed
        FROM wickets
        ORDER BY times_dismissed DESC, batsman
        LIMIT 50
        """

        with Database() as db:
            results = db.execute_query(query, (bowler_name,))

            return jsonify({
                'success': True,
                'bowler': bowler_name,
                'victims': results if results else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
