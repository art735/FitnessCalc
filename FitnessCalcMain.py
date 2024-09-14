import os

import gspread
from oauth2client import service_account

from FitnessCalcService import FitnessCalcService, ExerciseType

# Указываем необходимые API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]


# Файл credentials.json – это файл, содержащий учётные данные, которые нужны для аутентификации и доступа к Google API.
# В контексте работы с Google Sheets API или другими сервисами Google, он используется для предоставления вашему
# приложению прав на доступ к ресурсам Google от имени пользователя.
# Данный файл является конфиденциальным и его нельзя публиковать (в том числе и в GitHub-репозиторий).
# Файл credentials.json хранится на локальном компьютере + вручную подкладывается на сервер (напр., Google Colab).
# В тексте программы путь к файлу credentials.json вычитывается из переменной окружения (должна быть настроена как
# на локальном компьютере, так и на сервере Google Colab) и таким образом происходит безопасная и абстрактная работа
# с этим файлом (без засвечивания локальных путей в коде).


# Лучший способ безопасно хранить и использовать конфиденциальные данные — через переменные окружения.
# Загрузите файл credentials.json на сервер (или в защищённое хранилище).
# В вашем коде замените прямую загрузку файла на использование переменной окружения для получения пути к файлу

# Предполагается, что путь к credentials.json установлен в переменной окружения
credentials_filename = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if credentials_filename:
    credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(credentials_filename)
else:
    raise FileNotFoundError("Environment variable 'GOOGLE_APPLICATION_CREDENTIALS' is not set.")

# credentials_json_filename = r"E:\IT\Programming\Python\! My Projects\FitnessCalc\credentials.json"
# # Загружаем файл с ключами для авторизации
# creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json_filename, scope)

# В Google Colab переменные окружения можно установить следующим образом:
# import os
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/credentials.json"

# Авторизуемся с помощью gspread
client = gspread.authorize(credentials)

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

        pullups_current_state, pullups_average = self.fitnessCalcService.calculate_exercises(pullups_column_data,
                                                                                             ExerciseType.PULL_UPS)
        dips_current_state, dips_average = self.fitnessCalcService.calculate_exercises(dips_column_data,
                                                                                       ExerciseType.DIPS)

        print(f'Current pull-ups: {pullups_current_state}')
        print(f'Current dips: {dips_current_state}')

        print(f'\nThis month average:\nPull-ups: {pullups_average}\nDips: {dips_average}')


###################################

fitnessCalcMain = FitnessCalcMain()
fitnessCalcMain.calculate()

