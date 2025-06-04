from get_keys import USER_DB, PASSWORD_DB, DB_NAME
import psycopg2
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO, filename='./log/db.log')


# Create TABLES:
def create_tables_in_db():

    try:
        # Conect to db:                   имя контейнера app_postgres or localhost
        connection = psycopg2.connect(host="app_postgres", database=DB_NAME, user=USER_DB, password=PASSWORD_DB)
        
        cursor = connection.cursor()
        
        # Create table:
        create_table_users = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            name VARCHAR(50),
            full_name VARCHAR(50),
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            block BOOLEAN DEFAULT FALSE,
            last_visit TIMESTAMP,
            time_zone VARCHAR(10), 
            language VARCHAR(10),
            system_content TEXT,
            paid INT DEFAULT 0,
            money FLOAT,
            notifications BOOLEAN,
            dialog BOOLEAN,
            dialog_sum BOOLEAN,
            voice_answer BOOLEAN,

            ai VARCHAR(50),
            model_language VARCHAR(50),

            ai_draw VARCHAR(50),
            model_draw VARCHAR(50),

            ai_voice_to_text VARCHAR(50),
            model_voice_to_text VARCHAR(50),

            ai_text_to_voice VARCHAR(50),
            model_text_to_voice VARCHAR(50),

            voice VARCHAR(50),
            voice_speed FLOAT,
            img_quality VARCHAR(50),
            img_style VARCHAR(50),
            img_size VARCHAR(50),
            n_number INTEGER
        );
        CREATE INDEX idx_ai ON users(ai);
        CREATE INDEX idx_user_system_content ON users(system_content);
        '''
        # Executing an SQL query:
        cursor.execute(create_table_users)


        # !!!! Как-то надо её чистить, боюсь представить сколько там записей..
        create_table_statistics = '''
        CREATE TABLE IF NOT EXISTS statistics (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP,
            model VARCHAR(50),
            tokens INTEGER,
            min FLOAT,
            img INTEGER,
            price_1 FLOAT,
            price FLOAT,
            user_id BIGINT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        '''
        cursor.execute(create_table_statistics)


        create_table_discussion = '''
        CREATE TABLE IF NOT EXISTS discussion (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP,
            user_say TEXT,
            assist_say TEXT,
            summarization BOOLEAN,
            user_id BIGINT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        '''
        cursor.execute(create_table_discussion)

        create_table_methods_pay = '''
        CREATE TABLE IF NOT EXISTS methods_pay (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP,
            counts INT,
            use_sbp_transfer BOOLEAN,
            use_mastercard BOOLEAN,
            use_visa BOOLEAN,
            use_mircard BOOLEAN,
            use_cripto BOOLEAN,
            use_sms BOOLEAN,
            use_stars BOOLEAN,
            use_telegram BOOLEAN,
            use_digital BOOLEAN,
            title_method_pay VARCHAR(50) UNIQUE,
            method_pay_ru TEXT,
            method_pay_en TEXT
        );
        '''
        cursor.execute(create_table_methods_pay)

        create_table_payments = '''
        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP UNIQUE,
            title_method_pay VARCHAR(50),
            sum FLOAT,
            user_id BIGINT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        '''
        cursor.execute(create_table_payments)


        # create_table_admin_data = '''
        # CREATE TABLE IF NOT EXISTS admin_data (
        #     id SERIAL PRIMARY KEY,
        #     date TIMESTAMP,
        #     thread_id VARCHAR(100),
        #     assistant_id VARCHAR(100),
        #     model_assist VARCHAR(50),                                   --(Модель OpenAI для Ассистента-Админ)
        #     operating_mode BOOLEAN,                                     --(Режим работы в админке. Admin AI or Normal)                 
        #     user_id BIGINT NOT NULL UNIQUE,                             --(id_user admin)
        #     FOREIGN KEY (user_id) REFERENCES users(user_id)
        # );
        # '''
        # cursor.execute(create_table_admin_data)


        # Saving changes:
        connection.commit()
        logging.info("Adding tables is done!")
        print("Adding tables is done!")
        return True

    except Exception as error:
        logging.error(f"Error Create Tables in DB: {error}")
        print("Error Create Tables in DB:", error)
        return False

    finally:

        # Closing the cursor and database connection
        if cursor:
            cursor.close()
            
        if connection:
            connection.close()




# create_tables_in_db()







'''
Architecture Data Base.

Table users:
user_id  name  full_name  first_name  last_name  block  last_visit  time_zone  language  system_content  money  
notifications  dialog  dialog_sum  audio_response  ai  model_openai  model_google  model_anthropic  model_llamA  model_dall_e  
model_midjourney  model_voice  model_speech  voice  voice_speed  img_quality  img_style  img_size  n_number

Table statistics:
id  date  model  tokens  min  img  price  user_id  name

Table discussion:
id  date  user_say  model_say  summarization  user_id 

'''


# VARCHAR(n) - строковый тип данных ограничение n, TEXT - строковый тип данных ограничение в 1Гб.
# iuser_id INTEGER SERIAL PRIMARY KEY , тут SERIAL - означает, что каждый последующее число в строке будет само увеличиваться..
# Если ячейка является первичным ключем, то она автоматически добавленна в индекс, CONSTRAINT unique_user_id UNIQUE (user_id)  -- Создание уникального ограничения также создает индекс
# INTEGER  BIGINT block BOOLEAN NOT NULL DEFAULT FALSE  INTEGER  VARCHAR(100) NOT NULL UNIQUE UNIQUE
# time_zone TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# UNIQUE - автоматом индексируются
# INDEX idx_name (name)  -- Создание обычного индекса на колонке name