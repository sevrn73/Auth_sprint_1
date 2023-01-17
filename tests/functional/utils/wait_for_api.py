import asyncio
import logging
from http import HTTPStatus

import aiohttp
import backoff

from settings import TEST_SETTINGS


logger = logging.getLogger("tests")

def backoff_handler(details):
    logger.info("API is unavailable - sleeping")

@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=60,
)
async def wait_for_api(url):
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with session.get(url) as response:
            return response.status

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    logger.info('Waiting for Auth API')
    status = loop.run_until_complete(wait_for_api(TEST_SETTINGS.SERVICE_URL))
    if status == HTTPStatus.OK:
        logger.info('Auth API is started')


