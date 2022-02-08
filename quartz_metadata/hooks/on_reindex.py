from dipdup.context import HookContext

from quartz_metadata.models import ResolveToken


async def on_reindex(
    ctx: HookContext,
) -> None:
    await ResolveToken.all().delete()
