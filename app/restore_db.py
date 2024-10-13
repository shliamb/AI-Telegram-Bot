from get_keys import USER_DB, PASSWORD_DB, DB_NAME
from config import BACKUP_PATH, TIME_CORRECTION
from general_functions import day_utcnow, unformat_date
import subprocess
import logging
# import asyncio



async def restore_db(file_path):
                                                            # localhost  app_postgres
    terminate_command = f'PGPASSWORD={PASSWORD_DB} psql -h app_postgres -p 5432 -U {USER_DB} -d {DB_NAME} -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname=\'{DB_NAME}\';"'

    clear_command = f'PGPASSWORD={PASSWORD_DB} psql -h app_postgres -p 5432 -U {USER_DB} -d {DB_NAME} -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"'

    pg_restore_command = f'PGPASSWORD={PASSWORD_DB} pg_restore -h app_postgres -p 5432 -U {USER_DB} -d {DB_NAME} {file_path}'
    
    try:
        subprocess.run(terminate_command, shell=True) # Формирование команды для завершения активных сеансов

        subprocess.run(clear_command, shell=True) # Формирование команды для удаления базы данных

        subprocess.run(pg_restore_command, shell=True) # Восстановления базы данных из резервной копии с помощью pg_restore, выполнение команды через subprocess
        
        logging.info("Database restore completed successfully.")
        print("Database restore completed successfully.")
        return True
    
    except Exception as e:
        logging.info(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return False



#
# Очищает имеющуюся базу и восстанавливает из копии находящейся на сервере по адресу переданному по адресу и имени файла - file_path
# У меня чет на Linux pg_dump не обновляется выше 15.5, потому я поставил в docker-compose.yml
# версию 15.5 PostgreSQL, если на сервере будет выше, то в файле просто поставить Last img Postgres.
#