from get_keys import USER_DB, PASSWORD_DB, DB_NAME
from config import BACKUP_PATH, TIME_CORRECTION
from general_functions import day_utcnow, unformat_date
import subprocess
import logging
import asyncio



async def backup_db():
    # Name file
    date = await day_utcnow(TIME_CORRECTION)
    dict_date = await unformat_date(date)

    backup_filename = f'Db_backup_{dict_date.get("day")}_{dict_date.get("time")}.sql'                                           
    pg_dump_command = f'PGPASSWORD={PASSWORD_DB} pg_dump -h localhost -p 5432 -U {USER_DB} -d {DB_NAME} -F c -f {BACKUP_PATH}{backup_filename}' # В бинарный формат # postgres  localhost


    try:
        subprocess.run(pg_dump_command, shell=True)
        logging.info("Backup Data Base is Completed.")
        print("Backup Data Base is Completed.")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"Error when creating a backup: {e}")
        print("Backup error")
        return False



# confirm = asyncio.run(backup_db())
# print(confirm)