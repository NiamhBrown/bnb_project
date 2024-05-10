from lib.request import *
from lib.request_repository import *

def test_get_all_request(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = RequestRepository(db_connection)
    result = repository.all()
    result = [str(r) for r in result]
    assert result == [
            "Request(1, 2, 2024-01-01, 2024-01-08)",
            "Request(2, 3, 2024-04-04, 2024-05-05)",
            "Request(3, 4, 2024-01-01, 2024-01-05)",
            "Request(2, 4, 2024-01-03, 2024-02-03)"
        ]

def test_create_spaces(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = RequestRepository(db_connection)
    repository.create(Request(1, 4, '2024-01-04', '2024-02-02'))
    result = repository.all()
    result = [str(r) for r in result]
    assert result == [
            "Request(1, 2, 2024-01-01, 2024-01-08)",
            "Request(2, 3, 2024-04-04, 2024-05-05)",
            "Request(3, 4, 2024-01-01, 2024-01-05)",
            "Request(2, 4, 2024-01-03, 2024-02-03)",
            "Request(1, 4, 2024-01-04, 2024-02-02)"
        ]

def test_find(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = RequestRepository(db_connection)
    result = repository.find(3, 4)
    assert str(result) == "Request(3, 4, 2024-01-01, 2024-01-05)"

def test_delete(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = RequestRepository(db_connection)
    repository.delete(3, 4)
    result = repository.all()
    result = [str(r) for r in result]
    assert result == [
            "Request(1, 2, 2024-01-01, 2024-01-08)",
            "Request(2, 3, 2024-04-04, 2024-05-05)",
            "Request(2, 4, 2024-01-03, 2024-02-03)",
        ]

