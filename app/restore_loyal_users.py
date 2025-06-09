# Base:
# import asyncio
from config import LOG_CONFIG_BOT
import logging
logging.basicConfig(**LOG_CONFIG_BOT)
import json
import datetime
# System:
from worker_db import add_user, update_user, add_methods_pay



metods_pay = [
    {
        'date': datetime.datetime(2024, 10, 14, 0, 8, 38), 
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
        'date': datetime.datetime(2024, 10, 14, 0, 9, 11), 
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



async def restore_loyal_users_to_db():

    """Импортирует постоянных клиентов из JSON, добавляет или обновляет в БД."""

    qty_add_usr = 0
    err_add_usr = 0

    qty_met_pay = 0
    err_met_pay = 0

    try:

        # Add Loyalti Users:
        with open("./json/loyal_users.json", "r") as file:
            users_json = json.load(file) # В dict

        for user_id, user_data in users_json.items():
            data = {**user_data, "user_id": int(user_id)}

            try:
                if await add_user(data):
                    qty_add_usr += 1
            except Exception:
                try:
                    if await update_user(data):
                        qty_add_usr += 1
                except Exception as err:
                    logging.error(f"Fail update user_id: {user_id}, reason: {err}")
                    err_add_usr += 1

        # Metods Pay:
        for metod in metods_pay:
            try:
                if await add_methods_pay(metod):
                    qty_met_pay += 1
            except Exception as err:
                logging.error(f"Fail update metod pay: {metod}, reason: {err}")
                err_met_pay += 1


        return {"status": "good", "added users": qty_add_usr, "errors users": err_add_usr, "added metods": qty_met_pay, "errors metods": err_met_pay}
    
    except Exception as err:
        logging.critical(f"Fail open or handle file: {err}")
        return {"status": f"bad: {err}", "added users": qty_add_usr, "errors users": err_add_usr, "added metods": qty_met_pay, "errors metods": err_met_pay}


    



# asyncio.run(restore_loyal_users_to_db())