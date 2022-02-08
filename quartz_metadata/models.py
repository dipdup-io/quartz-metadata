from tortoise import Model, fields


class ResolveToken(Model):
    id = fields.UUIDField(pk=True)
    contract = fields.CharField(max_length=36)
    token_id = fields.CharField(max_length=16)
    token_metadata_uri = fields.TextField()
    resolved = fields.BooleanField(default=False, index=True)
    token_metadata = fields.TextField(null=True)
    failures_count = fields.IntField(default=0, index=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)

    class Meta:
        table = "resolve_token"
        unique_together = (("contract", "token_id"),)
