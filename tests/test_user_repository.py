from lib.user import *
from lib.user_repository import *


def test_get_all_users(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = UserRepository(db_connection)

    result = repository.all()
    assert result == [
            User(1, 'Person1', 'test1@gmail.com', 'password123'),
            User(2, 'Person2', 'test2@gmail.com', 'password123'),
            User(3, 'Person3', 'test3@gmail.com', 'password123')
        ]
    
def test_create_user(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = UserRepository(db_connection)
    repository.create(User(None, 'Person4', "test email", "Password1234"))
    result = repository.all()
    assert result == [
        User(1, 'Person1', 'test1@gmail.com', 'password123'),
        User(2, 'Person2', 'test2@gmail.com', 'password123'),
        User(3, 'Person3', 'test3@gmail.com', 'password123'),
        User(4, 'Person4', 'test email', 'Password1234')
    ]

def test_find_user(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = UserRepository(db_connection)
    result = repository.find(3)
    assert result == User(3, 'Person3', 'test3@gmail.com', 'password123')

def test_delete_user(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = UserRepository(db_connection)
    repository.delete(3)
    result = repository.all()
    assert result == [
        User(1, 'Person1', 'test1@gmail.com', 'password123'),
        User(2, 'Person2', 'test2@gmail.com', 'password123')
    ]