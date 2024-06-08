from faker import Faker
from fastapi.testclient import TestClient
from app import app, fetch_coordinates
import pytest
import requests
from fastapi import HTTPException

client = TestClient(app)

@pytest.fixture
def fake():
    return Faker()

def test_can_call_existing_endpoints_of_the_API():
    response = client.get("/get_coordinates/?city_name=Lima, Peru")
    assert response.status_code == 200

def test_cannot_call_not_existing_endpoints_of_the_API():
    response = client.get("/get_coordinates/?city_name=ASDASDASDASD")
    assert response.status_code == 404

def test_endpoint_returns_something():
    response = client.get("/get_coordinates/?city_name=Lima, Peru")
    assert 'latitude' in response.json()
    assert 'longitude' in response.json()

def test_the_result_is_correct_for_simple_cases():
    test_cases = [
        {'city': 'New York', 'expected_lat': 40.7128, 'expected_lon': -74.0060},
        {'city': 'London', 'expected_lat': 51.5074, 'expected_lon': -0.1448},
    ]

    for case in test_cases:
        response = client.get(f"/get_coordinates?city_name={case['city']}")
        assert response.status_code == 200
        data = response.json()
        assert float(data['latitude']) == pytest.approx(case['expected_lat'], rel=0.01)
        assert float(data['longitude']) == pytest.approx(case['expected_lon'], rel=0.01)

def test_result_is_correct_for_generated_inputs(fake):
    for _ in range(10):  # Generar 10 nombres de ciudades aleatorios
        city_name = fake.city()
        response = client.get(f"/get_coordinates?city_name={city_name}")
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert 'latitude' in data and 'longitude' in data

def test_get_distance_success():
    response = client.get("/get_distance/?lat1=0&lon1=0&lat2=1&lon2=1")
    assert response.status_code == 200
    assert 'distance' in response.json()
    assert response.json()['distance'] >= 0

def test_get_distance_failure():
    response = client.get("/get_distance/?lat1=0&lon1=0")
    assert response.status_code == 422  

@pytest.mark.parametrize("city_name, expected_lat, expected_lon", [
    ("London", 51.5074, -0.1278),
    ("New York", 40.7128, -74.0060),
    ("Paris", 48.8566, 2.3522),
    ("Tokyo", 35.6895, 139.6917)
])
def test_the_result_is_correct_for_all_inputs_get_coordinates(city_name, expected_lat, expected_lon):
    response = client.get(f"/get_coordinates/?city_name={city_name}")
    assert response.status_code == 200
    data = response.json()
    assert abs(float(data["latitude"]) - expected_lat) < 1  # 1km tolerance
    assert abs(float(data["longitude"]) - expected_lon) < 1  # 1km tolerance

@pytest.mark.parametrize("lat1, lon1, lat2, lon2, expected_distance", [
    (51.5074, -0.1278, 48.8566, 2.3522, 343.56),  # London to Paris
    (40.7128, -74.0060, 34.0522, -118.2437, 3940),  # New York to Los Angeles
    (35.6895, 139.6917, 37.7749, -122.4194, 8289),  # Tokyo to San Francisco
    (52.5200, 13.4050, 41.9028, 12.4964, 1184)  # Berlin to Rome
])
def test_the_result_is_correct_for_all_inputs_get_distance(lat1, lon1, lat2, lon2, expected_distance):
    response = client.get(f"/get_distance/?lat1={lat1}&lon1={lon1}&lat2={lat2}&lon2={lon2}")
    assert response.status_code == 200
    data = response.json()
    assert abs(data["distance"] - expected_distance) < 5  # 5km tolerance

def test_fetch_coordinates_city_not_found(monkeypatch):
    def mock_requests_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return []
            
            @property
            def status_code(self):
                return 200
        return MockResponse()
    
    monkeypatch.setattr(requests, 'get', mock_requests_get)
    
    with pytest.raises(HTTPException) as excinfo:
        fetch_coordinates("NonExistentCity")
    
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "City not found"