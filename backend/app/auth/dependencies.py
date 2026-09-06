from typing import Annotated
from fastapi import Depends
from app.auth.interfaces import IdentityProvider
async def get_identity_provider() -> IdentityProvider | None: return None
CurrentIdentity = Annotated[IdentityProvider | None, Depends(get_identity_provider)]

