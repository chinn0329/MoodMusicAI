def get_music_query(mood, intensity, adjust_style=False):
    base_queries = {
        "Happy": "happy upbeat pop",
        "Sad": "sad acoustic piano",
        "Stressed": "calming ambient instrumental",
        "Calm": "peaceful instrumental",
        "Focused": "lofi study beats"
    }

    intensity_modifier = {
        "Low": "",
        "Medium": "soft",
        "High": "very calming"
    }

    query = f"{intensity_modifier[intensity]} {base_queries[mood]}"

    if adjust_style:
        query += " alternative"

    return query.strip()


def explain_recommendation(mood, intensity, mode):
    if mode == "Student Mode":
        return (
            f"This music is recommended to match your "
            f"{intensity.lower()} intensity {mood.lower()} mood "
            f"and help regulate emotions."
        )
    else:
        return (
            f"The recommendation aligns with a "
            f"{intensity.lower()} intensity {mood.lower()} emotional state, "
            f"following music therapy principles."
        )
def therapy_goal_modifier(goal):
    goal_map = {
        "Stress Reduction": "slow calming",
        "Emotional Grounding": "steady instrumental",
        "Anxiety Calming": "ambient soothing",
        "Sleep Preparation": "sleep peaceful"
    }

    return goal_map.get(goal, "")
