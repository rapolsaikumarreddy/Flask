from user import User

users = [
    User(1, 'bob', 'asdf'),
    User(2, "rapol", "rapol")
]

username_mapping = {
    u.username: u for u in users
}

userid_mapping = {
    u.id: u for u in users
}

"""
userid_mapping = { 1: {
        'id' = 1,
        'username': 'bob',
        'password': 'asdf'
    }
}

werkzeug.security for comparing strigs securily 

"""


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user


def identity(payload):
    print(payload)
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
