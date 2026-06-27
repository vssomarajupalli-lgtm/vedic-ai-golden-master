def calculate_planetary_axis(house_1: int, house_2: int) -> str:
    """
    Calculates the positional relationship (axis) between two placements.
    E.g., if Planet A is in House 1 and Planet B is in House 8 -> "6_8" axis.
    
    Args:
        house_1 (int): The house number of the first entity (1-12)
        house_2 (int): The house number of the second entity (1-12)
        
    Returns:
        str: Standardized axis string with the smaller number first (e.g., "6_8", "5_9")
    """
    if not house_1 or not house_2:
        return "1_1"  # Safe fallback if data is missing
        
    if house_1 == house_2:
        return "1_1"
        
    diff_1 = ((house_2 - house_1) % 12) + 1
    diff_2 = ((house_1 - house_2) % 12) + 1
    
    axis_pair = sorted([diff_1, diff_2])
    return f"{axis_pair[0]}_{axis_pair[1]}"

def clamp_score(score: float, min_val: int = 0, max_val: int = 100) -> int:
    """
    Deterministically clamps a calculated astrological score within safe boundaries.
    
    Args:
        score (float): The raw calculated score.
        min_val (int): Minimum allowable bound (default 0).
        max_val (int): Maximum allowable bound (default 100).
        
    Returns:
        int: The clamped integer score, rounded (not truncated) from float.
             Example: raw=0.8 → 1 (not 0). raw=-0.3 → 0 (clamped at min).
    """
    return max(min_val, min(max_val, round(score)))