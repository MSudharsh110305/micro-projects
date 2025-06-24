from user_profile import get_daily_intake

def summarize_intake(rows):
    """Given a list of intake rows, return totals as a dict."""
    totals = {'calories':0, 'protein':0, 'fat':0, 'carbs':0, 'sugar':0, 'sodium':0}
    for _, cal, prot, fat, carb, sugar, sod in rows:
        totals['calories'] += cal
        totals['protein']  += prot
        totals['fat']      += fat
        totals['carbs']    += carb
        totals['sugar']    += sugar
        totals['sodium']   += sod
    return totals

def get_today_summary():
    rows = get_daily_intake()
    return summarize_intake(rows)
