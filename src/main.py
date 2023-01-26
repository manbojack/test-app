import logging

import uvicorn
from fastapi import FastAPI

import ping

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router, prefix="/ping_page")
    return application


app = create_application()


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
