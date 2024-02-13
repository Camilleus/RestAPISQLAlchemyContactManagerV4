import mysql.connector
import os 
from dotenv import load_dotenv


load_dotenv()


def import_data_to_mysql():
    """
    Importuje dane z pliku SQL do bazy danych MySQL.
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="Camilleus",
        password="fghg1234",
        database="konigcontacts"
    )
    

    cursor = mysql_conn.cursor()


    try:
        with open("data_for_db.sql", "r") as sql_file:
            sql_commands = sql_file.read().split(';')

            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)


        mysql_conn.commit()
        print("Dane zostały zaimportowane do bazy MySQL.")
    except Exception as e:
        print(f"Błąd podczas importowania danych: {e}")
    finally:
        cursor.close()
        mysql_conn.close()

if __name__ == "__main__":
    import_data_to_mysql()
