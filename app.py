from extensions import jwt
from flask import Flask
from apiv1 import blueprint as api1
import datetime
from flask_cors import CORS
from flask_redmail import RedMail
from redmail import gmail
mail=RedMail()
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.secret_key = 'ChangeMe!'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False    
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50 MB
    
    app.config["EMAIL_HOST"] = gmail.host
    app.config["EMAIL_PORT"] = gmail.port
    app.config["EMAIL_USER"] = "yourgmail@gmail.com"
    app.config["EMAIL_PASSWORD"] = "yourpassword"

    # Set some other relevant configurations
    app.config["SECRET_KEY"] = "GUI interface with VBA"

    

    mail.init_app(app)

    jwt.init_app(app)

    app.register_blueprint(api1)
    
    return app