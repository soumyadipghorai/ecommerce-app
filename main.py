import os 
from flask import Flask 
# from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig 
from application.database import db 
import logging 
logging.basicConfig(
        filename = 'debug.log', 
        level = logging.DEBUG, 
        format = f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
    )

app = None 
api = None 
def create_app() : 
    app = Flask(__name__, template_folder = 'templates')
    app.secret_key = 'abcd'
    if os.getenv('ENV', 'development') == 'production' :
        raise Exception('Currently no production config is setup')

    else : 
        print('starting local dev')
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    # api = Api(app)
    app.app_context().push()
    # return app, api 
    return app

# app, api = create_app()
app = create_app()

# import all the controllers so they are loaded 
from application.controllers import *
# from application.api import UserAPI
# api.add_resource(UserAPI, "/api/user", "/api/user/<string:username>")

if __name__ == '__main__' : 
    app.run(host = '0.0.0.0', port = 8080)