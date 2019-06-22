MOCK_USERS = [{'email': 'test@test.com',
                'hashed': '$2b$12$mUyANVxdik6mitVSOliTeuHdXjG0SimkstM5TQCyuyGDRTeZcwYGG'}]

class MockDBhelper:
    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get('email') == email]:
        if user:
            return user[0]
        return None

    def add_user(self, email, hashed):
        MOCK_USERS.append({'email': email, 'hashed': hashed})
