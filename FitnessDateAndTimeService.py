import calendar
import math
from datetime import datetime, timedelta

MON_WED_FRI_SPECIFIC_WEEKDAYS = [0, 2, 4]  # понедельники, среды, пятницы (турник)
TUE_THUR_SAT_SPECIFIC_WEEKDAYS = [1, 3, 5]  # вторники, четверги, субботы (брусья)

# Получите текущую дату
now = datetime.now()

# Извлеките текущий год и месяц
year = now.year
month = now.month
day_of_month = now.day

# Получите первый и последний дни текущего месяца
first_day_of_month = datetime(year, month, 1)
last_day_of_month = datetime(year, month, calendar.monthrange(year, month)[1])

class FitnessDateAndTimeService:

    def get_mon_wed_fri_days(self):
        # ---=== ТУРНИК ===---
        # Количество понедельников, сред и пятниц по сегодняшний день включительно
        mon_wed_fri_days_until_now = self._count_weekdays(first_day_of_month, now, MON_WED_FRI_SPECIFIC_WEEKDAYS)
        # Количество понедельников, сред и пятниц в текущем месяце
        mon_wed_fri_days_all = self._count_weekdays(first_day_of_month, last_day_of_month, MON_WED_FRI_SPECIFIC_WEEKDAYS)
        # print(f"Количество понедельников, сред и пятниц по сегодняшний день включительно: {mon_wed_fri_days_until_now}")
        # print(f"Количество понедельников, сред и пятниц в текущем месяце: {mon_wed_fri_days_all}\n")
        return mon_wed_fri_days_until_now, mon_wed_fri_days_all

    def get_tue_thu_sat_days(self):
        # ---=== БРУСЬЯ ===---
        # Количество вторников, четвергов и суббот по сегодняшний день включительно
        tue_thu_sat_days_until_now = self._count_weekdays(first_day_of_month, now, TUE_THUR_SAT_SPECIFIC_WEEKDAYS)
        # Количество вторников, четвергов и суббот в текущем месяце
        tue_thu_sat_days_all = self._count_weekdays(first_day_of_month, last_day_of_month, TUE_THUR_SAT_SPECIFIC_WEEKDAYS)
        # print(f"Количество вторников, четвергов и суббот по сегодняшний день включительно: {tue_thu_sat_days_until_now}")
        # print(f"Количество вторников, четвергов и суббот в текущем месяце: {tue_thu_sat_days_all}")
        return tue_thu_sat_days_until_now, tue_thu_sat_days_all

    # Определите количество понедельников, сред и пятниц
    # specific_weekdays=[0, 2, 4] - понедельники, среды, пятницы (турник)
    # specific_weekdays=[1, 3, 5] - вторники, четверги, субботы (брусья)
    def _count_weekdays(self, start_date, end_date, specific_weekdays):
        specific_weekdays_counter = 0
        current_day = start_date
        while current_day <= end_date:
            if current_day.weekday() in specific_weekdays:
                specific_weekdays_counter += 1
            # Переходите к следующему дню
            current_day += timedelta(days=1)
        return specific_weekdays_counter


