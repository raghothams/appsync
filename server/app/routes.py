from flask import request, make_response, send_file, session, jsonify
from flask.ext.login import (LoginManager, login_user, logout_user,
        current_user, login_required, confirm_login)

import psycopg2.extras
import uuid
import traceback
import json

from app import app
from app.userdao import UserDAO
from app.user import User
from app.userapp import UserApp

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    user = UserDAO()
    return user.get(id)


# display index.html
@app.route("/")
def index():
    return send_file("static/index.html")


# user signup
@app.route("/signup/", methods=["POST"])
def signup():

    email = request.form["email"]
    uname = request.form["name"]
    password = request.form["password"]
    repeat = request.form["repeat"]

    result = None
    json_response = {}

    try:
        if email and uname and password and repeat:

            email = email.lower()
            uname = uname.strip()

            user = User()
            user.name = uname
            user.email = email
            user.password = password

            user_mapper = UserDAO()
            user_id = user_mapper.add(user)
            print user_id, "new user"

        else:
            json_respons['error'] = True
            json_response['data'] = "params error"

    except Exception as e:
        print "error while signing up user"
        print e
        
        # 500 internal server error
        raise ExceptionResponse()

    if user_id:
        json_response['error'] = False
        json_response['data'] = "Success!"
    else:
        json_response['error'] = True
        json_response['data'] = "Error signing up user"

    return jsonify(json_response)


# login the user
@app.route("/login/", methods=["POST"])
def login():

    result = None
    email = request.form["email"]
    password = request.form["password"]
    json_response = {}

    if email and password:
        email = email.lower()
        user_mapper = UserDAO()
        user = user_mapper.validate(email, password)

        if user:
            #login user
            is_success = login_user(user)
            if is_success:
                json_response['error'] = False
                json_response['data'] = "User logged in"
            else:
                json_response['error'] = True
                json_response['data'] = "Check user/password"

        else:
            json_response['error'] = True
            json_response['data'] = "Check user/password"

    else:
        json_response['error'] = True
        json_response['data'] = "email/password not supplied"

    return jsonify(json_response)


# logout user
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return jsonify({"error" : False, "data" : "User logged out"})


# get apps
@app.route("/apps/")
@login_required
def get_apps():

    user_app = UserApp()
    try:
        user_id = current_user.get_id()
        apps = user_app.get(user_id)

        if apps:
            response = {}
            response['user'] = current_user.serialize()
            response['apps'] = apps
            return jsonify(response)


    except Exception as e:
        print e
        raise ExceptionResponse() 


# update apps
@app.route("/apps/", methods=["POST"])
@login_required
def update_apps():

    user_app = UserApp()
    try:
        user_id = current_user.get_id()
        apps_json_str = request.form["apps"]
        apps_json = json.loads(apps_json_str)
        result = user_app.set(user_id, apps_json )

    except Exception as e:
        print e
        raise ExceptionResponse("Bad json", 400)

    try:
        if result:
            response = {}
            response['data'] = result
            return jsonify(response)

        else:
            return  "lol no data"

    except psycopg2.DatabaseError as e:
        print e
        raise ExceptionResponse()
    
    except Exception as e:
        print e
        raise ExceptionResponse()
        #return "error"



class ExceptionResponse(Exception):

    def __init__(self, message=None, status=500):

        Exception.__init__(self)
        self.status = status
        self.message = message or "Internal Server Error"

    def __dict__(self):

        rv = {}
        rv['error_code'] = self.status
        rv['message'] = str(self.message)
        return rv

@app.errorhandler(ExceptionResponse)
def internal_error(error):
    return make_response(jsonify(error.__dict__()), error.status)

