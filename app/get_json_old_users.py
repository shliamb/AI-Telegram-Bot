# System:
from worker_db import json_old_users
from config import PATH_JSON_USERS, PATH_LOGS
# Base:
#import asyncio
import os
import json
import uuid
from datetime import datetime
from setup_config_logger import setup_logger
logger_db = setup_logger('db', f'{PATH_LOGS}db.log')






def extended_encoder(obj):
    '''Кастомный сериализатор для нестандартных типов данных'''
    if isinstance(obj, uuid.UUID):  # Обрабатываем UUID
        return str(obj)
    
    elif isinstance(obj, datetime):  # Обрабатываем дату/время
        return obj.isoformat()
    
    elif hasattr(obj, '__dict__'):  # Обрабатываем объекты с атрибутами
        return obj.__dict__
    
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")






async def get_json_old_users_to_db():
    '''Собирает из базы всех пользователей кто хоть раз платил или счет больше тестовой суммы'''

    try:
        users_data = await json_old_users()

        if not users_data:
            return False

        json_users_data = {}
        for user in users_data:
            id = user.get("user_id")
            json_users_data[id] = user

        # Создаем имя файла с текущей датой-временем
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{PATH_JSON_USERS}users_data_{timestamp}.json"
        
        # Полный путь к файлу в рабочей директории
        filepath = os.path.join(os.getcwd(), filename)
        
        # Сохраняем с обработкой специальных типов
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                json_users_data, 
                f, 
                ensure_ascii=False, 
                indent=4,
                default=extended_encoder
            )
        return filepath

    except Exception as e:
        logger_db.error(f"Error save file to JSON: {e}")
        return False
    
# asyncio.run(get_json_old_users_to_db())