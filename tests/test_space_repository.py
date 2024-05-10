from lib.spaces import *
from lib.space_repository import *

def test_get_all_spaces(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = SpaceRepository(db_connection)
    result = repository.all()
    result = [str(r) for r in result]
    assert result == [
            "Space(1, 1, venue #1, desc #1, 50, 2024-01-01, 2024-01-08)",
            "Space(2, 1, venue #2, desc #2, 60, 2024-04-04, 2024-05-05)",
            "Space(3, 1, venue #3, desc #3, 70, 2024-01-01, 2024-01-05)",
            "Space(4, 2, venue #4, desc #4, 80, 2024-01-03, 2024-02-03)",
            "Space(5, 2, venue #5, desc #5, 90, 2024-02-04, 2024-02-05)"
        ]

def test_create_spaces(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = SpaceRepository(db_connection)
    repository.create(Space(None, 2, 'venue #6', 'desc #6', 50, '2024-12-12', '2024-12-20'))
    result = repository.all()
    result = [str(r) for r in result]
    assert result == [
            "Space(1, 1, venue #1, desc #1, 50, 2024-01-01, 2024-01-08)",
            "Space(2, 1, venue #2, desc #2, 60, 2024-04-04, 2024-05-05)",
            "Space(3, 1, venue #3, desc #3, 70, 2024-01-01, 2024-01-05)",
            "Space(4, 2, venue #4, desc #4, 80, 2024-01-03, 2024-02-03)",
            "Space(5, 2, venue #5, desc #5, 90, 2024-02-04, 2024-02-05)",
            "Space(6, 2, venue #6, desc #6, 50, 2024-12-12, 2024-12-20)"
        ]

def test_find(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = SpaceRepository(db_connection)
    result = repository.find(3)
    assert str(result) == "Space(3, 1, venue #3, desc #3, 70, 2024-01-01, 2024-01-05)"

def test_delete(db_connection):
    db_connection.seed("seeds/seed.sql")
    repository = SpaceRepository(db_connection)
    repository.delete(3)
    result = repository.all()
    result = [str(r) for r in result]
    assert result == [
            "Space(1, 1, venue #1, desc #1, 50, 2024-01-01, 2024-01-08)",
            "Space(2, 1, venue #2, desc #2, 60, 2024-04-04, 2024-05-05)",
            "Space(4, 2, venue #4, desc #4, 80, 2024-01-03, 2024-02-03)",
            "Space(5, 2, venue #5, desc #5, 90, 2024-02-04, 2024-02-05)"
        ]

