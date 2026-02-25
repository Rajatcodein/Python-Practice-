
from fastapi import FastAPI
from crud_routes import router as crud_router
from Mithai_routes import router as Mithai_routes
app = FastAPI()

# Include the routes from crud_routes

app.include_router(crud_router)

app.include_router(Mithai_routes)