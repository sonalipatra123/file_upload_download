
from db import fetch_scripts



def login(args):
    msg={}
    
    # Check if account exists using SqlLite
    try:
        user_name=args['user_name']
        password=args['password']
        
        res = fetch_scripts.check_operator_credentials(user_name,password)
        print(res)
        # If account exists show error and validation checks
        if res['flag']:
            
            msg = {'login':True,'message':'login successful','user_name':user_name}
        else:
            msg = {'login':False, 'Error':'User name or password is incorrect'}

    except KeyError as error:
        msg = {'login':False,'Error':'Error in login : {}'.format(error)}
    return msg
