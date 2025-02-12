import requests

def send_image_to_server(image_path):
    url = 'http://localhost:8080/process'
    files = {'file': open(image_path, 'rb')}
    
    response = requests.post(url, files=files)
    if response.status_code == 200:
        csv_path = response.json().get('csv_path')
        print(f"CSV generated: {csv_path}")
    else:
        print(f"Error: {response.json().get('details')}")

def test_server():
    url = 'http://localhost:8080/test'
    response = requests.post(url)
    try:
        response_json = response.json()
        if response.status_code == 200:
            print(response_json)
        else:
            print(f"Error: {response_json.get('error')}")
    except requests.exceptions.JSONDecodeError:
        print(f"Error: Received non-JSON response: {response.text}")

# Example usage
from os.path import expandvars

#test_server()
send_image_to_server('../images/test.jpeg')
