from get_keys import USER_DB, PASSWORD_DB
import asyncpg
import asyncio



# Asinc onnection to DB:
async def get_connection():
    connection = await asyncpg.connect(
        host="localhost",
        database="my_database",
        user=USER_DB,
        password=PASSWORD_DB
    )
    return connection



#### USERS TABLE: ####
#######################

# Add user:
async def add_user(user_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None

    user_id = user_data.get("user_id")

    if not user_id:
        print("Error add_user: Where is user_id?") 
        return False
    
    if len(user_data) < 1: # if there is at least a user_id, let's go
        print("Error add_user: User_data is empty.")
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
        print(f"Error add_user: {e}")
        return False
    
    finally:
        if connection is not None:
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
        print(f"Error read_user: {e}")
    finally:
        if connection is not None:
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
        print("Error update_user: Where is user_id?") 
        return False
    
    if len(user_data) <= 1: # At a minimum, we need user_id + at least one element of the change.
        print("Error update_user: User_data is empty or contains a single entry.")
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
        print(f"Error update_user: {e}")
        return False
    finally:
        if connection is not None:
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
        print("Error add_statistics: Where is user_id?") 
        return False
    
    if len(statistics_data) < 1: # if there is at least a user_id, let's go
        print("Error add_statistics: Statistics_data is empty.")
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
        print(f"Error add_statistics: {e}")
        return False
    
    finally:
        if connection is not None:
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
            '''
                SELECT * FROM statistics WHERE user_id = $1 ORDER BY id DESC LIMIT 100;
            ''',
            user_id,
        )

        if not result:
            return False

        data = []
        for record in result:
            data.append(dict(record))

        if len(data) == 1:
            data = dict(*result)

        return data
    
    except Exception as e:
        print(f"Error read_statistics: {e}")
    finally:
        if connection is not None:
            await connection.close()

# # Read statistics by user_id:
# data_user = asyncio.run(read_statistics(1666495))
# #print(data_user)
# for one in data_user:
#     print(one.get("user_id"), one.get("model"), one.get("tokens"))


# Clear statistics:
async def clear_statistics():

    date_now = None
    # date_now = функция получения даты + какое то условие, что бы давался лимит 3 месяца допустим

    if not date_now:
        print("Error date: Today's date has not been received")
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
        print(f"Error clear_statistics {e}")
        return False
    
    finally:
        if connection is not None:
            await connection.close()











#### DISCUSSION TABLE: ####
###########################

# Add discussion:
async def add_discussion(discussion_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None

    user_id = discussion_data.get("user_id")

    if not user_id:
        print("Error add_discussion: Where is user_id?") 
        return False
    
    if len(discussion_data) < 1: # if there is at least a user_id, let's go
        print("Error add_discussion: Discussion_data is empty.")
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
        print(f"Error add_discussion: {e}")
        return False
    
    finally:
        if connection is not None:
            await connection.close()


# # Add discussion:
# discussion_data = {
#     "user_id": 485435943,
#     "user_say": "Ничего, тебе показалось..",
#     "model_say": "Нет, ты явно что то хотел, повтори.",
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
            '''
                SELECT * FROM discussion WHERE user_id = $1 ORDER BY id DESC LIMIT 10;
            ''',
            user_id,
        )

        if not result:
            return False

        data = []
        for record in result:
            data.append(dict(record))

        if len(data) == 1:
            data = dict(*result)

        return data
    
    except Exception as e:
        print(f"Error read_discussion: {e}")
    finally:
        if connection is not None:
            await connection.close()

# # Read discussion by user_id:
# data_user = asyncio.run(read_discussion(485435943))
# for one in data_user:
#     print(one.get("user_say"), one.get("model_say"), one.get("summarization"))


# Clear discussion:
async def clear_discussion():

    date_now = None
    # date_now = функция получения даты + ~ 2 дня, что бы дать время на использование..

    if not date_now:
        print("Error date: Today's date has not been received")
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
        print(f"Error clear_discussion {e}")
        return False
    
    finally:
        if connection is not None:
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
            print("The methodt pay is empty, sorry.")
            return False

        data = []
        for record in result:
            data.append(dict(record))

        if len(data) == 1:
            data = dict(*result)
            
        return data
    
    except Exception as e:
        print(f"Error read_all_methods_pay: {e}")
        return False
    finally:
        if connection is not None:
            await connection.close()



# Read one methods_pay by title:
async def read_one_methods_pay(title: str):
    connection = None
    try:
        if type(title) != str:
            print("Error: input data is not str (title method pay.)")
            return False

        if not title:
            print("Error: Title method pay is Empty or None.")
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
        print(f"Error read_one_methods_pay: {e}")
        return False
    finally:
        if connection is not None:
            await connection.close()


# Read one methods_pay by id:
async def read_one_methods_pay_by_id(id: int):
    connection = None
    try:
        if type(id) != int:
            print("Error: input data is not int (id method pay.)")
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
        print(f"Error read_one_methods_pay_by_id: {e}")
        return False
    finally:
        if connection is not None:
            await connection.close()


# Read one methods_pay by use == True:
async def read_one_methods_pay_by_use(i):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            f'''
                SELECT * FROM methods_pay WHERE use_{i} = $1;
            ''',
            True,
        )

        if not result:
            return False

        return dict(*result)
    
    except Exception as e:
        print(f"Error read_one_methods_pay_by_use: {e}")
        return False
    finally:
        if connection is not None:
            await connection.close()


# # Read one method pay by USE:
# i = 2
# data = asyncio.run(read_one_methods_pay_by_use(i))
# print(data)
# print(data.get(f"use_{i}"))


# Deleted one methods_pay:
async def deleted_one_methods_pay(title: str):
    connection = None
    try:
        if type(title) != str:
            print("Error: input data is not str (title method pay.)")
            return False

        if not title:
            print("Error: Title method pay is Empty or None.")
            return False

        connection = await get_connection()
        await connection.execute(
            '''
                DELETE FROM methods_pay WHERE title_method_pay = $1;
            ''',
            title,
        )

        return True
    
    except Exception as e:
        print(f"Error deleted_one_methods_pay: {e}")
        return False
    finally:
        if connection is not None:
            await connection.close()


# Add methods_pay:
async def add_methods_pay(pay_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None

    if len(pay_data) <= 1: 
        print("Error: User_data is empty.")
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
        print(f"Error add_methods_pay: {e}")
        return False
    
    finally:
        if connection is not None:
            await connection.close()



# Update methods_pay by id:
async def update_methods_pay(pay_data):
    keys_list, values_list, i, connection = [], [], 1, None

    id = pay_data.get("id")

    if not id:
        print("Error update_methods_pay: Where is id?") 
        return False
    
    if len(pay_data) <= 1: # At a minimum, we need id + at least one element of the change.
        print("Error update_methods_pay: pay_data is empty or contains a single entry.")
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
        print(f"Error update_methods_pay: {e}")
        return False
    
    finally:
        if connection is not None:
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

# # Read all:
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


# Read all payments for one user_id:
async def read_all_payments_for_user_id(user_id):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM payments WHERE user_id = $1;
            ''',
            user_id
        )

        if not result:
            print(f"User {user_id} not pay.")
            return False

        data = []
        for record in result:
            data.append(dict(record))

        if len(data) == 1:
            data = dict(*result)

        return data
    
    except Exception as e:
        print(f"Error read_all_payments_for_user_id: {e}")
        return False
    finally:
        if connection is not None:
            await connection.close()


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
            print("Users not pay.")
            return False

        data = []
        for record in result:
            data.append(dict(record))

        if len(data) == 1:
            data = dict(*result)

        return data
    
    except Exception as e:
        print(f"Error read_all_payments: {e}")
        return False
    finally:
        if connection is not None:
            await connection.close()


# Add payments:
async def add_payments(payments):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None

    if len(payments) <= 1: 
        print("Error: User_data is empty.")
        return False
    
    if payments.get("user_id") is None: 
        print("Error: User_id is empty.")
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
        print(f"Error add_payments: {e}")
        return False
    
    finally:
        if connection is not None:
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
        print(f"Error deleted_all_payments: {e}")
        return False
    finally:
        if connection is not None:
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

        if len(data) == 1:
            data = dict(*result)

        return data
    
    except Exception as e:
        print(f"Error read_all_users: {e}")
    finally:
        if connection is not None:
            await connection.close()


# data_all_users = asyncio.run(read_all_users())
# for user in data_all_users:
#     print(user.get("user_id"), user.get("name"), user.get("money"))

