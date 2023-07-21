from fastapi import FastAPI

from src.controller.controller import app_user_router, health_check_router, log_router, tenant_router

app = FastAPI()

app.include_router(
    router=health_check_router,
    prefix="/health_check",
    tags=["health_check"],
)

app.include_router(
    router=tenant_router,
    prefix="/tenant",
    tags=["tenant"],
)

app.include_router(
    router=app_user_router,
    prefix="/app_user",
    tags=["app_user"],
)

app.include_router(
    router=log_router,
    prefix="/log",
    tags=["log"],
)
