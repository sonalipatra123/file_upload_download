from flask_restplus import Namespace, Resource, reqparse
# from oauthlib.oauth2 import WebApplicationClient
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from core import login_client as l
from flask import *  
from flask_mail import * 
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from core import file_download
from db import fetch_scripts,insert_data
s = URLSafeTimedSerializer('Thisisasecret!')
api = Namespace('client', description='client related operations')

#################################################### sign up ########################################

signup = reqparse.RequestParser()
signup.add_argument('email', required = True)
signup.add_argument('password', required = True)
@api.route("/signup")
class Signup(Resource):
    
    
    @api.doc(responses={ 200: 'OK',400: 'Invalid Data' })
    @api.expect(signup)
    def post(self):
        try:
            from app import mail
            
            args = signup.parse_args()
            email = args["email"]
            password = args["password"]

            # Verifying the user does not exist
            old_user = fetch_scripts.check_client_credentials(email,password)
            if old_user['flag']:
                abort(403)
            # Create a secure token (string) that identifies the user
            # token = jwt.encode({"email": email,"password":password}, current_app.config["SECRET_KEY"])
            # print(token)
            # Send verification email
            token = s.dumps(email + "|" +password, salt='email-confirm')

            msg = Message('Confirm Email', sender='mama.sona04@gmail.com', recipients=[email])
            
            link = api.url_for('/client/verify', token=token, _external=True)
            msg.body = 'Your link is {}'.format(link)

            mail.send(msg)

            return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)
   

        except KeyError as e:
            api.abort(500, e.__doc__, status = "error in server", statusCode = "500")
        except Exception as e:
            api.abort(400, e.__doc__, status = "error in code", statusCode = "400")


######################################## Verify Email #################################################
verify = reqparse.RequestParser()
verify.add_argument('token', required = True)
@api.route("/verify")
class Verify(Resource):
    @api.doc(responses={ 200: 'OK',400: 'Invalid Data' })
    @api.expect(verify)
    def post(self,token):
        try:
            args = verify.parse_args()
            # data = jwt.decode(args['token'], current_app.config["SECRET_KEY"])
            try:
                emailpassword = s.loads(args['token'], salt='email-confirm', max_age=3600)
                epasslist = emailpassword.split("|")
                email = epasslist[0]
                password = epasslist[1]
                msg = insert_data.insert_client(email,password)
            except SignatureExpired:
                return '<h1>The token is expired!</h1>'
            

            
            if msg['flag']:
                # when authenticated, return a fresh access token and a refresh token
                access_token = create_access_token(identity=msg['email'], fresh=True)                
                msg['access_token']= access_token
                msg['message'] = 'login successful'
                return msg, 200
            
            else:
                return msg, 400
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Error", statusCode = "500")
        except Exception as e:
            api.abort(400, e.__doc__, status = "Error", statusCode = "400")
# api.add_resource(Verify, '/verify/<token>', endpoint = 'verify_email')
########################################### LOGIN ######################################################

login = reqparse.RequestParser()
login.add_argument('email', required = True)
login.add_argument('password',required = True)
@api.route("/login")
class Login(Resource):
    @api.doc(responses={ 200: 'OK',400: 'Invalid Data' })
    @api.expect(login)
    def post(self):
        try:
            args = login.parse_args()
            message=l.login(args)
            if message['login']:
                # when authenticated, return a fresh access token and a refresh token
                access_token = create_access_token(identity=message['email'], fresh=True)                
                message['access_token']= access_token
                message['message'] = 'login successful'
                return message, 200
            
            else:
                return message, 400

        except KeyError as e:
            api.abort(500, e.__doc__, status = "Error", statusCode = "500")
        except Exception as e:
            api.abort(400, e.__doc__, status = "Error", statusCode = "400")


############################################### download file ######################################################
download_file =reqparse.RequestParser()
download_file.add_argument('file_path', required = True)
download_file.add_argument('Authorization',type = str, location = 'headers', required = True)

@api.route("/file_download")
class FileDownload(Resource):
    @jwt_required()
    @api.doc(responses={ 200: 'OK',400: 'Invalid Data' })
    @api.expect(download_file)
    def post(self):
        try:
            args = download_file.parse_args()
            email = get_jwt_identity()
            message=file_download.download(email,args['file_path'])
            if message['flag']:
                return message, 200
            
            else:
                return message, 400

        except KeyError as e:
            api.abort(500, e.__doc__, status = "Error", statusCode = "500")
        except Exception as e:
            api.abort(400, e.__doc__, status = "Error", statusCode = "400")


############################################### list file ######################################################
list_file =reqparse.RequestParser()
download_file.add_argument('Authorization',type = str, location = 'headers', required = True)


@api.route("/list_files")
class Listfiles(Resource):
    @api.doc(responses={ 200: 'OK',400: 'Invalid Data' })
    @api.expect(list_file)
    def post(self):
        try:
            args = list_file.parse_args()
            message=fetch_scripts.fetch_files()
            if message['flag']:
                return message, 200
            
            else:
                return message, 400

        except KeyError as e:
            api.abort(500, e.__doc__, status = "Error", statusCode = "500")
        except Exception as e:
            api.abort(400, e.__doc__, status = "Error", statusCode = "400")



