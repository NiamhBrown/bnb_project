from lib.user import *

"""
test the init 
"""

def test_construct_user():
    user = User(1, "test_name", "test_email", "test_password")
    assert user.id == 1
    assert user.name == "test_name"
    assert user.email == "test_email"
    assert user.password == "test_password"

def test_users_are_equal():
    user1 = User(1, "Person1", "test_email", "test_password")
    user2 = User(1, "Person1", "test_email", "test_password")
    assert user1 == user2

def test_user_are_format():
    user = User(1, "Person1", "test_email", "test_password")
    assert str(user) == "User(1, Person1, test_email, test_password)"