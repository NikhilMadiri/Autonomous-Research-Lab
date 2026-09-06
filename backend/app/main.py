from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.router import router
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.logging import configure_logging
from app.middleware.logging import RequestLoggingMiddleware
configure_logging(); logger = logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(RequestLoggingMiddleware); app.include_router(router, prefix=settings.api_prefix)
@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException): return JSONResponse(exc.status_code, {"success": False, "message": exc.message, "errors": exc.errors})
@app.exception_handler(RequestValidationError)
async def validation_handler(_: Request, exc: RequestValidationError): return JSONResponse(422, {"success": False, "message": "Validation failed", "errors": [{"field": ".".join(str(x) for x in e["loc"]), "message": e["msg"]} for e in exc.errors()]})
@app.exception_handler(Exception)
async def unexpected_handler(_: Request, exc: Exception): logger.exception("Unhandled exception", exc_info=exc); return JSONResponse(500, {"success": False, "message": "An unexpected error occurred", "errors": []})

