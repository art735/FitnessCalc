import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from FitnessCalcService import FitnessCalcService, ExerciseType

# Указываем необходимые API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

credentials_json_filename = r"E:\Languages\English\SVN repo\Python software\FitnessCalc\credentials.json"
# Загружаем файл с ключами для авторизации
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json_filename, scope)

# Авторизуемся с помощью gspread
client = gspread.authorize(creds)

# Открываем Google Sheets по названию
spreadsheet = client.open("Режим дня (питание и спорт)")
sheet = spreadsheet.worksheet('2024.09 - сентябрь')  # TODO: вычислять имя динамически!

class FitnessCalcMain:
    def __init__(self):
        self.fitnessCalcService = FitnessCalcService()

    def calculate(self):
        # Получаем данные из диапазона столбцов
        data = sheet.batch_get(['C:C', 'D:D'])

        # pull-ups - подтягивания на турнике
        pullups_column_data = data[0]
        # dips - отжимания на брусьях
        dips_column_data = data[1]

        pullups_current_state, pullups_average = self.fitnessCalcService.calculate_exercises(pullups_column_data, ExerciseType.PULL_UPS)
        dips_current_state, dips_average = self.fitnessCalcService.calculate_exercises(dips_column_data, ExerciseType.DIPS)

        print(f'Current pull-ups: {pullups_current_state}')
        print(f'Current dips: {dips_current_state}')

        print(f'\nThis month average:\nPull-ups: {pullups_average}\nDips: {dips_average}')


###################################

fitnessCalcMain = FitnessCalcMain()
fitnessCalcMain.calculate()

