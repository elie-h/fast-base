import structlog
from tenacity import retry, stop_after_attempt, wait_fixed

from alembic import command

# from app.db import db
from alembic.config import Config
from app.core.config import config
from app.core.logging import setup_logging

setup_logging(json_logs=config.JSON_LOGGING, log_level=config.LOG_LEVEL)
logger = structlog.stdlib.get_logger("api.startup")

max_tries = 60 * 1  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
async def init() -> None:
    try:
        logger.info("Pre-flight checks starting")
        # await db.connect()
        # await db.execute("SELECT 1")
        # await db.disconnect()
        logger.info("Pre-flight checks passed, application can start")
    except Exception as e:
        logger.critical("Exception while trying to connect to database", exc_info=True)
        raise e


def run_migrations() -> None:
    logger.info("Running migrations")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Migrations have been run")


async def main() -> None:
    logger.info("Initializing service")
    await init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    run_migrations()
