from dipdup.context import HookContext

from quartz_metadata.manager import ResolveMetadataTaskManager


async def on_synchronized(ctx: HookContext) -> None:
    await ResolveMetadataTaskManager.process_resolve_tasks(ctx)
