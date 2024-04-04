from fastapi import Header, HTTPException


async def authorize(token: str = Header(alias='auth-token')):
    """
    Dependency to check secret token from "auth-token" header
    """
    if token != 'secret':
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return

