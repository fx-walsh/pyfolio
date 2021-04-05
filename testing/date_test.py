import datetime

def create_min_max_date(current_date):

    max_year = current_date.year
    min_year = current_date.year if current_date.month != 1 else current_date.year - 1

    max_month = current_date.month
    min_month = current_date.month - 1 if current_date.month != 1 else 12

    max_day = 1
    min_day = 1

    max_date = datetime.date(max_year, max_month, max_day)
    min_date = datetime.date(min_year, min_month, min_day)

    return [min_date, max_date]


refresh_dates = []

for i in range(12):

    refresh_dates.append(datetime.date(2021, i + 1, 1))


for refresh_date in refresh_dates:

    dates = create_min_max_date(refresh_date)

    print("Refresh date: ", refresh_date)
    print("Min date: ", dates[0])
    print("Max date: ", dates[1])
    print("=========================================")

