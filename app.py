from fastapi import FastAPI, HTTPException

from config import server_config
from database import open_app, close_app

app = FastAPI()

@app.on_event("startup")
async def startup():
    await open_app()

@app.on_event("shutdown")
async def shutdown():
    await close_app()

def validate_token(authorization) -> str:
    """validate the token, returning the team name on success
    The token format should be f'token {token}'.

    Raises: HTTPException if the token is not found.
    """
    prefix = "token "
    lp = len(prefix)
    if len(authorization) < lp or authorization[:lp] != prefix:
        raise HTTPException(
            status_code=404,
            detail="Authorization Token Required",
            headers={"X-Error": "authentication error"},
        )
    token = authorization[lp:]

    cfg = server_config()
    for team in cfg.teams:
        if token == team.token.get_secret_value():
            return team.name
    raise HTTPException(
        status_code=404,
        detail="Invalid Token",
        headers={"X-Error": "authentication error"},
    )
