from flask_restplus import Namespace, Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from core import login_operator as l
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import datetime
from core import file_upload

api = Namespace('operation', description='Operation related operations')
########################################### LOGIN ######################################################

login = reqparse.RequestParser()
login.add_argument('user_name', required = True)
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
                access_token = create_access_token(identity=message['user_name'], fresh=True)                
                message['access_token']= access_token
                message['message'] = 'login successful'
                return message, 200
            
            else:
                return message, 400

        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            api.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")


########################################### File Upload ######################################################

upparser = reqparse.RequestParser()
upparser.add_argument('file', location='files',
                  type=FileStorage, required=True)
upparser.add_argument('Authorization',type = str, location = 'headers', required = True)

@api.route('/uploader')
class Uploader(Resource):
    @jwt_required()
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @api.expect(upparser)
    def post(self):
        try:
            user = get_jwt_identity()
            args = upparser.parse_args()
            f = args['file']
            file_type= os.path.splitext(f.filename)[1]
            print(file_type)
            filename = (datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+'_'+ str(user) + file_type)
            sec_filename = secure_filename(filename)
            try:
                msg = file_upload.upload(f,sec_filename,user,file_type.replace(".",""))
                return msg, 200
            except Exception as e:
                return {'error':e}, 405
            # return msg
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            api.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")