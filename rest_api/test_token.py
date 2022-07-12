import requests   # pip install requests

TOKEN = '4d3a9e615a3f70bcd5c1a8133c077b67cd88f3a6'

headers = {
    'Authorization': f'Token {TOKEN}',
}

res = requests.get("http://localhost:8000/post/1/", headers=headers)
print(res.json())