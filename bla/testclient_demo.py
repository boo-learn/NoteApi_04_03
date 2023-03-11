from app import app

test_client = app.test_client()
response = test_client.get('/users')
print("json = ", response.json)
print("code = ", response.status_code)