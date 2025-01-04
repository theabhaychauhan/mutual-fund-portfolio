from fastapi import FastAPI
from .routes import router

app = FastAPI()

# Include the registration router
app.include_router(router)
