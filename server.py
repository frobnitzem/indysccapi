from typing import List, Optional, Dict
from datetime import datetime

from fastapi import FastAPI, Header, Body, HTTPException
from sqlalchemy import func, select

from database import open_app, close_app, database, answers
from config import server_config
from models import ProblemName, AnswerSummary, Team

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

def check_answer(problem_name : ProblemName, answer : str) -> List[str]:
    """Provide a list of error strings for the given answer.

    Returning an empty list means the answer is OK.

    The error messages should be VERY informative, since
    answers failing this test should not be added to the DB.
    """
    return []

@app.get("/team")
async def get_team(authorization: str = Header('')):
    return validate_token(authorization)

@app.get("/answers", response_model=Dict[str,int])
async def get_answers(authorization: str = Header('')):
    """Returns answers submitted by the team.
    """
    team = validate_token(authorization)

    query = select( answers.c.problem, func.count() ) \
              . where(answers.c.team == team) \
              . group_by(answers.c.problem)
    ans = await database.fetch_all(query)
    return dict(ans)

@app.get("/answers/{problem_name}", response_model=List[AnswerSummary])
async def get_answer(problem_name: ProblemName,
                     authorization: str = Header('')):
    """Returns answers submitted by the team.
    """
    team = validate_token(authorization)

    query = answers.select().where(answers.c.team == team) \
                            .where(answers.c.problem == problem_name.value)
    #query = answers.count(answers.c.team == team)
    return await database.fetch_all(query)

# Not recommended - read request directly as binary data
@app.post("/answers/{problem_name}", response_model=List[str])
async def set_answer(problem_name: ProblemName,
                     text: str = Body(''),
                     authorization: str = Header('')):
    """Appends the team's answer for the given problem.

    Returns an empty list if the answer is accepted
    or else a list of error strings otherwise.
    """
    timestamp = datetime.now()
    team = validate_token(authorization)

    errors = check_answer(problem_name, text)
    if len(errors) > 0:
        return errors
    query = answers.insert().values(
                team = team,
                problem = problem_name.value,
                text = text,
                created_at = timestamp,
                )
    last_record_id = await database.execute(query)

    return []
