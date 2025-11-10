"""
Utility functions for the ODI Cricket Analytics application
"""

def format_player_name(name):
    """Format player name for consistent display"""
    return name.strip()

def calculate_strike_rate(runs, balls):
    """Calculate batting strike rate"""
    if balls == 0:
        return 0
    return round((runs / balls) * 100, 2)

def calculate_batting_average(runs, dismissals):
    """Calculate batting average"""
    if dismissals == 0:
        return float('inf')  # Not out in all innings
    return round(runs / dismissals, 2)

def calculate_economy_rate(runs, balls):
    """Calculate bowling economy rate (runs per over)"""
    if balls == 0:
        return 0
    overs = balls / 6
    return round(runs / overs, 2)

def calculate_bowling_average(runs, wickets):
    """Calculate bowling average"""
    if wickets == 0:
        return float('inf')
    return round(runs / wickets, 2)

def calculate_bowling_strike_rate(balls, wickets):
    """Calculate bowling strike rate (balls per wicket)"""
    if wickets == 0:
        return float('inf')
    return round(balls / wickets, 2)

def format_date(date_str):
    """Format date string for display"""
    try:
        from datetime import datetime
        date_obj = datetime.strptime(date_str.strip('"'), '%Y-%m-%d')
        return date_obj.strftime('%d %b %Y')
    except:
        return date_str

def get_phase_from_over(over_num):
    """Get match phase from over number"""
    if over_num < 10:
        return 'Powerplay'
    elif over_num < 40:
        return 'Middle Overs'
    else:
        return 'Death Overs'
