from typing import Protocol


class IdentityProvider(Protocol):
    async def current_identity(self) -> object | None: ...
