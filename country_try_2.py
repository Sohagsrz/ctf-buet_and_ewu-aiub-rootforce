import socket
from geopy.geocoders import Nominatim
import time
import re

def get_country_from_coordinates(coords):
    geolocator = Nominatim(user_agent="measurements")
    countries = set()  # Use a set to avoid duplicates

    for coord in coords:
        try:
            # Extract latitude and longitude from the input line
            latitude = float(coord.split(',')[0].split(': ')[1])
            longitude = float(coord.split(',')[1].split(': ')[1])
            location = geolocator.reverse((latitude, longitude), exactly_one=True, language='en')  # Specify language as English
            if location and 'country' in location.raw['address']:
                countries.add(location.raw['address']['country'])
        except (IndexError, ValueError) as e:
            print(f"Error processing coordinate '{coord}': {e}")

    return sorted(countries)

def extract_round_info(data):
    """Extract the current and total rounds from the server response."""
    match = re.search(r"Round (\d+)/(\d+)", data)
    if match:
        current_round = int(match.group(1))
        total_rounds = int(match.group(2))
        return current_round, total_rounds
    return None, None
def looprun(data, s):
    print(data)
    if not data:
        print("Could not extract round information. Exiting.")
        return False
    current_round, total_rounds = extract_round_info(data)
    if current_round is None or total_rounds is None:
        print("Could not extract round information. Exiting.")
        return False

    print(f"Processing Round {current_round}/{total_rounds}")

    print(f"Received:\n{data}") 
    
    coords = [line.strip() for line in data.splitlines() if 'Latitude:' in line and 'Longitude:' in line]
    # print(coords)

    # Get sorted country names
    countries = get_country_from_coordinates(coords)
    print(countries)
    response = ', '.join(countries)
    print(f"Sending Response: {response}")

    # Send the response back to the server
    s.sendall((response + '\n').encode())
    # Receive the server's reply (could be the next round or success message)
    reply = s.recv(4096).decode()
    print(f"Server Reply:\n{reply}")
    if "Congratulations" in reply or current_round == total_rounds:
        print("Challenge completed!")
        return False
    looprun(reply, s)
    

def connect_and_solve(host, port):
    """Connect to the nc server, receive data, solve it, and send the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to {host}:{port}")

        while True:
            # Receive data from the server
            data = s.recv(4096).decode()

            current_round, total_rounds = extract_round_info(data)
            if current_round is None or total_rounds is None:
                print("Could not extract round information. Exiting.")
                break

            print(f"Processing Round {current_round}/{total_rounds}")

            print(f"Received:\n{data}")

            # Check if the server closed the connection
            if not data:
                print("Connection closed.")
                break

            # Extract coordinates from the response
            coords = [line.strip() for line in data.splitlines() if 'Latitude:' in line and 'Longitude:' in line]
            # print(coords)

            # Get sorted country names
            countries = get_country_from_coordinates(coords)
            print(countries)
            response = ', '.join(countries)
            print(f"Sending Response: {response}")

            # Send the response back to the server
            s.sendall((response + '\n').encode())
            # Receive the server's reply (could be the next round or success message)
            reply = s.recv(4096).decode()
            
            print(f"Server Reply:\n{reply}")
            if "Congratulations" in reply or current_round == total_rounds:
                print("Challenge completed!")
                # break
            looprun(reply, s)


            # If the challenge is completed, exit the loop
            # if "Congratulations" in reply or "Correct!" in reply:
            #     print("Challenge completed!")
            #     break

if __name__ == "__main__":
    # Connect to the challenge server and solve it
    connect_and_solve('chall.cbctf.xyz', 33455)
