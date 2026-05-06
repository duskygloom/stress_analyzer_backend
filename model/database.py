from datetime import datetime
import sqlite3


class Database:
    tables = {
        # user_data table
        "user_data": "create table if not exists user_data ("
        "email text,"
        "upload_time text,"
        "mood float,"
        "stress float,"
        "comment text,"
        "primary key(email, upload_time)"
        ")",
        # otp_data table
        "otp_data": "create table if not exists otp_data ("
        "code text,"
        "email text primary key,"
        "creation_time text"
        ")",
        # token_data table
        "token_data": "create table if not exists token_data ("
        "token text,"
        "email text primary key,"
        "creation_time text"
        ")",
    }

    @staticmethod
    def get_connection():
        return sqlite3.connect("stress_analysis.db")

    @staticmethod
    def create_tables():
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(Database.tables["user_data"])
            cursor.execute(Database.tables["otp_data"])
            cursor.execute(Database.tables["token_data"])
            conn.commit()

    @staticmethod
    def drop_tables():
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("drop table if exists user_data")
            cursor.execute("drop table if exists otp_data")
            cursor.execute("drop table if exists token_data")
            conn.commit()

    @staticmethod
    def add_dummies():
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("delete from user_data")
            conn.commit()
            today = datetime.now()
            cursor.executemany(
                "insert into user_data values (?, ?, ?, ?, ?)",
                [
                    # user 1
                    ("user001@uni.edu", "2026-03-05", "3", "3", ""),
                    ("user001@uni.edu", "2026-03-08", "4", "3", ""),
                    ("user001@uni.edu", "2026-03-09", "3", "4", ""),
                    ("user001@uni.edu", "2026-03-10", "2", "5", ""),
                    ("user001@uni.edu", "2026-03-11", "1", "1", ""),
                    # user 2
                    ("user002@uni.edu", "2026-03-06", "3", "3", ""),
                    ("user002@uni.edu", "2026-03-08", "3", "3", ""),
                    ("user002@uni.edu", "2026-03-09", "3", "4", ""),
                    ("user002@uni.edu", "2026-03-10", "1", "1", ""),
                    ("user002@uni.edu", "2026-03-11", "4", "3", ""),
                    # user 3
                    ("user003@uni.edu", "2026-03-10", "5", "1", ""),
                    ("user003@uni.edu", "2026-03-11", "2", "5", ""),
                ],
            )
            conn.commit()
