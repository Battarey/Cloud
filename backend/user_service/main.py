from fastapi import FastAPI
from registration.router import router as registration_router
from statistics.router import router as stat_router
from authorization.router import router as auth_router
from logout.router import router as logout_router
from delete_account.router import router as delete_account_router

app = FastAPI(title="User Service")
app.include_router(registration_router)
app.include_router(stat_router)
app.include_router(auth_router)
app.include_router(logout_router)
app.include_router(delete_account_router)

@app.get("/")
def read_root():
    return {"message": "User Service is running"}
