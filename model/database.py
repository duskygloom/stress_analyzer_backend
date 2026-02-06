import os
import sqlite3
from dotenv import load_dotenv

load_dotenv(".env")


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
