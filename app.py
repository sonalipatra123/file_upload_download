from extensions import jwt
from flask import Flask
from apiv1 import blueprint as api1
import datetime
from flask_cors import CORS
from flask_mail import Mail
mail=Mail()
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.secret_key = 'ChangeMe!'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False    
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50 MB
    
    # app.config["EMAIL_HOST"] = "smtp.gmail.com"
    # app.config["EMAIL_PORT"] = 587
    # app.config["EMAIL_USER"] = "mama.sona04@gmail.com"
    # app.config["EMAIL_PASSWORD"] = "uttam.sonali"
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'mama.sona@gmail.com'
    app.config['MAIL_PASSWORD'] = 'uttam.sonali'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    # Set some other relevant configurations
    app.config["SECRET_KEY"] = "GUI interface with VBA"

    

    mail.init_app(app)

    jwt.init_app(app)

    app.register_blueprint(api1)
    
    return app