from fastapi import FastAPI
from .router import RychlyRouter


class RychlyAPI(FastAPI):

    def __init__(self):
        self.app = FastAPI()
        
    def get_server(self):
        return self.app

    # Pointer must be a rychlyAPI Router (for now)
    def use(self, path, router: RychlyRouter):
        if not isinstance(router, RychlyRouter):
            raise Exception("router must be a rychlyAPI Router")
        
        router.activate_router(self.app, path)

    # Also allow paths to be defined not through a router

    def get(self, path, pointer):
        self.app.add_api_route(path, pointer, methods=['GET'])

    def post(self, path, pointer):
        self.app.add_api_route(path, pointer, methods=['POST'])

    def put(self, path, pointer):
        self.app.add_api_route(path, pointer, methods=['PUT'])

    def delete(self, path, pointer):
        self.app.add_api_route(path, pointer, methods=['DELETE'])
