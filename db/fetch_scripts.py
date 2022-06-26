import sqlite3 as sl

con = sl.connect("operation.db", check_same_thread=False)
cur = con.cursor()

def check_operator_credentials(user_name,password):
    msg = {'flag':False}
    try:
        query ="select * from operator where user_name='{}' and password = '{}'".format(user_name,password)
        # print(query)
        cur.execute(query)
        data= cur.fetchone()
        # print(data)
        if data is not None:
            msg = {'flag':True,'message':'User exists.',"user_name":data[1]}
        else:
            msg = {'flag':False,'message':'User does not exist.'}
    except Exception as e:
        msg = {'flag':False,'error':e}

    return msg

def check_client_credentials(user_name,password):
    msg = {'flag':False}
    try:
        query ="select * from client where email='{}' and password = '{}'".format(user_name,password)
        # print(query)
        cur.execute(query)
        data= cur.fetchone()
        print(data)
        if data is not None:
            msg = {'flag':True,'message':'User exists.','email':data['email']}
        else:
            msg = {'flag':False,'message':'User does not exist.'}
    except Exception as e:
        msg = {'flag':False,'error':e}

    return msg

def check_client_existance(email):
    msg = {'flag':False}
    try:
        query ="select * from client where email='{}'".format(email)
        # print(query)
        cur.execute(query)
        data= cur.fetchone()
        # print(data)
        if data is not None:
            msg = {'flag':True,'message':'User exists.','email':data[1]}
        else:
            msg = {'flag':False,'message':'User does not exist.'}
    except Exception as e:
        msg = {'flag':False,'error':e}

    return msg

def fetch_files():
    msg = {'flag':False}
    try:
        query ="select file_path from uploaded_files"
        # print(query)
        cur.execute(query)
        data= cur.fetchall()
        # print(data)
        if data is not None and data !=[]:
            msg = {'flag':True,'message':'files listed','data':data}
        else:
            msg = {'flag':False,'message':'files not present','data':data}
    except Exception as e:
        msg = {'flag':False,'error':e}

    return msg

