from django.shortcuts import render
import requests

# Replace with your actual API URL
API_URL = 'https://api.data.gov.in/resource/6732c416-5de6-4a14-9e9d-7366316436a3?api-key=579b464db66ec23bdd000001104f22e5aaa7405b7f9e699179320eb5&format=json&limit=1000'

def crime_map_view(request):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        records = data.get('records', [])
        districts = list(set(record['district'] for record in records if 'district' in record))
        districts.sort()
    except requests.RequestException as e:
        print(f"Error fetching districts from API: {e}")
        districts = []

    selected_district = request.GET.get('district', None)
    context = {'districts': districts, 'selected_district': selected_district}

    if selected_district:
        district_data = next((record for record in records if record['district'] == selected_district), None)
        if district_data:
            location = f"{district_data['district']}, {district_data['state_ut']}"
            lat, lon = fetch_lat_long(location)
            context['lat'] = lat
            context['lon'] = lon

            # Convert string values to integers, default to 0 if conversion fails
            try:
                rape_cases = int(district_data.get('rape', 0))
            except ValueError:
                rape_cases = 0

            context['crime_data'] = {
                'rape': rape_cases,
                'kidnapping_and_abduction': int(district_data.get('kidnapping_and_abduction', 0)),
                'dowry_deaths': int(district_data.get('dowry_deaths', 0)),
                'assault_on_women': int(district_data.get('assault_on_women', 0)),
                'insult_to_modesty': int(district_data.get('insult_to_modesty', 0)),
                'cruelty_by_husband': int(district_data.get('cruelty_by_husband', 0)),
                'importation_of_girls': int(district_data.get('importation_of_girls', 0)),
            }

            # Determine if the district is safe or unsafe
            context['is_safe'] = rape_cases <= 10

    return render(request, 'map_visualization/map.html', context)

def fetch_lat_long(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
    except requests.RequestException as e:
        print(f"Error fetching geocoding data: {e}")
    return None, None
