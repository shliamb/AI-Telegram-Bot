from get_keys import USER_DB, PASSWORD_DB, DB_NAME
from config import HISTORY_LINE_LIMIT, LIMIT_STAT, HOST, GIFT, PATH_LOGS
from setup_config_logger import setup_logger
logger_db = setup_logger('db', f'{PATH_LOGS}db.log')
import asyncpg
#import asyncio



# Asinc onnection to DB:
async def get_connection():
    connection = await asyncpg.connect(
        host=HOST,
        database=DB_NAME,
        user=USER_DB,
        password=PASSWORD_DB
    )
    return connection





#### USERS TABLE: ####
######################

# Add user:
async def add_user(user_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None 

    user_id = user_data.get("user_id")

    if not user_id:
        logger_db.error("Error add_user: Where is user_id?") 
        return False
    
    if len(user_data) < 1: # if there is at least a user_id, let's go
        logger_db.error("Error add_user: User_data is empty.")
        return False

    for key, value in user_data.items():
        keys_list.append(key)
        values_list.append(value)
        num_list.append(f"${i}")
        i += 1

    keys = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    nums = ", ".join(num_list)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            INSERT INTO users ({keys}) VALUES ({nums})
            ''', 
            *values_list # Оператор распоковки *
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error add_user: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()

# #Add user:
# user_data = {
#     "user_id": 485435943,
#     "name": "Julia",
#     "money": 5.0,
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

        if not result:
            return False

        return dict(*result)
    
    except Exception as e:
        logger_db.error(f"Error read_user: {e}")
    finally:
        if connection:
            await connection.close()

# # # Read user:
# data_user = asyncio.run(read_user(1666495))

# #print(data_user)

# print(data_user.get("user_id"), data_user.get("name"), data_user.get("money"))



# Update user:
async def update_user(user_data):
    keys_list, values_list, i, connection = [], [], 1, None

    user_id = user_data.get("user_id")

    if not user_id:
        logger_db.error("Error update_user: Where is user_id?") 
        return False
    
    if len(user_data) <= 1: # At a minimum, we need user_id + at least one element of the change.
        logger_db.error("Error update_user: User_data is empty or contains a single entry.")
        return False

    for key, value in user_data.items():
        if key != "user_id":
            keys_list.append(f"{key} = ${i}")
            values_list.append(value) #user_data[key])
            i += 1

    update_string = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    values_list.append(user_id)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            UPDATE users SET {update_string} WHERE user_id = ${i};
            ''',
            *values_list
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error update_user: {e}")
        return False
    finally:
        if connection:
            await connection.close()


# # Update user:
# user_data = {
#     "user_id": 485435943,
#     "name": "Juna4",
#     #"money": 5.0,
# }

# confirm = asyncio.run(update_user(user_data))
# print(confirm)

# data_user = asyncio.run(read_user(485435943))
# print(data_user.get("user_id"), data_user.get("name"), data_user.get("money"))







#### STATISTICS TABLE: ####
###########################


# Add statistics:
async def add_statistics(statistics_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None

    user_id = statistics_data.get("user_id")

    if not user_id:
        logger_db.error("Error add_statistics: Where is user_id?") 
        return False
    
    if len(statistics_data) < 1: # if there is at least a user_id, let's go
        logger_db.error("Error add_statistics: Statistics_data is empty.")
        return False

    for key, value in statistics_data.items():
        keys_list.append(key)
        values_list.append(value)
        num_list.append(f"${i}")
        i += 1

    keys = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    nums = ", ".join(num_list)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            INSERT INTO statistics ({keys})
            VALUES ({nums})
            ''', *values_list # Оператор распоковки *
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error add_statistics: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()

# # Add statistics:
# statistics_data = {
#     "user_id": 485435943,
#     "model": "gpt-o",
#     "tokens": 10,
# }

# confirm = asyncio.run(add_statistics(statistics_data))
# print(confirm)



# # Read statistics by user_id:
async def read_statistics(user_id):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            f'''
                SELECT * FROM statistics WHERE user_id = $1 ORDER BY id DESC LIMIT {LIMIT_STAT};
            ''',
            user_id,
        )

        if not result:
            return False

        data = []
        for record in result:
            data.append(dict(record))
        return data
    
    except Exception as e:
        logger_db.error(f"Error read_statistics: {e}")
    finally:
        if connection:
            await connection.close()

# # Read statistics by user_id:
# data_user = asyncio.run(read_statistics(1666495))
# #print(data_user)
# for one in data_user:
#     print(one.get("user_id"), one.get("model"), one.get("tokens"))


# Clear statistics:
async def clear_statistics():
    connection = None

    date_now = None
    # date_now = функция получения даты + какое то условие, что бы давался лимит 3 месяца допустим

    if not date_now:
        logger_db.error("Error date: Today's date has not been received")
        return False

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            DELETE FROM statistics WHERE date < $1;
            ''', 
            (date_now,)
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error clear_statistics {e}")
        return False
    
    finally:
        if connection:
            await connection.close()



# Fast delete Tab Statistic:
async def fast_delete_statistics_tab():

    connection = None

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            TRUNCATE TABLE statistics;
            ''', 
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error fast_delete_statistics_tab {e}")
        return False
    
    finally:
        if connection:
            await connection.close()







#### DISCUSSION TABLE: ####
###########################

# Add discussion:
async def add_discussion(discussion_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None

    user_id = discussion_data.get("user_id")

    if not user_id:
        logger_db.error("Error add_discussion: Where is user_id?") 
        return False
    
    if len(discussion_data) < 1: # if there is at least a user_id, let's go
        logger_db.error("Error add_discussion: Discussion_data is empty.")
        return False

    for key, value in discussion_data.items():
        keys_list.append(key)
        values_list.append(value)
        num_list.append(f"${i}")
        i += 1

    keys = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    nums = ", ".join(num_list)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            INSERT INTO discussion ({keys})
            VALUES ({nums})
            ''', *values_list # Оператор распоковки *
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error add_discussion: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()


# # Add discussion:
# discussion_data = {
#     "timestamp": 33,
#     "user_id": 485435943,
#     "user_question": "Ничего, тебе показалось..",
#     "assistant_response": "Нет, ты явно что то хотел, повтори.",
#     "summarization": True,
# }

# confirm = asyncio.run(add_discussion(discussion_data))
# print(confirm)




# # Read discussion by user_id:
async def read_discussion(user_id):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            f'''
                SELECT * FROM discussion WHERE user_id = $1 ORDER BY id DESC LIMIT {HISTORY_LINE_LIMIT};
            ''',
            user_id,
        )

        if not result:
            return False

        data = []
        for record in result:
            data.append(dict(record))
        return data
    
    except Exception as e:
        logger_db.error(f"Error read_discussion: {e}")
        return False

    finally:
        if connection:
            await connection.close()

# # Read discussion by user_id:
# data_user = asyncio.run(read_discussion(485435943))
# for one in data_user:
#     print(one.get("user_question"), one.get("assistant_response"), one.get("summarization"))


# Clear discussion by id:
async def clear_discussion_by_id(user_id):
    connection = None

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            DELETE FROM discussion WHERE user_id = $1;
            ''', 
            (user_id)
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error clear_discussion by id {e}")
        return False
    
    finally:
        if connection:
            await connection.close()



# Clear discussion:
async def clear_discussion():
    connection = None

    date_now = None
    # date_now = функция получения даты + ~ 2 дня, что бы дать время на использование..

    if not date_now:
        logger_db.error("Error date: Today's date has not been received")
        return False

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            DELETE FROM discussion WHERE date < $1;
            ''', 
            (date_now,)
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error clear_discussion {e}")
        return False
    
    finally:
        if connection:
            await connection.close()




#### METHOD_PAY TABLE: ####
###########################

# Read all methods_pay:
async def read_all_methods_pay():
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM methods_pay;
            '''
        )

        if not result:
            logger_db.error("The methodt pay is empty, sorry.")
            return False

        data = []
        for record in result:
            data.append(dict(record))
        return data
    
    except Exception as e:
        logger_db.error(f"Error read_all_methods_pay: {e}")
        return False
    finally:
        if connection:
            await connection.close()

# data = asyncio.run(read_all_methods_pay())
# print(data)

# if data:
#     for n in data:
#         print(n.get("id"))
#         #print(n)

# Read one methods_pay by title:
async def read_one_methods_pay(title: str):
    connection = None
    try:
        if type(title) != str:
            logger_db.error("Error: input data is not str (title method pay.)")
            return False

        if not title:
            logger_db.error("Error: Title method pay is Empty or None.")
            return False

        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM methods_pay WHERE title_method_pay = $1;
            ''',
            title,
        )

        if not result:
            return False

        return dict(*result)

    except Exception as e:
        logger_db.error(f"Error read_one_methods_pay: {e}")
        return False
    finally:
        if connection:
            await connection.close()


# Read one methods_pay by id:
async def read_one_methods_pay_by_id(id: int):
    connection = None
    try:
        if type(id) != int:
            logger_db.error("Error: input data is not int (id method pay.)")
            return False

        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM methods_pay WHERE id = $1;
            ''',
            id,
        )

        if not result:
            return False

        return dict(*result)
    
    except Exception as e:
        logger_db.error(f"Error read_one_methods_pay_by_id: {e}")
        return False
    finally:
        if connection:
            await connection.close()


# Read one methods_pay by use == True:
async def read_one_methods_pay_by_use(place_of_use):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            f'''
                SELECT * FROM methods_pay WHERE {place_of_use} = $1;
            ''',
            True,
        )

        if not result:
            return False

        return dict(*result)
    
    except Exception as e:
        logger_db.error(f"Error read_one_methods_pay_by_use: {e}")
        return False
    finally:
        if connection:
            await connection.close()


# Read one method pay by USE:
# i = "use_mircard"
# data = asyncio.run(read_one_methods_pay_by_use(i))
# print(data)
# print(data.get(f"counts"))


# Deleted one methods_pay:
async def deleted_one_methods_pay(id):
    connection = None
    try:
        if type(id) != int:
            logger_db.error("Error: input data is not int (id method pay.)")
            return False

        if not id:
            logger_db.error("Error: Title method pay is Empty or None.")
            return False

        connection = await get_connection()
        await connection.execute(
            '''
                DELETE FROM methods_pay WHERE id = $1;
            ''',
            id,
        )

        return True
    
    except Exception as e:
        logger_db.error(f"Error deleted_one_methods_pay: {e}")
        return False
    finally:
        if connection:
            await connection.close()


# Add methods_pay:
async def add_methods_pay(pay_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None

    if len(pay_data) <= 1: 
        logger_db.error("Error: User_data is empty.")
        return False

    for key, value in pay_data.items():
        keys_list.append(key)
        values_list.append(value)
        num_list.append(f"${i}")
        i += 1

    keys = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    nums = ", ".join(num_list)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            INSERT INTO methods_pay ({keys}) VALUES ({nums})
            ''', 
            *values_list # Оператор распоковки *
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error add_methods_pay: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()



# Update methods_pay by id:
async def update_methods_pay(pay_data):
    keys_list, values_list, i, connection = [], [], 1, None

    id = pay_data.get("id")

    if not id:
        logger_db.error("Error update_methods_pay: Where is id?") 
        return False
    
    if len(pay_data) <= 1: # At a minimum, we need id + at least one element of the change.
        logger_db.error("Error update_methods_pay: pay_data is empty or contains a single entry.")
        return False

    for key, value in pay_data.items():
        if key != "id":
            keys_list.append(f"{key} = ${i}")
            values_list.append(value) #user_data[key])
            i += 1

    update_string = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    values_list.append(id)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            UPDATE methods_pay SET {update_string} WHERE id = ${i};
            ''', 
            *values_list
        )
        return True
    
    
    except Exception as e:
        logger_db.error(f"Error update_methods_pay: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()




# # Add methods_pay:
# pay_data = {
#     # "date": ,
#     "title_method_pay": "White",
#     "counts": 1,
#     "method_pay": "С вас 3 пирожка и это официально, я нарисую чек!",
# }

# Deleted:
# confirm = asyncio.run(deleted_one_methods_pay("White"))
# print(confirm)

# # Add:
# confirm = asyncio.run(add_methods_pay(pay_data))
# print(confirm)

# Read all:
# data = asyncio.run(read_all_methods_pay())
# print(data)

# # Read one method pay by USE:
# data = asyncio.run(read_one_methods_pay_by_use())
# print(data)

# # Update row use to id:
# pay_data = {
#     "id": 1,
#     "use": True,
# }
# data1 = asyncio.run(update_methods_pay(pay_data))
# print(data1)

# # Read by id:
# data = asyncio.run(read_one_methods_pay_by_id(1))
# print(data)

# # Read for title record:
# data = asyncio.run(read_one_methods_pay("White"))
# print(data)





#### PAYMENTS TABLE: ####
#########################


# # Read all payments for one user_id:
# async def read_all_payments_for_user_id(user_id):
#     connection = None
#     try:
#         connection = await get_connection()
#         result = await connection.fetch(
#             '''
#                 SELECT * FROM payments WHERE user_id = $1;
#             ''',
#             user_id
#         )

#         if not result:
#             print(f"User {user_id} not pay.")
#             return False

#         data = []
#         for record in result:
#             data.append(dict(record))

#         # if len(data) == 1:
#         #     data = dict(*result)

#         return data
    
#     except Exception as e:
#         print(f"Error read_all_payments_for_user_id: {e}")
#         return False
#     finally:
#         if connection is not None:
#             await connection.close()


# Read all payments:
async def read_all_payments():
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM payments;
            '''
        )

        if not result:
            logger_db.error("Users not pay.")
            return False

        data = []
        for record in result:
            data.append(dict(record))

        # if len(data) == 1:
        #     data = dict(*result)

        return data
    
    except Exception as e:
        logger_db.error(f"Error read_all_payments: {e}")
        return False
    finally:
        if connection:
            await connection.close()


# # Read all payments:
# data = asyncio.run(read_all_payments())
# print(data)


# Add payments:
async def add_payments(payments):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None

    if len(payments) <= 1: 
        logger_db.error("Error: User_data is empty.")
        return False
    
    if payments.get("user_id") is None: 
        logger_db.error("Error: User_id is empty.")
        return False

    for key, value in payments.items():
        keys_list.append(key)
        values_list.append(value)
        num_list.append(f"${i}")
        i += 1

    keys = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    nums = ", ".join(num_list)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            INSERT INTO payments ({keys}) VALUES ({nums})
            ''', 
            *values_list # Оператор распоковки *
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error add_payments: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()


# Deleted all payments:
async def deleted_all_payments():
    connection = None
    try:
        connection = await get_connection()
        await connection.execute(
            '''
                DELETE FROM payments;
            '''
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error deleted_all_payments: {e}")
        return False
    finally:
        if connection:
            await connection.close()


# # Add payments:
# payments = {
#     "user_id": 1666495,
#     # "date": ,
#     "title_method_pay": "White",
#     "sum": 126,
# }

# # Add payments:
# data = asyncio.run(add_payments(payments))
# print(data)

# # Resd one payments for her user_id:
# data = asyncio.run(read_all_payments_for_user_id(1666495))
# print(data)

# # Deleted all records payments:
# data = asyncio.run(deleted_all_payments())
# print(data)

# # Read all payments:
# data = asyncio.run(read_all_payments())
# print(data)



#### ADMIN PARSE TABLE: ####
###########################

# Read all users:
async def read_all_users():
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM users;
            '''
        )

        if not result:
            return False

        data = []
        for record in result:
            data.append(dict(record))

        return data
    
    except Exception as e:
        logger_db.error(f"Error read_all_users: {e}")
    finally:
        if connection:
            await connection.close()


# data_all_users = asyncio.run(read_all_users())
# print(data_all_users)

# for user in data_all_users:
#     print(user.get("user_id"), user.get("name"), user.get("money"))





# Read all users whu pay and have money:
async def json_old_users():
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM users WHERE paid > $1 OR money > $2;
            ''',
            0, GIFT
        )

        if not result:
            return False

        data = []
        for record in result:
            data.append(dict(record))

        return data
    
    except Exception as e:
        logger_db.error(f"Error json_old_users: {e}")
        return False
    finally:
        if connection:
            await connection.close()


# print(asyncio.run(json_old_users()))








# Fast delete ALL Tabs:
async def drop_all_tables_and_reset_schema():
    connection = None
    try:
        connection = await get_connection()
        # Удаляем схему public со всеми объектами и создаём её заново
        await connection.execute("DROP SCHEMA public CASCADE;")
        await connection.execute("CREATE SCHEMA public;")
        # Возвращаем стандартные права (без указания конкретной роли)
        await connection.execute("GRANT ALL ON SCHEMA public TO PUBLIC;")
        return True
    except Exception as e:
        logger_db.error(f"Error in drop_all_tables_and_reset_schema: {e}")
        return False
    finally:
        if connection:
            await connection.close()





# from datetime import datetime, timezone, timedelta

# Read all users to Assist Admin:
# async def assist_admin_db_users() -> str:
#     connection = None
#     try:
#         connection = await get_connection()
#         all_records = await connection.fetch(
#             '''
#                 SELECT user_id, name, full_name, first_name, last_name, last_visit, paid, money  
#                 FROM users;
#             '''
#         )

#         if not all_records:
#             return False

#         data = ""

#         for r in all_records:
#             # Collect unique name parts
#             name_parts = {r.get("name"), r.get("full_name"), r.get("first_name"), r.get("last_name")}
#             name = ' '.join(filter(None, name_parts))

#             # Format date and time
#             dt = r.get("last_visit")
#             if dt:
#                 day_time = f"{dt.strftime("%Y-%m-%d")} {dt.strftime("%H:%M")}"
#             else:
#                 day_time = "N/A"

#             # Short line
#             data += (
#                 f"ID: {r['user_id']}, Name: '{name}', "
#                 f"Last visit: {day_time}, "
#                 f"Payments: {r.get('paid', 0)}, "
#                 f"Balance $: {round(r.get('money', 0), 2)};\n"
#             )

#         return data
    
#     except Exception as e:
#         logging.error(f"Error async def assist_admin_db_users(): {e}")
#     finally:
#         if connection is not None:
#             await connection.close()











# #### ADMIN TABLE: ####
# ######################

# # Add data admin:
# async def add_data_admin(admin_data):
#     keys_list, values_list, num_list, i, connection = [], [], [], 1, None 

#     user_id = admin_data.get("user_id")

#     if not user_id:
#         logging.error("Error add_user: Where is user_id?") 
#         return False
    
#     if len(admin_data) < 1: # if there is at least a user_id, let's go
#         logging.error("Error add_user: admin_data is empty.")
#         return False

#     for key, value in admin_data.items():
#         keys_list.append(key)
#         values_list.append(value)
#         num_list.append(f"${i}")
#         i += 1

#     keys = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
#     nums = ", ".join(num_list)

#     try:
#         connection = await get_connection()
#         await connection.execute(
#             f'''
#             INSERT INTO admin_data ({keys}) VALUES ({nums})
#             ''', 
#             *values_list # Оператор распоковки *
#         )
#         return True
    
#     except Exception as e:
#         logging.error(f"Error add_data_admin: {e}")
#         return False
    
#     finally:
#         if connection is not None:
#             await connection.close()


# # Read Data Admin:
# async def read_admin_data(user_id):
#     connection = None
#     try:
#         connection = await get_connection()
#         result = await connection.fetch(
#             '''
#                 SELECT * FROM admin_data WHERE user_id = $1;
#             ''',
#             user_id,
#         )

#         if not result:
#             return False

#         return dict(*result)
    
#     except Exception as e:
#         logging.error(f"Error read_admin_data: {e}")
#     finally:
#         if connection is not None:
#             await connection.close()





# # Update Admin Data:
# async def update_admin_data(admin_data):
#     keys_list, values_list, i, connection = [], [], 1, None

#     user_id = admin_data.get("user_id")

#     if not user_id:
#         logging.error("Error update_user: Where is user_id?") 
#         return False
    
#     if len(admin_data) <= 1: # At a minimum, we need user_id + at least one element of the change.
#         logging.error("Error update_user: admin_data is empty or contains a single entry.")
#         return False

#     for key, value in admin_data.items():
#         if key != "user_id":
#             keys_list.append(f"{key} = ${i}")
#             values_list.append(value)
#             i += 1

#     update_string = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
#     values_list.append(user_id)

#     try:
#         connection = await get_connection()
#         await connection.execute(
#             f'''
#             UPDATE admin_data SET {update_string} WHERE user_id = ${i};
#             ''',
#             *values_list
#         )
#         return True
    
#     except Exception as e:
#         logging.error(f"Error update_admin_data: {e}")
#         return False
#     finally:
#         if connection is not None:
#             await connection.close()