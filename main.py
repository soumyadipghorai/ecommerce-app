import os 
import logging 
from flask import Flask 
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig 
from application.data.database import db 
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore 
from application.data.models import User, Role 
from flask_cors import CORS

logging.basicConfig(
    filename = 'debug.log', 
    level = logging.DEBUG, 
    format = f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
)

app = None 
api = None 
def create_app() : 
    app = Flask(__name__, template_folder = 'templates')
    app.secret_key = 'ItShouldBeAnythingButSecret'
    if os.getenv('ENV', 'development') == 'production' :
        raise Exception('Currently no production config is setup')

    else : 
        print('starting local dev')
        app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    app.logger.info("App setup complete")
    CORS(app)
    return app, api 
    # return app

app, api = create_app()
# app = create_app()

# import all the controllers so they are loaded 
from application.controller.controllers import *
from application.controller.api import UserAPI, ProductAPI, CartAPI, AdminDashboarAPI, ProductPageAPI, OffersAPI, SearchResult
api.add_resource(UserAPI, "/api/user", "/api/user/<string:username>")
api.add_resource(ProductAPI, "/api/product", "/api/category/<string:product>")
api.add_resource(CartAPI, "/api/cart", "/api/cart/<string:username>")
api.add_resource(AdminDashboarAPI, "/api/admin", "/api/admin/<string:username>")
api.add_resource(ProductPageAPI, "/api/product-page", "/api/product-page/<string:username>")
api.add_resource(OffersAPI, "/api/offers", "/api/offers/<string:username>")
api.add_resource(SearchResult, "/api/search", "/api/search/<string:username>")

@app.errorhandler(404)
def page_not_found(e) :
    return render_template('error.html'), 404

if __name__ == '__main__' : 
    app.run(host = '0.0.0.0', port = 8080)