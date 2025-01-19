import requests

url = 'http://127.0.0.1:5000/api/reviews'
params = {'page': 'https://2717recovery.com/products/recovery-cream'}

print(f"Sending GET request to URL: {url} with params: {params}")
response = requests.get(url, params=params)

if response.status_code == 200:
    print("Request successful! Reviews extracted:")
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)


