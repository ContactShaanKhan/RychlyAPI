# RychlyAPI

A router-controller library to use with FastAPI and uvicorn.   

1. Instead of using the traditional way of defining endpoints in FAST API - adopt the router-controller model.    
2. Integrated logger, simply import and log away with beautiful structured and colored logs

## TODO

1. Create examples to demonstrate how it is used

## Dependencies
1. python 3.10 
2. fastapi==0.87.0
3. uvicorn==0.19.0

## Fun Facts

Rychlý means fast in Czech :)

## Example

```python
import argparse
from lib.rychlyapi import RychlyAPI, RychlyRouter, logger

logger.info("Initializing endpoints...")

# API endpoint for auth
async def login(id: int):
    return {
        "message": "Log in!"
    }

async def register(username: str, password: str):
    return {
        "message": "Registered!"
    }


logger.info("Initializing auth Router...")

authRouter = RychlyRouter()

authRouter.get('/register', register)
authRouter.get('/login{id}', login)


def main():
    # Command line arguments
    parser = argparse.ArgumentParser(description="EXAMPLE SERVER")
    parser.add_argument("--port", help="Port to run the server on, default is 8000", default=8000, type=int)
    parser.add_argument("--host", help="Host to run the server on, default is 127.0.0.1", default="127.0.0.1")

    args = parser.parse_args()

    # We can use RychlyAPI features or fastAPI features directly here as both are returned by the context manager
    with RychlyAPI(log_request_time=True, host=args.host, port=args.port) as (app, fastapi_app):
        # Define Routers
        app.use('/auth', authRouter)


if __name__ == "__main__":
    main()

```
