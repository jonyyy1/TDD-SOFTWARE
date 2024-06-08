from fastapi import FastAPI, HTTPException
import requests
import uvicorn
from geopy.distance import geodesic

app = FastAPI()

def fetch_coordinates(city_name: str):
    '''
    Function to fetch the coordinates of a given city using the Nominatim OpenStreetMap API.
    
    Parameters:
    city_name (str): The name of the city to find coordinates for.
    
    Returns:
    dict: A dictionary containing the latitude and longitude of the city.
    
    Raises:
    HTTPException: If the city is not found or there is an error in the API request.
    '''
    api_url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    headers = {
        'User-Agent': 'Testing App'
    }
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    
    if not response_data:
        raise HTTPException(status_code=404, detail="City not found")
    
    return {
        "latitude": response_data[0]['lat'],
        "longitude": response_data[0]['lon']
    }

@app.get("/get_coordinates/")
async def get_coordinates(city_name: str):
    '''
    API endpoint to get the coordinates of a given city.
    
    Parameters:
    city_name (str): The name of the city to find coordinates for.
    
    Returns:
    dict: A dictionary containing the latitude and longitude of the city.
    '''
    return fetch_coordinates(city_name)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    '''
    Function to calculate the distance between two geographical points.
    
    Parameters:
    lat1 (float): Latitude of the first point.
    lon1 (float): Longitude of the first point.
    lat2 (float): Latitude of the second point.
    lon2 (float): Longitude of the second point.
    
    Returns:
    dict: A dictionary containing the distance in kilometers.
    '''
    coordinates_point_1 = (lat1, lon1)
    coordinates_point_2 = (lat2, lon2)
    distance_km = geodesic(coordinates_point_1, coordinates_point_2).kilometers
    return {"distance": distance_km}

@app.get("/get_distance/")
async def get_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    '''
    API endpoint to calculate the distance between two geographical points.
    
    Parameters:
    lat1 (float): Latitude of the first point.
    lon1 (float): Longitude of the first point.
    lat2 (float): Latitude of the second point.
    lon2 (float): Longitude of the second point.
    
    Returns:
    dict: A dictionary containing the distance in kilometers.
    '''
    return calculate_distance(lat1, lon1, lat2, lon2)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
