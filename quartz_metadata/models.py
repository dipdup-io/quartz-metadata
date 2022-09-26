from tortoise import fields
from tortoise.queryset import QuerySet
from dipdup.models import Model

from quartz_metadata.const import ResolveTokenMetadataConst as Const


class ResolveToken(Model):
    id = fields.UUIDField(pk=True)
    network = fields.CharField(51)
    contract = fields.CharField(max_length=36)
    token_id = fields.CharField(max_length=16)
    token_metadata_uri = fields.TextField()
    resolved = fields.BooleanField(default=False, index=True)
    failures_count = fields.IntField(default=0, index=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)

    class Meta:
        table = "resolve_token"
        unique_together = (("network", "contract", "token_id"),)

    @classmethod
    def get_unresolved_chunk(cls) -> QuerySet:
        return (
            cls.filter(
                resolved=False,
                failures_count__lt=Const.failures_limit,
            )
            .order_by("created_at")
            .limit(Const.select_chunk_size)
        )

    async def set_resolved(self):
        if self.resolved:
            return
        self.resolved = True
        await self.save()

    async def set_failed(self):
        self.failures_count += 1
        await self.save()

    @property
    def url(self) -> str:
        return self.token_metadata_uri.replace(Const.placeholder, str(self.token_id))

    def __str__(self):
        return f"{self.network}_{self.contract}_{self.token_id}"
