import sqlite3 as sl

conn = sl.connect("operation.db", check_same_thread=False)
cur = conn.cursor()


def insert_operators():
    conn.execute("INSERT INTO operator (operator_id,user_name,password) VALUES (1, 'sonali', 'Sonali@12345')");  
    
    conn.execute("INSERT INTO operator (operator_id,user_name,password) VALUES (2, 'uttam', 'Uttam@12345')");  
    
    conn.execute("INSERT INTO operator (operator_id,user_name,password) VALUES (3, 'mark', 'Mark@12345' )");  
    
    conn.commit()   
    conn.close()  



def insert_file(file_path,user_name):
    msg = {'flag':False}
    try:
        conn.execute("INSERT INTO uploaded_files (file_path,user_name) VALUES ('{}', '{}')".format(file_path,user_name))
        msg= {'flag':True,"message":"inserted the file"}
    except Exception as e:
        msg = {'flag':False,'error':e}
    return msg


def insert_client(email,password):
    msg = {'flag':False}
    try:
        conn.execute("INSERT INTO client (email,password) VALUES ('{}', '{}')".format(email,password))
        msg= {'flag':True,"message":"created the account",'email':msg['email']}
    except Exception as e:
        msg = {'flag':False,'error':e}
    return msg



