from app import app

test_client = app.test_client()
user_data = {
   'username': 'test-user',
   'password': 'test-user'
}
response = test_client.post('/users',
                      json=user_data,
                      content_type='application/json')