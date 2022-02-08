from asyncio import sleep

import aiohttp
from aiohttp import ClientConnectorError, ContentTypeError
from dipdup.context import HookContext

from quartz_metadata.models import ResolveToken


async def resolve_token_metadata(
    ctx: HookContext,
) -> None:
    logger = ctx.logger
    block_time = 30
    token_limit = 1000
    failures_limit = 5
    placeholder = "{tokenId}"
    async with aiohttp.ClientSession() as session:
        while True:
            logger.info("Waiting for unresolved tokens...")

            tasks_list = (
                await ResolveToken.filter(
                    resolved=False, failures_count__lt=failures_limit
                )
                .order_by("created_at")
                .limit(token_limit)
            )
            if len(tasks_list) == 0:
                await sleep(block_time)
            else:
                logger.info(f"Processing {len(tasks_list)} unresolved tokens")
                for task in tasks_list:
                    logger.info(
                        f"Fetching metadata for token {task.contract}_{task.token_id}"
                    )
                    url = task.token_metadata_uri.replace(placeholder, task.token_id)
                    try:
                        async with session.get(url) as response:
                            task.token_metadata = await response.json()
                            task.resolved = True
                    except (ContentTypeError, ClientConnectorError):
                        logger.warning(
                            f"Metadata fetching failed for token {task.contract}_{task.token_id}"
                        )
                        task.failures_count += 1
                    finally:
                        await task.save()
