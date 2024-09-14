import re
from datetime import datetime
import math
from enum import Enum

from FitnessDateAndTimeService import FitnessDateAndTimeService

TARGET_EXERCISES = 1000


class ExerciseType(Enum):
    PULL_UPS = 1
    DIPS = 2


class FitnessCalcService:

    def __init__(self):
        self.fitnessDateAndTimeService = FitnessDateAndTimeService()

    # pull-ups - подтягивания на турнике
    # dips - отжимания на брусьях

    def calculate_exercises(self, column_data, exercise_type: ExerciseType):
        # days_until_now = 0
        # days_all = 0

        if exercise_type == ExerciseType.PULL_UPS:
            mon_wed_fri_days_until_now, mon_wed_fri_days_all = self.fitnessDateAndTimeService.get_mon_wed_fri_days()
            days_until_now = mon_wed_fri_days_until_now
            days_all = mon_wed_fri_days_all
        elif exercise_type == ExerciseType.DIPS:
            tue_thu_sat_days_until_now, tue_thu_sat_days_all = self.fitnessDateAndTimeService.get_tue_thu_sat_days()
            days_until_now = tue_thu_sat_days_until_now
            days_all = tue_thu_sat_days_all

        # Среднее количество упражнений (подтягиваний или отжиманий) в день занятий
        average_exercises = math.ceil(TARGET_EXERCISES / days_all)

        expected_exercises_until_now = days_until_now * average_exercises

        column_data_data_cleaned = self._clean_column_data(column_data)
        actual_exercises_until_now = self._get_actual_exercises_until_now(column_data_data_cleaned)

        diff = actual_exercises_until_now - expected_exercises_until_now
        formatted_diff_str = "{:+}".format(diff)
        return formatted_diff_str, average_exercises

    def _clean_column_data(self, column_data):
        column_data_data_cleaned = []
        for item in column_data[1:]:  # игнорируем первую строку таблицы (header)
            # Если ячейка-список не пустая - берём её первый и единственный элемент
            if item:
                cell = item[0]
            # проставляем в пустую ячейку число 0
            else:
                cell = '0'
            column_data_data_cleaned.append(cell)

        return column_data_data_cleaned

    def _get_actual_exercises_until_now(self, column_data):
        # Определяем какой сегодня день месяца
        day_of_month = datetime.now().day

        # Берём из столбца данные по сегодняшний день месяца включительно.
        # В slice для верхней границы НЕ делаем day_of_month + 1, т. к. индексация в массиве начинается с 0-го элемента,
        # а месяц начинается с 1-го числа и эта разница в единицу даёт нужный результат.
        column_data_until_now = column_data[:day_of_month]

        # Отфильтровываем числовые значения
        numeric_values = [int(item) for item in column_data_until_now if self._is_number(item)]

        # Суммируем числовые значения
        exercises_until_now = sum(numeric_values)

        return exercises_until_now

    def _is_number(self, s: str):
        return bool(re.search(r'^\d+$', s))


##################################

fitnessCalcService = FitnessCalcService()
# fitnessCalcService.calculate_pullups(pullups_col_data)
