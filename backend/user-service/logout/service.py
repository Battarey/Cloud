from security.tokens.refresh import revoke_refresh_token

async def logout_user_service(refresh_token: str):
    await revoke_refresh_token(refresh_token)
    return {"status": "logged out"}
