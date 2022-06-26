import werkzeug
try:
    from flask_restplus import Api
except ImportError:
    #import werkzeug
    werkzeug.cached_property = werkzeug.utils.cached_property
    from flask_restplus import Api
from flask import Blueprint



from apis.operation_ns import api as operator_api
from apis.client_ns import api as client_api


blueprint = Blueprint('api', __name__, url_prefix='/')
api = Api(blueprint,
          version = "1.0", 
          title = "Arabeasy", 
          description = "Upload and download files")

api.add_namespace(operator_api)

api.add_namespace(client_api)
