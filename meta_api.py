from fastapi import Header

from app import app, validate_token

@app.get("/team")
async def get_team(authorization: str = Header('')):
    return validate_token(authorization)
