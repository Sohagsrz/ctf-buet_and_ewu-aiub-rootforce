from geopy.geocoders import Nominatim
import sys

def get_country_from_coordinates(coords):
    geolocator = Nominatim(user_agent="geoapiExercises")
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

def main(input_file):
    try:
        with open(input_file, 'r') as file:
            coords = file.readlines()
            
        # Clean up coordinates and remove any whitespace, ignore invalid lines
        coords = [coord.strip() for coord in coords if coord.strip() and 'Latitude:' in coord and 'Longitude:' in coord]
        
        countries = get_country_from_coordinates(coords)
        print("Sorted Countries:", ', '.join(countries))

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'countries.txt' with your actual input file path
    input_file = 'countries.txt'
    main(input_file)
