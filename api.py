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
