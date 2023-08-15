from werkzeug.exceptions import HTTPException
from flask import make_response
import json

# custom error handling 
class NotFoundError(HTTPException) : 
    def __init__(self, status_code, error_code) : 
        message = {"error_code" : error_code, 'error_message' : 'User Not Found'}
        self.response = make_response(json.dumps(message), status_code)

class ProductNotFoundError(HTTPException) : 
    def __init__(self, status_code, error_code) : 
        message = {"error_code" : error_code, 'error_message' : 'Product Not Found'}
        self.response = make_response(json.dumps(message), status_code)
        
class BusinessValidationError(HTTPException) : 
    def __init__(self, status_code, error_code, error_message) : 
        message = {'error_code' : error_code, 'error_message' : error_message}
        self.response = make_response(json.dumps(message), status_code)