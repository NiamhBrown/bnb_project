from lib.request import Request

class RequestRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM users_spaces_requests')
        requests = []
        for row in rows:
            item = Request(row["user_id"], row["space_id"], row["start_date"], row["end_date"], row["approval"])
            requests.append(item) 
        return requests
    
    def create(self, request):
        self._connection.execute('INSERT INTO users_spaces_requests (user_id, space_id, start_date, end_date, approval) VALUES (%s, %s, %s, %s, %s)',
                                 [request.user_id, request.space_id, request.start_date, request.end_date, request.approval])
        return None 
    
    def find(self, user_id, space_id):
        rows = self._connection.execute('SELECT * FROM users_spaces_requests WHERE user_id = %s AND space_id = %s', [user_id, space_id])
        row = rows[0]
        return Request(row["user_id"], row["space_id"], row["start_date"], row["end_date"], row["approval"])
    
    def delete(self, user_id, space_id):
        self._connection.execute('DELETE FROM users_spaces_requests WHERE user_id = %s AND space_id = %s', [user_id, space_id])
        return None 

    def update(self, status, user_id, space_id):
        self._connection.execute('UPDATE users_spaces_requests SET approval = %s  WHERE user_id = %s AND space_id = %s', [status, user_id, space_id])

# SELECT name FROM spaces, users_spaces_requests WHERE spaces.id = space_id AND user_id = 1;
    def list_request_from_user(self, user_id):
        rows = self._connection.execute('SELECT user_id, space_id, name, approval, users_spaces_requests.start_date, users_spaces_requests.end_date FROM spaces, users_spaces_requests WHERE spaces.id = space_id AND user_id = %s', [user_id])
        return rows
    
    def list_request_to_user(self, user_id):
        rows = self._connection.execute('SELECT user_id, space_id, name, approval, users_spaces_requests.start_date, users_spaces_requests.end_date FROM spaces, users_spaces_requests WHERE spaces.id = space_id AND spaces.owner = %s', [user_id])
        return rows