from fastapi import FastAPI, Request
from .router import RychlyRouter
from time import perf_counter
from .logging import ColorFormatter, logger
import logging


class RychlyAPI():
    
    def __init__(self, log_request_time=False):
        self.app = FastAPI()

        # Setup some middleware now too
        @self.app.on_event("startup")
        async def startup_event():
            # Setup Logger
            logger = logging.getLogger("uvicorn")
            console_formatter = ColorFormatter(
                "[{asctime}][{process}][{location}][{levelprefix}]: {message}",
                style='{',
                use_colors=True
            )
            logger.handlers[0].setFormatter(console_formatter)
            logger.info("Logger initialized")

        if log_request_time:
            @self.app.middleware('http')
            async def log_requests_middleware(request: Request, call_next):
                interval = perf_counter()
                response = await call_next(request)
                interval = perf_counter() - interval
                logger.info(f"{request.client[0]}:{request.client[1]} - \"{request.method} {request.url.path}\" completed in {interval:0.12f} seconds")
                return response

    def get_server(self):
        return self.app

    # Pointer must be a rychlyAPI Router (for now)
    # TODO: Allow middleware to be done here: Install function pointers that are called or maybe fastapi has a way
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
