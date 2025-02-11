import requests

def get_max_latitude(city, country):
    # Define the Nominatim API endpoint
    url = 'https://nominatim.openstreetmap.org/search'
    
    # Set up the parameters for the API request
    params = {
        'q': f'{city}, {country}',
        'format': 'json',
        'limit': 1,
        'email': 'your_email@example.com'  # Replace with your actual email
    }
    
    # Send the GET request to the Nominatim API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data:
            # Extract the bounding box from the first result
            bounding_box = data[0]['boundingbox']
            # The maximum latitude is the north latitude (second value in the bounding box)
            max_latitude = float(bounding_box[1])
            return max_latitude
        else:
            print('No data found for the specified city and country.')
            return None
    else:
        print(f'Error: Received status code {response.status_code}')
        return None

# Example usage:
city = 'Mumbai'
country = 'India'
max_lat = get_max_latitude(city, country)
if max_lat:
    print(f'The maximum latitude of the bounding box for {city}, {country} is {max_lat}')