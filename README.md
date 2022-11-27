# RychlyAPI

A fastAPI + uvicorn library that lets you create a Python based API even faster with integrated logging and the more readable router-controller model.   

## Dependencies
1. python = 3.10 
2. fastapi = 0.87.0
3. uvicorn = 0.19.0

## Fun Facts

Rychlý means fast in Czech :)

## Example

#### authController.py

```python
from rychlyapi import logger

logger.info("Initializing auth controller")

# API endpoint for auth
async def login(id: int):
    return {
        "message": "Log in!"
    }

async def register(username: str, password: str):
    return {
        "message": "Registered!"
    }
    
```

#### authRouter.py
```python
from rychlyapi import RychlyRouter, logger
from authController import login, register

logger.info("Initializing auth Router...")

authRouter = RychlyRouter()

authRouter.get('/register', register)
authRouter.get('/login/{id}', login)

```
#### main.py

```python
import argparse
from rychlyapi import RychlyAPI
from authRouter import authRouter

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
