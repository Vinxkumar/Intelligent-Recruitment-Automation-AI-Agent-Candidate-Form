from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os
from DataBase import Queries
load_dotenv()
class DataBaseConnection:
    def connect(self):
        # return ( mysql.connector.connect(
        #         host = "localhost",
        #         user = "vinxkumar",
        #         password = "060814",
        #         database = "recruit",
        #         port = 3306
        #     )
        # )
        return (mysql.connector.connect(
                host=os.getenv("HOSTNAME"),
                user=os.getenv("USER_NAME"),
                password=os.getenv("PASSWORD"),
                database=os.getenv("DATABASE"),
                port=int(os.getenv("MYSQLPORT"),
                autocommit = True
            )
        )
    def getDriveStatus(self, drive_name:str):
        try:
            connect = self.connect()
            cursor = connect.cursor()
            cursor.execute(Queries.check_Drive_status, (drive_name,))
            result = cursor.fetchone()
            print(f"Drive status for {drive_name}: {result[0] if result else 'Not found'}")  #type: ignore
            return result[0] if result else 'Not found' #type: ignore

        except Error as e:
            print(f"Error fetching drive status: {e}")
            return None
        
    def insertCandidate(self, table_name:str, candidate_data:tuple):
        try :
            drivename = table_name.strip().lower().replace(" ", "_")
            connect = self.connect()
            cursor = connect.cursor()
            cursor.execute(Queries.insert_into_recruitment.format(table_name=drivename), candidate_data)
            return True
        except Error as e:
            print(f"Error inserting candidate data: {e}")
            return False
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()
