from fastapi import FastAPI

from api import crud, access, log

app = FastAPI( title="API for bariier control via MTC Exolve",
    description="This API requires an API key in the X-API-Key header demo key is 12345",
    version="1.0.0")

app.include_router(access.router) # Use the router
app.include_router(log.router) # Use the router
app.include_router(crud.router) # Use the router
