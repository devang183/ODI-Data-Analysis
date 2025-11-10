from flask import Blueprint, request, jsonify
from models.database import Database

phase_performance_bp = Blueprint('phase_performance', __name__)

@phase_performance_bp.route('/player/<player_name>', methods=['GET'])
def get_player_phase_performance(player_name):
    """
    Get batting performance in different phases (Powerplay, Middle, Death)
    Phases: Powerplay (0-10 overs), Middle (11-40 overs), Death (41-50 overs)
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
                innings_data->>'team' as batting_team,
                jsonb_array_elements(innings_data->'overs') as over_data
        ),
        ball_by_ball AS (
            SELECT
                match_id,
                batting_team,
                (over_data->>'over')::int as over_num,
                jsonb_array_elements(over_data->'deliveries') as delivery
        ),
        phase_data AS (
            SELECT
                CASE
                    WHEN over_num < 10 THEN 'Powerplay'
                    WHEN over_num >= 10 AND over_num < 40 THEN 'Middle Overs'
                    ELSE 'Death Overs'
                END as phase,
                COUNT(*) as balls_faced,
                SUM((delivery->'runs'->>'batter')::int) as runs_scored,
                SUM(CASE WHEN delivery->'wickets' IS NOT NULL THEN 1 ELSE 0 END) as dismissals,
                SUM(CASE WHEN (delivery->'runs'->>'batter')::int = 4 THEN 1 ELSE 0 END) as fours,
                SUM(CASE WHEN (delivery->'runs'->>'batter')::int = 6 THEN 1 ELSE 0 END) as sixes,
                SUM(CASE WHEN (delivery->'runs'->>'batter')::int = 0 THEN 1 ELSE 0 END) as dots
            FROM ball_by_ball
            WHERE delivery->>'batter' = %s
            GROUP BY phase
        )
        SELECT
            phase,
            balls_faced,
            runs_scored,
            dismissals,
            fours,
            sixes,
            dots,
            ROUND((runs_scored::numeric / NULLIF(balls_faced, 0) * 100), 2) as strike_rate,
            ROUND((runs_scored::numeric / NULLIF(dismissals, 0)), 2) as average,
            ROUND((dots::numeric / NULLIF(balls_faced, 0) * 100), 2) as dot_ball_percentage
        FROM phase_data
        ORDER BY
            CASE phase
                WHEN 'Powerplay' THEN 1
                WHEN 'Middle Overs' THEN 2
                WHEN 'Death Overs' THEN 3
            END
        """

        with Database() as db:
            results = db.execute_query(query, (player_name,))

            return jsonify({
                'success': True,
                'player': player_name,
                'phases': results if results else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@phase_performance_bp.route('/player/<player_name>/bowling', methods=['GET'])
def get_player_bowling_phase_performance(player_name):
    """
    Get bowling performance in different phases
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
                innings_data->>'team' as batting_team,
                jsonb_array_elements(innings_data->'overs') as over_data
        ),
        ball_by_ball AS (
            SELECT
                match_id,
                batting_team,
                (over_data->>'over')::int as over_num,
                jsonb_array_elements(over_data->'deliveries') as delivery
        ),
        phase_data AS (
            SELECT
                CASE
                    WHEN over_num < 10 THEN 'Powerplay'
                    WHEN over_num >= 10 AND over_num < 40 THEN 'Middle Overs'
                    ELSE 'Death Overs'
                END as phase,
                COUNT(*) as balls_bowled,
                SUM((delivery->'runs'->>'total')::int) as runs_conceded,
                SUM(CASE WHEN delivery->'wickets' IS NOT NULL THEN 1 ELSE 0 END) as wickets,
                SUM(CASE WHEN (delivery->'runs'->>'total')::int = 0 THEN 1 ELSE 0 END) as dots
            FROM ball_by_ball
            WHERE delivery->>'bowler' = %s
            GROUP BY phase
        )
        SELECT
            phase,
            balls_bowled,
            ROUND(balls_bowled::numeric / 6, 1) as overs,
            runs_conceded,
            wickets,
            dots,
            ROUND((runs_conceded::numeric / NULLIF(balls_bowled, 0) * 6), 2) as economy,
            ROUND((runs_conceded::numeric / NULLIF(wickets, 0)), 2) as average,
            ROUND((balls_bowled::numeric / NULLIF(wickets, 0)), 2) as strike_rate,
            ROUND((dots::numeric / NULLIF(balls_bowled, 0) * 100), 2) as dot_ball_percentage
        FROM phase_data
        ORDER BY
            CASE phase
                WHEN 'Powerplay' THEN 1
                WHEN 'Middle Overs' THEN 2
                WHEN 'Death Overs' THEN 3
            END
        """

        with Database() as db:
            results = db.execute_query(query, (player_name,))

            return jsonify({
                'success': True,
                'player': player_name,
                'phases': results if results else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@phase_performance_bp.route('/team/<team_name>', methods=['GET'])
def get_team_phase_performance(team_name):
    """
    Get team batting performance across different phases
    """
    try:
        query = """
        WITH deliveries AS (
            SELECT
                id as match_id,
                metadata->'info'->'teams' as teams,
                jsonb_array_elements(metadata->'innings') as innings_data
        ),
        player_deliveries AS (
            SELECT
                match_id,
                teams,
                innings_data->>'team' as batting_team,
                jsonb_array_elements(innings_data->'overs') as over_data
        ),
        ball_by_ball AS (
            SELECT
                match_id,
                teams,
                batting_team,
                (over_data->>'over')::int as over_num,
                jsonb_array_elements(over_data->'deliveries') as delivery
        ),
        phase_data AS (
            SELECT
                CASE
                    WHEN over_num < 10 THEN 'Powerplay'
                    WHEN over_num >= 10 AND over_num < 40 THEN 'Middle Overs'
                    ELSE 'Death Overs'
                END as phase,
                COUNT(*) as balls_faced,
                SUM((delivery->'runs'->>'batter')::int) as runs_scored,
                SUM(CASE WHEN delivery->'wickets' IS NOT NULL THEN 1 ELSE 0 END) as wickets_lost,
                SUM(CASE WHEN (delivery->'runs'->>'batter')::int = 4 THEN 1 ELSE 0 END) as fours,
                SUM(CASE WHEN (delivery->'runs'->>'batter')::int = 6 THEN 1 ELSE 0 END) as sixes
            FROM ball_by_ball
            WHERE batting_team = %s
                AND teams @> %s
            GROUP BY phase
        )
        SELECT
            phase,
            balls_faced,
            runs_scored,
            wickets_lost,
            fours,
            sixes,
            ROUND((runs_scored::numeric / NULLIF(balls_faced, 0) * 100), 2) as strike_rate,
            ROUND((runs_scored::numeric / NULLIF(balls_faced, 0) * 6), 2) as run_rate
        FROM phase_data
        ORDER BY
            CASE phase
                WHEN 'Powerplay' THEN 1
                WHEN 'Middle Overs' THEN 2
                WHEN 'Death Overs' THEN 3
            END
        """

        with Database() as db:
            results = db.execute_query(query, (team_name, f'["{team_name}"]'))

            return jsonify({
                'success': True,
                'team': team_name,
                'phases': results if results else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@phase_performance_bp.route('/player/<player_name>/custom-analysis', methods=['GET'])
def get_custom_phase_analysis(player_name):
    """
    Analyze player performance in a custom phase
    Query params:
    - balls_before: Minimum balls faced before the analysis phase
    - over_start: Over number when the analysis phase begins
    - overs_to_analyze: Number of overs in the analysis phase
    - min_balls_in_phase: Minimum balls to face in the analysis phase
    """
    try:
        balls_before = int(request.args.get('balls_before', 15))
        over_start = int(request.args.get('over_start', 7))
        overs_to_analyze = int(request.args.get('overs_to_analyze', 3))
        min_balls_in_phase = int(request.args.get('min_balls_in_phase', 10))

        over_end = over_start + overs_to_analyze

        query = """
        WITH player_matches AS (
            SELECT o.id, o.metadata
            FROM odiwc2023 o
            WHERE o.metadata->'info'->'registry'->'people' ? %s
        ),
        all_innings AS (
            SELECT
                pm.id as match_id,
                innings_elem as innings_data
            FROM player_matches pm,
            LATERAL jsonb_array_elements(pm.metadata->'innings') as innings_elem
        ),
        ball_by_ball AS (
            SELECT
                ai.match_id,
                (over_elem->>'over')::int as over_num,
                delivery_elem as delivery,
                ROW_NUMBER() OVER (
                    PARTITION BY ai.match_id, ai.innings_data
                    ORDER BY (over_elem->>'over')::int,
                             (SELECT ordinality FROM jsonb_array_elements(over_elem->'deliveries')
                              WITH ORDINALITY WHERE value = delivery_elem LIMIT 1)
                ) as ball_number
            FROM all_innings ai,
            LATERAL jsonb_array_elements(ai.innings_data->'overs') as over_elem,
            LATERAL jsonb_array_elements(over_elem->'deliveries') as delivery_elem
            WHERE delivery_elem->>'batter' = %s
        ),
        innings_with_criteria AS (
            SELECT DISTINCT
                match_id,
                COUNT(*) FILTER (WHERE ball_number <= %s) as balls_before_phase,
                COUNT(*) FILTER (WHERE over_num >= %s AND over_num < %s) as balls_in_phase
            FROM ball_by_ball
            GROUP BY match_id
            HAVING COUNT(*) FILTER (WHERE ball_number <= %s) >= %s
                AND COUNT(*) FILTER (WHERE over_num >= %s AND over_num < %s) >= %s
        ),
        phase_performance AS (
            SELECT
                b.match_id,
                (b.delivery->'runs'->>'batter')::int as runs,
                CASE WHEN b.delivery->'wickets' IS NOT NULL
                     AND jsonb_array_length(b.delivery->'wickets') > 0
                     AND b.delivery->'wickets'->0->>'player_out' = %s
                     THEN 1 ELSE 0
                END as is_dismissed
            FROM ball_by_ball b
            INNER JOIN innings_with_criteria iwc ON b.match_id = iwc.match_id
            WHERE b.over_num >= %s AND b.over_num < %s
        ),
        run_distribution AS (
            SELECT
                CASE
                    WHEN runs = 0 THEN '0'
                    WHEN runs BETWEEN 1 AND 3 THEN '1-3'
                    WHEN runs = 4 THEN '4'
                    WHEN runs = 5 THEN '5'
                    WHEN runs = 6 THEN '6'
                    ELSE '7+'
                END as run_range,
                COUNT(*) as frequency
            FROM phase_performance
            GROUP BY run_range
        )
        SELECT
            (SELECT COUNT(*) FROM innings_with_criteria) as innings_analyzed,
            (SELECT COALESCE(SUM(runs), 0) FROM phase_performance) as total_runs,
            (SELECT COUNT(*) FROM phase_performance) as total_balls,
            (SELECT COALESCE(SUM(is_dismissed), 0) FROM phase_performance) as times_dismissed,
            (SELECT ROUND(AVG(runs)::numeric, 1) FROM phase_performance) as avg_runs_per_ball,
            (SELECT ROUND((COALESCE(SUM(runs), 0)::numeric / NULLIF(COUNT(*), 0) * 100), 0)
             FROM phase_performance) as strike_rate,
            (SELECT ROUND((COALESCE(SUM(is_dismissed), 0)::numeric / NULLIF(COUNT(DISTINCT match_id), 0) * 100), 0)
             FROM phase_performance) as dismissal_rate,
            (SELECT json_agg(json_build_object('run_range', run_range, 'frequency', frequency)
                             ORDER BY CASE run_range
                                 WHEN '0' THEN 1
                                 WHEN '1-3' THEN 2
                                 WHEN '4' THEN 3
                                 WHEN '5' THEN 4
                                 WHEN '6' THEN 5
                                 ELSE 6
                             END)
             FROM run_distribution) as run_distribution
        """

        with Database() as db:
            results = db.execute_query(query, (
                player_name, player_name,
                balls_before, over_start, over_end,
                balls_before, balls_before,
                over_start, over_end, min_balls_in_phase,
                player_name,
                over_start, over_end
            ))

            if results and len(results) > 0:
                result = results[0]
                return jsonify({
                    'success': True,
                    'player': player_name,
                    'parameters': {
                        'balls_before': balls_before,
                        'over_start': over_start,
                        'overs_to_analyze': overs_to_analyze,
                        'min_balls_in_phase': min_balls_in_phase
                    },
                    'summary': {
                        'avg_runs_per_ball': result.get('avg_runs_per_ball') or 0,
                        'strike_rate': result.get('strike_rate') or 0,
                        'dismissal_rate': result.get('dismissal_rate') or 0,
                        'innings_analyzed': result.get('innings_analyzed') or 0
                    },
                    'totals': {
                        'total_runs': result.get('total_runs') or 0,
                        'total_balls': result.get('total_balls') or 0,
                        'times_dismissed': result.get('times_dismissed') or 0
                    },
                    'run_distribution': result.get('run_distribution') or []
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No data found for the given criteria'
                }), 404

    except Exception as e:
        print(f"Error in custom phase analysis: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
