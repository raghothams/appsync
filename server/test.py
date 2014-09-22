from app.userdao import UserDAO
from app.userapp import UserApp
from app.user import User

import json

def test_create_user():
    user_mapper = UserDAO()
    user = User("tester@test.com", "test123", "tester")

    result = user_mapper.add(user)

    print result

def test_update_apps():
    app_mapper = UserApp()
    res = app_mapper.set(1, '{"attr":"loler"}')
    print res

def test_get_apps():
    app_mapper = UserApp()
    apps = app_mapper.get(1)
    print apps
#test_create_user()
#test_update_apps()
#test_get_apps()

