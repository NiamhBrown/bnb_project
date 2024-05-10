from lib.request import Request

def test_construct_request():
    request = Request(1, 2, '2024-01-01', '2024-01-08')
    assert request.user_id == 1
    assert request.space_id == 2
    assert request.start_date == '2024-01-01'
    assert request.end_date == '2024-01-08'

def test_request_are_equal():
    request1 = Request(1, 2, '2024-01-01', '2024-01-08')
    request2 = Request(1, 2, '2024-01-01', '2024-01-08')
    assert request1 == request2

def test_user_are_format():
    request = Request(1, 2, '2024-01-01', '2024-01-08')
    assert str(request) == "Request(1, 2, 2024-01-01, 2024-01-08)"


