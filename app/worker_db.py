from get_keys import TELEGRAM_BOT_TOKEN, USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI, USER_DB, PASSWORD_DB, ADMIN_ID
import asyncpg
import asyncio
# import json



# Asinc onnection to DB:
async def get_connection():
    connection = await asyncpg.connect(
        host="localhost",
        database="my_database",
        user=USER_DB,
        password=PASSWORD_DB
    )
    return connection









# Users Table:


# Add user:
async def add_user(user_data):
    connection = None

    try:
        connection = await get_connection()
        await connection.execute(
            '''
            INSERT INTO users (user_id, name, money)
            VALUES ($1, $2, $3)
            ''', 
            user_data.get("user_id"), 
            user_data.get("name"), 
            user_data.get("money")
        )
        return True
    
    except Exception as e:
        print(f"Error add_user: {e}")
        return False
    
    finally:
        if connection is not None:
            await connection.close()

# # Add user:
# user_data = {
#     "user_id": 185435943,
#     "name": "Jonish",
#     "money": 4.0,
# }

# confirm = asyncio.run(add_user(user_data))
# print(confirm)





# Read user:
async def read_user(user_id):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM users WHERE user_id = $1;
            ''',
            user_id,
        )
        for record in result:
            data = dict(record)
        return data 
    
    except Exception as e:
        print(f"Error read_user: {e}")
    finally:
        if connection is not None:
            await connection.close()

# Read user:
# data_user = asyncio.run(read_user(185435943))
# print(data_user.get("user_id"), data_user.get("name"), data_user.get("money"))







# Update user:
async def update_user(user_data):
    updates, values, i, connection = [], [], 0, None

    user_id = user_data.get("user_id")
    if not user_id:
        print("Error update_user: Where is user_id?")
        return False
    
    if not user_data:
        print("Error update_user: User_data is empty.")
        return False

    for key, value in user_data.items():
        if key != "user_id":
            i += 1
            updates.append(f"{key} = ${i}")
            values.append(user_data[key])

    if updates:
        update_string = ", ".join(updates)

    values.append(user_id)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            UPDATE users SET {update_string} WHERE user_id = ${i + 1};
            ''',
            *values
        )
        return True
    
    except Exception as e:
        print(f"Error update_user: {e}")
        return False
    finally:
        if connection is not None:
            await connection.close()




# Update user:
user_data = {
    "user_id": 185435943,
    "name": "Juna4",
    #"money": 3.0,
}

confirm = asyncio.run(update_user(user_data))
print(confirm)

data_user = asyncio.run(read_user(185435943))
print(data_user.get("user_id"), data_user.get("name"), data_user.get("money"))












































# try:
#     # Подключение к базе данных
#     connection = psycopg2.connect(host="localhost", database="my_database", user=USER_DB, password=PASWORD_DB)
    
#     cursor = connection.cursor()

#     # Проверка существования таблиц
#     check_tables_query = '''
#     SELECT table_name 
#     FROM information_schema.tables 
#     WHERE table_schema='public';
#     '''

#     cursor.execute(check_tables_query)
#     tables = cursor.fetchall()

#     print("Существующие таблицы:")
#     for table in tables:
#         print(table[0])



# except Exception as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     # Закрытие курсора и соединения с базой данных
#     if cursor:
#         cursor.close()
        
#     if connection:
#         connection.close()