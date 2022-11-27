from fastapi import FastAPI, Request
import uvicorn
from .router import RychlyRouter
from time import perf_counter
from .logging import rychlyLogFormatter, logger
import logging

class RychlyAPI():
    
    # TODO: Fix how routes are done to do it the starlette recommended way (check decorator documentation for more info)
    # TODO: Allow middleware to be added the starlette way (starlette.middleware.base)

    # Host and port only need to be provided if using a context manager
    def __init__(self, log_request_time=False, host=None, port=None):
        self.app = FastAPI()

        self.host = host
        self.port = port

        # Initialize the uvicorn logger on startup
        @self.app.on_event("startup")
        async def startup_event():
            loggers = [ logging.getLogger("uvicorn"), logging.getLogger("uvicorn.access") ]
            
            for _logger in loggers:
                _logger.handlers[0].setFormatter(rychlyLogFormatter)
                
            loggers[0].info("Initialized logger")

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

    def launch_server(self, host, port, **kwargs):
        uvicorn.run(self.app, host=host, port=port, **kwargs)        

    def __enter__(self):
        if self.host is None or self.port is None:
            raise Exception("Host and port must be not None when using a context manager")

        return self, self.app

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.launch_server(self.host, self.port)

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
