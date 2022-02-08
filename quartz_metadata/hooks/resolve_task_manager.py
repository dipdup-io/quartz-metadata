from aiohttp import ClientConnectorError, ClientResponseError
from dipdup.context import HookContext

from quartz_metadata.manager import ResolveMetadataTaskManager
from quartz_metadata.models import ResolveToken


async def resolve_task_manager(
    ctx: HookContext,
) -> None:
    logger = ctx.logger
    client = ctx.get_http_datasource("aleph")

    while tasks_list := await ResolveToken.get_unresolved_chunk():
        logger.info(f"Processing {len(tasks_list)} unresolved tokens")

        for task in tasks_list:
            try:
                logger.info(f"Fetching metadata for token {task}")
                metadata = await client.get(task.url)

                await ctx.update_token_metadata(
                    network=task.network,
                    address=task.contract,
                    token_id=task.token_id,
                    metadata=metadata,
                )
                await task.set_resolved()
            except (ClientConnectorError, ClientResponseError):
                logger.warning(f"Metadata fetching failed for token {task}")
                await task.set_failed()

    ResolveMetadataTaskManager.finish()
    logger.info("Waiting for unresolved tokens...")
