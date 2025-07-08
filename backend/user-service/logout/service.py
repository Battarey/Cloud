from security.tokens.refresh import revoke_refresh_token

async def logout_user_service(refresh_token: str):
    from fastapi import HTTPException
    from security.tokens.refresh import get_user_id_by_refresh
    exists = await get_user_id_by_refresh(refresh_token)
    if not exists:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    await revoke_refresh_token(refresh_token)
    return {"status": "logged out"}
