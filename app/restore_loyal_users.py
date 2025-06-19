# Base:
# import asyncio
from config import PATH_LOGS
from setup_config_logger import setup_logger
logger_db = setup_logger('db', f'{PATH_LOGS}db.log')
import json
#import uuid
from datetime import datetime
# System:
from worker_db import add_user, add_methods_pay #, update_user



metods_pay = [
    {
        'date': datetime(2024, 10, 14, 0, 8, 38), 
        'counts': 0, 
        'use_sbp_transfer': None, 
        'use_mastercard': None, 
        'use_visa': None, 
        'use_mircard': True, 
        'use_cripto': None, 
        'use_sms': None, 
        'use_stars': None, 
        'use_telegram': None, 
        'use_digital': None, 
        'title_method_pay': 'OZON  CARD NUMBER', 
        'method_pay_ru': 'Переведите на карту банка OZON по номеру карты  2204 2402 7076 3321 из приложения своего банка. На имя Александр В. сумму вводимую ранее.', 
        'method_pay_en': "Transfer to the OZON Bank card by card number 2204 2402 7076 3321 from your bank's application. In the name of Alexander V. the amount entered earlier."
    },  
    {
        'date': datetime(2024, 10, 14, 0, 9, 11), 
        'counts': 0, 
        'use_sbp_transfer': None, 
        'use_mastercard': True, 
        'use_visa': None, 
        'use_mircard': None, 
        'use_cripto': None, 
        'use_sms': None, 
        'use_stars': None, 
        'use_telegram': None, 
        'use_digital': None, 
        'title_method_pay': 'Jusan', 
        'method_pay_ru': 'Переведите на карту банка JUSAN по номеру карты  5395 4599 0505 1850 из приложения своего банка. На имя Александр В. сумму вводимую ранее.', 
        'method_pay_en': "Transfer to a JUSAN Bank card using the card number 5395 4599 0505 1850 from your bank's application. In the name of Alexander V. the amount entered earlier."
}
]



def datetime_to_db(value):
    '''to  datetime.datetime(2024, 10, 14, 0, 8, 38)'''
    try:
        return datetime.fromisoformat(value)  # Пробуем распарсить
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")  # Если не ISO-формат, пробуем другой формат



async def restore_loyal_users_to_db(file_path):

    """Импортирует постоянных клиентов из JSON, добавляет или обновляет в БД."""

    qty_add_usr = 0
    err_add_usr = 0

    qty_met_pay = 0
    err_met_pay = 0



    # Открытие файла и в файл:
    with open(file_path, "r") as file:

        if not file:
            return False

        users_json = json.load(file) # В dict

    # Списки для обработки данных:
    list_keys_date = ["last_visit"]

    # Users Table:
    for user_records in users_json.values():

        try:
            # Сереализация..
            clear_data_user = {} 
            for key, value in user_records.items():
                if key in list_keys_date:
                    clear_data_user[key] = datetime_to_db(value)
                else:
                    clear_data_user[key] = value

            if await add_user(clear_data_user):
                qty_add_usr += 1

        except Exception as err:
            err_add_usr += 1
            logger_db.error(f"Fail update user_id: {clear_data_user.get('user_id')}, reason: {err}")
        


    # Metods_pay Table:
    for metod in metods_pay:
        try:
            if await add_methods_pay(metod):
                qty_met_pay += 1
        except Exception as err:
            logger_db.error(f"Fail update metod pay: {metod}, reason: {err}")
            err_met_pay += 1


    return {"status": "good", "added users": qty_add_usr, "errors users": err_add_usr, "added metods pay": qty_met_pay, "errors metods pay": err_met_pay}
    

    



# asyncio.run(restore_loyal_users_to_db())
#print(asyncio.run(restore_loyal_users_to_db("./json/user_best.json")))
