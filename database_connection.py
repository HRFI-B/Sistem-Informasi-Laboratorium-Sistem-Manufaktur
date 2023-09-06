import mysql.connector
import time

def database_connection():
    try:
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="81132329",
            database="SILSM"
            )
    except mysql.connector.Error as e:
        raise e
    return db

def read_data(query, params=(), fetch_type="fetchall"):
    attempt = 0
    max_attempt = 5
    while attempt < max_attempt:
        try:
            mysql = database_connection()
            with mysql.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                if fetch_type == "fetchone":
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error connecting to database: {e}. Retrying in 5 seconds.")
            time.sleep(5)
            attempt += 1

    return result

def write_data(query, params=()):
    attempt = 0
    max_attempt = 5
    while attempt < max_attempt:
        try:
            mysql = database_connection()
            with mysql.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                mysql.commit()
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}. Retrying in 5 seconds.")
            time.sleep(5)
            attempt += 1
            
# def audit_log():
#     query = "INSERT INTO `audit_log` (`user_id`, `activity`, `table_name`, `data_id`, `changed_attribute`, `old_value`, `new_value`, `description`, `timestamp`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     return query