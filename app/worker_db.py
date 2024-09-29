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
        
        for record in result:
            data = dict(record)
        return data 
    
    except Exception as e:
        print(f"Error read_user: {e}")
    finally:
        if connection is not None:
            await connection.close()

# # Read user:
# data_user = asyncio.run(read_user(1666495))

# print(data_user)

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
        return data
    
    except Exception as e:
        print(f"Error read_statistics: {e}")
    finally:
        if connection is not None:
            await connection.close()

# # Read statistics by user_id:
# data_user = asyncio.run(read_statistics(485435943))
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
        print(f"Error read_all_users: {e}")
    finally:
        if connection is not None:
            await connection.close()


# data_all_users = asyncio.run(read_all_users())
# for user in data_all_users:
#     print(user.get("user_id"), user.get("name"), user.get("money"))

