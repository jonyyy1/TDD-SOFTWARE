from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_coordinates(self):
        self.client.get("/get_coordinates/?city_name=New+York")

    @task
    def get_distance(self):
        self.client.get("/get_distance/?lat1=0&lon1=0&lat2=1&lon2=1")