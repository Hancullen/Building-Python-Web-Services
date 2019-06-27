import datetime

MOCK_USERS = [{'email': 'test@test.com',
                'hashed': '$2b$12$7At7WEWWEbT5NC49mlcdauDEd8E/ZlABU1no9qGSgFUL9C6WzMEPu'}]
MOCK_TABLES = [{"_id": "1", "number": "1", "owner": "test@example.com","url": "mockurl"}]
MOCK_REQUESTS = [{"_id": "1", "table_number": "1","table_id": "1", "time": datetime.datetime.now()}]

class MockDBhelper:
    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get('email') == email]
        if user:
            return user[0]
        return None

    def add_user(self, email, hashed):
        MOCK_USERS.append({'email': email, 'hashed': hashed})

    def add_table(self, number, owner):
        MOCK_TABLES.append({"_id": str(number), "number": number, "owner":owner})
        return number

    def update_table(self, _id, url):
        for table in MOCK_TABLES:
            if table.get("_id") == _id:
                table["url"] = url
                break

    def get_tables(self, owner_id):
        return MOCK_TABLES

    def delete_table(self, table_id):
        for i, table in enumerate(MOCK_TABLES):
            if table.get("_id") == table_id:
                del MOCK_TABLES[i]
                break

    def add_request(self, table_id, time):
        table = self.get_tables(table_id)
        for req in MOCK_REQUESTS:
            if req.get("_id") == table_id:
                req['owner'] = table['owner']
                req['table_number'] = table['number']
                req['time'] = time
                break
        MOCK_REQUESTS.append(req)
        return True

    def get_requests(self, owner_id):
        return MOCK_REQUESTS


    def delete_request(self, request_id):
        for i, request in enumerate(MOCK_REQUESTS):
            if request.get("_id") == request_id:
                del MOCK_REQUESTS[i]
                break
