import asyncio
import logging

from log import LoguruHandler

aps_logger = logging.getLogger("apscheduler")
aps_logger.setLevel(logging.DEBUG)
aps_logger.handlers.clear()
aps_logger.addHandler(LoguruHandler())

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.tasks.update_item_demand import get_item_demand


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    job = scheduler.add_job(get_item_demand, "interval", minutes=5)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
