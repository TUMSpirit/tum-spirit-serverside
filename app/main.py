from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from .src.routers import ai


def application_setup() -> FastAPI:
    ''' Configure, start and return the application '''

    # Start FastApi App
    application = FastAPI()

    # Mapping api routes
    application.include_router(ai.router)

    # Allow cors
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = application_setup()
