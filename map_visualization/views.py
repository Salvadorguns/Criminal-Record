import requests
from django.shortcuts import render

# Replace with your API URL
API_URL = 'https://api.data.gov.in/resource/6732c416-5de6-4a14-9e9d-7366316436a3?api-key=579b464db66ec23bdd000001104f22e5aaa7405b7f9e699179320eb5&format=json&limit=1000'

def crime_map_view(request):
    try:
        # Fetch data from the API
        response = requests.get(API_URL)
        response.raise_for_status()  # Ensure we raise an error for bad responses
        data = response.json()

        # Extract districts from the response
        records = data.get('records', [])
        districts = list(set(record['district'] for record in records if 'district' in record))

        # Sort the district names
        districts.sort()

    except requests.RequestException as e:
        print(f"Error fetching districts from API: {e}")
        districts = []  # Fallback if the API fails

    # Get the selected district from the query parameters
    selected_district = request.GET.get('district', None)

    context = {
        'districts': districts,
        'selected_district': selected_district,
    }

    if selected_district:
        # Filter to get the data for the selected district
        district_data = next((record for record in records if record['district'] == selected_district), None)

        # Fetch latitude and longitude for the selected district (if available)
        if district_data:
            # Use the `district` and `state_ut` fields to get lat/long from a geocoding API
            location = f"{district_data['district']}, {district_data['state_ut']}"
            lat, lon = fetch_lat_long(location)
            context['lat'] = lat
            context['lon'] = lon

    return render(request, 'map_visualization/map.html', context)


# Function to get latitude and longitude using a geocoding API
def fetch_lat_long(location):
    # Replace with your geocoding API (e.g., OpenStreetMap or Google Maps API)
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
    return None, None  # Fallback if no lat/long found
