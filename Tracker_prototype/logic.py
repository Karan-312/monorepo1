# File: logic.py

from datetime import datetime, timedelta

# Define your performance rating system
def calculate_last_performance(checkbox_states):
    """
    Accepts a dict like:
    {
        '1st_Myself': True,
        '1st_Help': False,
        ...
    }
    Returns one of: Excellent, Good, Mid, Poor, Skipped
    """
    score = 0
    for try_num in range(1, 5):
        myself = checkbox_states.get(f"{try_num}st_Myself") or checkbox_states.get(f"{try_num}nd_Myself") or checkbox_states.get(f"{try_num}rd_Myself") or checkbox_states.get(f"{try_num}th_Myself")
        help_ = checkbox_states.get(f"{try_num}st_Help") or checkbox_states.get(f"{try_num}nd_Help") or checkbox_states.get(f"{try_num}rd_Help") or checkbox_states.get(f"{try_num}th_Help")

        if myself:
            score += 2
        elif help_:
            score += 1

    if score >= 7:
        return "Excellent"
    elif score >= 5:
        return "Good"
    elif score >= 3:
        return "Mid"
    elif score >= 1:
        return "Poor"
    else:
        return "Skipped"


def estimate_next_review(last_date_str, performance):
    """
    Takes date string like '2025-06-18' and performance string.
    Returns next review date as string.
    """
    try:
        if not last_date_str:
            return "No Date"

        last_date_str = last_date_str.strip()

        # Strict parsing: must be YYYY-MM-DD
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")

        delta_days = {
            "Excellent": 30,
            "Good": 14,
            "Mid": 7,
            "Poor": 3,
            "Skipped": 1
        }.get(performance, 7)

        next_date = last_date + timedelta(days=delta_days)
        return next_date.strftime("%Y-%m-%d")

    except Exception as e:
        print(" Review date error:", e)
        return "Invalid Date"
