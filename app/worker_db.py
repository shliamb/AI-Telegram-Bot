from get_keys import TELEGRAM_BOT_TOKEN, USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI, USER_DB, PASWORD_DB, ADMIN_ID
import psycopg2




try:
    # Подключение к базе данных
    connection = psycopg2.connect(host="localhost", database="my_database", user=USER_DB, password=PASWORD_DB)
    
    cursor = connection.cursor()

    # Проверка существования таблиц
    check_tables_query = '''
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema='public';
    '''

    cursor.execute(check_tables_query)
    tables = cursor.fetchall()

    print("Существующие таблицы:")
    for table in tables:
        print(table[0])



except Exception as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    # Закрытие курсора и соединения с базой данных
    if cursor:
        cursor.close()
        
    if connection:
        connection.close()