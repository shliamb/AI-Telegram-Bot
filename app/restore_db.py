from get_keys import USER_DB, PASSWORD_DB, DB_NAME
from config import HOST, PATH_LOGS
from setup_config_logger import setup_logger
logger_db = setup_logger('db', f'{PATH_LOGS}db.log')
# from general_functions import day_utcnow, unformat_date
import subprocess
import os
# import asyncio



async def restore_db(file_path):
    # 1. Используем правильное имя хоста (то же, что в terminate_command)
    db_host = HOST  # Используем тот же хост, что и для psql
    
    # Команда для завершения подключений (кроме текущего)
    terminate_command = [
        'psql',
        '-h', db_host,
        '-p', '5432',
        '-U', USER_DB,
        '-d', 'postgres',  # Подключаемся к системной БД
        '-c', f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='{DB_NAME}' AND pid <> pg_backend_pid();"
    ]
    
    # Команда для очистки БД
    clear_command = [
        'psql',
        '-h', db_host,
        '-p', '5432',
        '-U', USER_DB,
        '-d', DB_NAME,
        '-c', "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    ]
    
    # Команда для восстановления
    pg_restore_command = [
        'pg_restore',
        '-h', db_host,  # Используем тот же хост
        '-p', '5432',
        '-U', USER_DB,
        '-d', DB_NAME,
        '-Fc',  # Указываем формат (custom)
        file_path
    ]
    
    try:
        env = {**os.environ, 'PGPASSWORD': PASSWORD_DB}
        
        # 1. Завершаем подключения
        logger_db.info("Terminating existing connections...")
        result = subprocess.run(terminate_command, env=env, capture_output=True, text=True)
        logger_db.info(result.stdout)
        
        # 2. Очищаем БД
        logger_db.info("Clearing database...")
        subprocess.run(clear_command, env=env, check=True)
        
        # 3. Восстанавливаем из бэкапа
        logger_db.info("Restoring database...")
        subprocess.run(pg_restore_command, env=env, check=True)
        
        logger_db.info("Database restore completed successfully.")
        return True
    
    except subprocess.CalledProcessError as e:
        logger_db.error(f"Command failed: {e}\nOutput: {e.stdout}\nError: {e.stderr}")
        return False
    except Exception as e:
        logger_db.error(f"An error occurred: {str(e)}")
        return False



#
# Очищает имеющуюся базу и восстанавливает из копии находящейся на сервере по адресу переданному по адресу и имени файла - file_path
# У меня чет на Linux pg_dump не обновляется выше 15.5, потому я поставил в docker-compose.yml
# версию 15.5 PostgreSQL, если на сервере будет выше, то в файле просто поставить Last img Postgres.
#