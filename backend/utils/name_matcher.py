"""
Smart name matching utility for cricket players
Handles abbreviated names like "V Kohli" vs "Virat Kohli"
"""

def levenshtein_distance(str1, str2):
    """Calculate Levenshtein distance between two strings"""
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1].lower() == str2[j-1].lower():
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return dp[m][n]


def get_last_name(name):
    """Extract last name from a player name"""
    parts = name.strip().split()
    return parts[-1].lower() if parts else ""


def get_first_part(name):
    """Extract first name or initials"""
    parts = name.strip().split()
    return parts[0].lower() if parts else ""


def calculate_name_similarity(query, player_name):
    """
    Calculate similarity score between query and player name
    Returns a score from 0 (no match) to 100 (perfect match)
    """
    query_lower = query.lower().strip()
    player_lower = player_name.lower().strip()

    # Perfect match
    if query_lower == player_lower:
        return 100

    # Exact substring match
    if query_lower in player_lower or player_lower in query_lower:
        return 95

    query_last_name = get_last_name(query)
    player_last_name = get_last_name(player_name)
    query_first_part = get_first_part(query)
    player_first_part = get_first_part(player_name)

    score = 0

    # Last name exact match is very strong indicator
    if query_last_name == player_last_name:
        score += 70

        # Check first name/initial match
        if query_first_part == player_first_part:
            score += 30  # Perfect match with abbreviated first name
        elif len(player_first_part) <= 2:
            # Player name has initials (like "V" in "V Kohli")
            if query_first_part and query_first_part[0] == player_first_part[0]:
                score += 25  # "virat" starts with "v"
        elif len(query_first_part) <= 2:
            # Query has initials
            if player_first_part and player_first_part[0] == query_first_part[0]:
                score += 25
        else:
            # Both are full names, use fuzzy matching
            first_name_distance = levenshtein_distance(query_first_part, player_first_part)
            max_length = max(len(query_first_part), len(player_first_part))
            if max_length > 0:
                similarity = max(0, 1 - first_name_distance / max_length)
                score += similarity * 25
    else:
        # Last names don't match exactly, use fuzzy matching
        last_name_distance = levenshtein_distance(query_last_name, player_last_name)
        max_length = max(len(query_last_name), len(player_last_name))

        if max_length > 0:
            last_name_similarity = max(0, 1 - last_name_distance / max_length)

            if last_name_similarity > 0.7:
                score += last_name_similarity * 60

                # Check first name
                first_name_distance = levenshtein_distance(query_first_part, player_first_part)
                first_max_length = max(len(query_first_part), len(player_first_part))
                if first_max_length > 0:
                    first_name_similarity = max(0, 1 - first_name_distance / first_max_length)
                    score += first_name_similarity * 30

    # Bonus for word-level matches
    query_words = query_lower.split()
    player_words = player_lower.split()

    for q_word in query_words:
        if len(q_word) > 2:
            for p_word in player_words:
                if q_word in p_word or p_word in q_word:
                    score += 5

    return min(100, round(score))


# Player popularity/priority mapping
PLAYER_PRIORITY = {
    'V Kohli': 100,
    'Virat Kohli': 100,
    'Rohit Sharma': 95,
    'MS Dhoni': 95,
    'AB de Villiers': 90,
    'JJ Bumrah': 90,
    'SR Tendulkar': 85,
    'Sachin Tendulkar': 85,
    'CH Gayle': 85,
    'Chris Gayle': 85,
    'DA Warner': 80,
    'David Warner': 80,
    'RA Jadeja': 80,
    'Ravindra Jadeja': 80,
    'SK Raina': 80,
    'Suresh Raina': 80,
    'YZ Chahal': 78,
    'HH Pandya': 75,
    'Hardik Pandya': 75,
    'KL Rahul': 75,
    'YK Pathan': 75,
    'Rashid Khan': 73,
    'DJ Bravo': 70,
    'Dwayne Bravo': 70,
    'R Ashwin': 70,
    'SA Yadav': 70,
    'Suryakumar Yadav': 70,
    'SL Malinga': 68,
    'Lasith Malinga': 68,
    'AD Russell': 67,
    'Andre Russell': 67,
    'PP Shaw': 65,
    'SS Iyer': 65,
    'KA Pollard': 65,
    'Kieron Pollard': 65,
    'HV Patel': 72,
    'Harshal Patel': 72,
    'MG Johnson': 85,
    'Mitchell Johnson': 85,
    'B Lee': 90,
    'Brett Lee': 90,
    'GD McGrath': 88,
    'Glenn McGrath': 88,
}


def find_best_player_match(query, players, threshold=60):
    """
    Find best matching player from a list
    Returns dict with player name and score, or None
    """
    if not query or not players:
        return None

    matches = []
    for player in players:
        score = calculate_name_similarity(query, player)
        priority = PLAYER_PRIORITY.get(player, 0)

        # Add priority bonus (scaled down to not overwhelm the similarity score)
        adjusted_score = score + (priority * 0.1)

        if score >= threshold:
            matches.append({
                'player': player,
                'score': score,
                'adjusted_score': adjusted_score,
                'priority': priority
            })

    if not matches:
        return None

    # Sort by adjusted score
    matches.sort(key=lambda x: (
        # If scores are within 10 points, prioritize by adjusted score
        x['adjusted_score'] if abs(x['score'] - matches[0]['score']) <= 10 else x['score']
    ), reverse=True)

    best_match = matches[0]

    return {
        'player': best_match['player'],
        'score': best_match['score']
    }


def get_player_profile_with_smart_matching(db, player_name):
    """
    Get player profile using smart name matching
    Returns profile dict or None
    """
    # First try exact match
    exact_query = """
    SELECT
        fullname,
        image_path,
        dateofbirth,
        battingstyle,
        bowlingstyle,
        position,
        country_name,
        country_image_path
    FROM cleaned_all_players
    WHERE fullname = %s
    LIMIT 1
    """

    result = db.execute_query(exact_query, (player_name,))
    if result and len(result) > 0:
        return result[0]

    # Get all potential matches based on last name
    def extract_last_name(name):
        parts = name.split()
        # Find the first part that is not just initials
        last_name_parts = [p for p in parts if len(p) > 2 or any(c.islower() for c in p)]
        if last_name_parts:
            return ' '.join(last_name_parts)
        return parts[-1] if parts else name

    last_name = extract_last_name(player_name)

    fuzzy_query = """
    SELECT
        fullname,
        image_path,
        dateofbirth,
        battingstyle,
        bowlingstyle,
        position,
        country_name,
        country_image_path
    FROM cleaned_all_players
    WHERE fullname ILIKE %s
    """

    candidates = db.execute_query(fuzzy_query, (f'%{last_name}%',))

    if not candidates:
        return None

    # Use smart matching to find best candidate
    candidate_names = [c['fullname'] for c in candidates]
    best_match = find_best_player_match(player_name, candidate_names, threshold=60)

    if not best_match:
        return None

    # Return the profile of the best match
    for candidate in candidates:
        if candidate['fullname'] == best_match['player']:
            print(f"Smart match: '{player_name}' -> '{best_match['player']}' (score: {best_match['score']})")
            return candidate

    return None
