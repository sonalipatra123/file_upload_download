import sqlite3 as sl

con = sl.connect("operation.db")
cur = con.cursor()

cur.execute(""" CREATE TABLE operator
            (
                operator_id INT NOT NULL PRIMARY KEY,
                user_name TEXT NOT NULL,
                password TEXT NOT NULL

            ) """)

con.commit()


cur.execute("""
CREATE TABLE client
            (
                client_id INT NOT NULL PRIMARY KEY,
                email_id TEXT NOT NULL,
                password TEXT NOT NULL

            ) """)

con.commit()

cur.execute(""" CREATE TABLE uploaded_files
            (
                file_id INT NOT NULL PRIMARY KEY,
                file_path TEXT NOT NULL,
                user_name TEXT NOT NULL

            ) """)

con.commit()


con.close()