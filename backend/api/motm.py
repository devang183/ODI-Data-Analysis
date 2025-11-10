from flask import Blueprint, request, jsonify
from models.database import Database

motm_bp = Blueprint('motm', __name__)

@motm_bp.route('/player/<player_name>', methods=['GET'])
def get_player_motm_awards(player_name):
    """
    Get all Man of the Match awards for a player
    """
    try:
        query = """
        SELECT
            id as match_id,
            metadata->'info'->'dates'->0 as match_date,
            metadata->'info'->>'venue' as venue,
            metadata->'info'->>'city' as city,
            metadata->'info'->'teams' as teams,
            metadata->'info'->'outcome'->>'winner' as winner,
            metadata->'info'->'outcome'->'by' as win_margin,
            metadata->'info'->'event'->>'name' as event_name,
            metadata->'info'->>'season' as season
        FROM odiwc2023
        WHERE metadata->'info'->'player_of_match' @> %s
        ORDER BY metadata->'info'->'dates'->0 DESC
        """

        # Also get count and statistics
        stats_query = """
        WITH motm_matches AS (
            SELECT
                id as match_id,
                metadata->'info'->'outcome'->>'winner' as winner,
                metadata->'info'->'teams' as teams,
                metadata->'info'->'players' as players
            FROM odiwc2023
            WHERE metadata->'info'->'player_of_match' @> %s
        ),
        player_team_check AS (
            SELECT
                mm.match_id,
                mm.winner,
                CASE
                    WHEN mm.teams->>0 = %s THEN mm.teams->>0
                    WHEN mm.teams->>1 = %s THEN mm.teams->>1
                    ELSE (
                        SELECT team_name
                        FROM (VALUES (mm.teams->>0), (mm.teams->>1)) AS t(team_name)
                        WHERE mm.players->team_name @> %s
                        LIMIT 1
                    )
                END as player_team
            FROM motm_matches mm
        )
        SELECT
            COUNT(*) as total_awards,
            SUM(CASE WHEN winner = player_team THEN 1 ELSE 0 END) as awards_in_wins,
            SUM(CASE WHEN winner != player_team OR winner IS NULL THEN 1 ELSE 0 END) as awards_in_losses
        FROM player_team_check
        WHERE player_team IS NOT NULL
        """

        with Database() as db:
            awards = db.execute_query(query, (f'["{player_name}"]',))
            stats = db.execute_query(stats_query, (f'["{player_name}"]', player_name, player_name, f'["{player_name}"]'))

            return jsonify({
                'success': True,
                'player': player_name,
                'statistics': stats[0] if stats and len(stats) > 0 else {},
                'awards': awards if awards else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@motm_bp.route('/leaderboard', methods=['GET'])
def get_motm_leaderboard():
    """
    Get players with most Man of the Match awards
    """
    try:
        limit = int(request.args.get('limit', 50))

        query = """
        WITH motm_data AS (
            SELECT
                jsonb_array_elements_text(metadata->'info'->'player_of_match') as player_name,
                metadata->'info'->'dates'->0 as match_date
            FROM odiwc2023
            WHERE metadata->'info'->'player_of_match' IS NOT NULL
        )
        SELECT
            player_name,
            COUNT(*) as total_awards,
            MIN(match_date) as first_award,
            MAX(match_date) as latest_award
        FROM motm_data
        GROUP BY player_name
        ORDER BY total_awards DESC, player_name
        LIMIT %s
        """

        with Database() as db:
            results = db.execute_query(query, (limit,))

            return jsonify({
                'success': True,
                'data': results if results else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@motm_bp.route('/by-year', methods=['GET'])
def get_motm_by_year():
    """
    Get MOTM awards distribution by year
    """
    try:
        query = """
        WITH motm_data AS (
            SELECT
                SUBSTRING(metadata->'info'->>'season' FROM 1 FOR 4) as year,
                jsonb_array_elements_text(metadata->'info'->'player_of_match') as player_name
            FROM odiwc2023
            WHERE metadata->'info'->'player_of_match' IS NOT NULL
                AND metadata->'info'->>'season' IS NOT NULL
        )
        SELECT
            year,
            player_name,
            COUNT(*) as awards
        FROM motm_data
        GROUP BY year, player_name
        ORDER BY year DESC, awards DESC
        """

        with Database() as db:
            results = db.execute_query(query)

            return jsonify({
                'success': True,
                'data': results if results else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@motm_bp.route('/team/<team_name>', methods=['GET'])
def get_team_motm_players(team_name):
    """
    Get players from a team who have won MOTM awards
    """
    try:
        query = """
        WITH team_matches AS (
            SELECT
                id as match_id,
                metadata->'info'->'dates'->0 as match_date,
                metadata->'info'->'player_of_match' as motm_players,
                metadata->'info'->'players'->%s as team_players
            FROM odiwc2023
            WHERE metadata->'info'->'teams' @> %s
                AND metadata->'info'->'player_of_match' IS NOT NULL
        ),
        player_awards AS (
            SELECT
                jsonb_array_elements_text(motm_players) as player_name,
                match_date
            FROM team_matches
            WHERE team_players @> (SELECT jsonb_array_elements_text(motm_players) FROM team_matches LIMIT 1)
        )
        SELECT
            player_name,
            COUNT(*) as awards,
            MIN(match_date) as first_award,
            MAX(match_date) as latest_award
        FROM player_awards
        GROUP BY player_name
        ORDER BY awards DESC
        """

        with Database() as db:
            results = db.execute_query(query, (team_name, f'["{team_name}"]'))

            return jsonify({
                'success': True,
                'team': team_name,
                'players': results if results else []
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
