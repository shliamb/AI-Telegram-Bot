from get_keys import USER_DB, PASSWORD_DB
import psycopg2


# Create TABLES:
def create_tables_in_db():

    try:
        # Conect to db:                   имя контейнера
        connection = psycopg2.connect(host="localhost", database="my_database", user=USER_DB, password=PASSWORD_DB)
        
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
            model_say TEXT,
            summarization BOOLEAN,
            user_id BIGINT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        '''
        cursor.execute(create_table_discussion)

        create_table_metod_pay = '''
        CREATE TABLE IF NOT EXISTS pays (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP,
            title_metod_pay VARCHAR(50),
            counts INT,
            metod_pay TEXT
        );
        '''
        cursor.execute(create_table_metod_pay)

        create_table_pays = '''
        CREATE TABLE IF NOT EXISTS pays (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP,
            title_metod_pay VARCHAR(50),
            sum FLOAT,
            user_id BIGINT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        '''
        cursor.execute(create_table_pays)


        # Saving changes:
        connection.commit()
        print("Adding tables is done!")

    except Exception as error:
        print("Error:", error)
    finally:

        # Closing the cursor and database connection
        if cursor:
            cursor.close()
            
        if connection:
            connection.close()




create_tables_in_db()







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
