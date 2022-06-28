from db import fetch_scripts



def login(args):
    msg={}
    
    # Check if account exists using SqlLite
    try:
        email=args['email']
        password=args['password']
        
        res = fetch_scripts.check_client_credentials(email,password)
        # print(res)
        # If account exists show error and validation checks
        if res['flag']:
            
            msg = {'login':True,'message':'login successful','email':email}
        else:
            msg = {'login':False, 'Error':'email or password is incorrect'}

    except KeyError as error:
        msg = {'login':False,'Error':'Error in login : {}'.format(error)}
    return msg
