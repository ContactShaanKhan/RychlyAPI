from fastapi import APIRouter, FastAPI

'''
    A library similar to express routers making routing for fast api easy
''' 

class RychlyRouter():

    def __init__(self, ):
        self.fastRouter = APIRouter()
        self.endpoints = []

    # Initiates all the endpoints
    def activate_router(self, app: FastAPI, base_path):
        # Iterate out of all the endpoint skeletons
        for http_type, path, pointer in self.endpoints:
            app.add_api_route("{}{}".format(base_path, path), pointer, methods=[http_type])

    def get(self, path, pointer):
        self.endpoints.append(('GET', path, pointer))

    def post(self, path, pointer):
        self.endpoints.append(('POST', path, pointer))

    def put(self, path, pointer):
        self.endpoints.append(('PUT', path, pointer))

    def delete(self, path, pointer):
        self.endpoints.append(('DELETE', path, pointer))
