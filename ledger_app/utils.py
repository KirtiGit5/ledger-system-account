import calendar
from datetime import date

def get_month_choices():
    today = date.today()
    return [
        (f"{today.year}-{str(m).zfill(2)}", calendar.month_name[m])
        for m in range(1, 13)
    ]