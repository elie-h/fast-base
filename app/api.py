import time

import structlog
from asgi_correlation_id import CorrelationIdMiddleware, correlation_id
from databases import Database
from fastapi import Depends, FastAPI, Request, Response
from uvicorn.protocols.utils import get_path_with_query_string

from app.core.config import config
from app.core.deps.db import get_db
from app.core.logging import setup_logging
from app.db import db
from app.routes.v1.router import router_v1

setup_logging(json_logs=config.JSON_LOGGING, log_level=config.LOG_LEVEL)
access_logger = structlog.stdlib.get_logger("api.access")

app = FastAPI(title=config.PROJECT_NAME, openapi_url=f"{config.API_V1_STR}/openapi.json")


@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    if request.url.path == "/health":
        return await call_next(request)

    get_path_with_query_string(request.scope)  # type: ignore
    client_host = request.client.host  # type: ignore
    client_port = request.client.port  # type: ignore
    http_method = request.method
    http_version = request.scope["http_version"]
    structlog.contextvars.clear_contextvars()
    # These context vars will be added to all log entries emitted during the request
    request_id = correlation_id.get()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.perf_counter_ns()
    # If the call_next raises an error, we still want to return our own 500 response,
    # so we can add headers to it (process time, request ID...)
    response = Response(status_code=500)
    try:
        response = await call_next(request)
    except Exception:
        structlog.stdlib.get_logger("api.error").exception("Uncaught exception")
        raise
    finally:
        process_time = (time.perf_counter_ns() - start_time) / 1000000  # Convert to ms
        status_code = response.status_code
        # Recreate the Uvicorn access log format, but add all parameters as structured information
        access_logger.info(
            "Access",
            http={
                "url": str(request.url),
                "status_code": status_code,
                "method": http_method,
                "request_id": request_id,
                "http_version": http_version,
            },
            network={"client": {"ip": client_host, "port": client_port}},
            app={"version": config.VERSION},
            duration_ms=process_time,
        )
        response.headers["X-Process-Time-Ms"] = str(process_time)
        return response


if config.BACKEND_CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["X-Requested-With", "X-Request-ID", "*"],  # Redundant when "*" is used but added for clarity
        allow_headers=["X-Request-ID", "*"],  # Redundant when "*" is used but added for clarity
    )

if config.INJECT_SECURITY_HEADERS:
    from app.routes.middleware.security import SecurityHeadersMiddleware

    app.add_middleware(SecurityHeadersMiddleware, csp_enabled=config.INJECT_CSP_HEADERS)

if config.REDIRECT_HTTPS:
    from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

    app.add_middleware(HTTPSRedirectMiddleware)

if config.TRUSTED_HOSTS and config.TRUSTED_HOSTS != ["*"]:
    from fastapi.middleware.trustedhost import TrustedHostMiddleware

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.TRUSTED_HOSTS)

if config.GZIP_ENABLED:
    from fastapi.middleware.gzip import GZipMiddleware

    app.add_middleware(GZipMiddleware, minimum_size=config.GZIP_MIN_SIZE)


app.add_middleware(CorrelationIdMiddleware)
app.include_router(router_v1, prefix=config.API_V1_STR)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def hello(request: Request, db: Database = Depends(get_db)):
    res = await db.execute("SELECT 1")
    print(res)
    hello_logger = structlog.stdlib.get_logger("hello.logger")
    hello_logger.info("This is an info message from Structlog")
    hello_logger.warning("This is a warning message from Structlog, with attributes", an_extra="attribute")
    hello_logger.error("This is an error message from Structlog")
    return "Hello, World!"
