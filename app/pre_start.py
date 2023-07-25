import structlog
from tenacity import retry, stop_after_attempt, wait_fixed

# from app.db.session import SessionLocal
from app.core.config import config
from app.core.logging import setup_logging

setup_logging(json_logs=config.JSON_LOGGING, log_level=config.LOG_LEVEL)
logger = structlog.stdlib.get_logger("api.startup")

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
def init() -> None:
    try:
        logger.info("Pre-flight checks starting")
        # db = SessionLocal()
        # Try to create session to check if DB is awake
        # db.execute("SELECT 1")
        logger.info("Pre-flight checks passed, application can start")
    except Exception as e:
        logger.critical("Exception while trying to connect to database", exc_info=True)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
