from dipdup.context import HandlerContext
from dipdup.models import Transaction
from tortoise.exceptions import IntegrityError

from quartz_metadata.models import ResolveToken
from quartz_metadata.types.ubisoft_quartz_minter.parameter.mint import MintParameter
from quartz_metadata.types.ubisoft_quartz_minter.storage import (
    UbisoftQuartzMinterStorage,
)


async def on_mint(
    ctx: HandlerContext,
    mint: Transaction[MintParameter, UbisoftQuartzMinterStorage],
) -> None:
    contract = mint.data.target_address
    token_id = mint.parameter.tokenid
    token_metadata_uri = mint.storage.token_metadata_uri

    try:
        await ResolveToken.create(
            contract=contract,
            token_id=token_id,
            token_metadata_uri=token_metadata_uri,
        )
    except IntegrityError:
        pass
