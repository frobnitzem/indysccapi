from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import Header, Body
from sqlalchemy import func, select

from database import database, answers
from models import ProblemName, AnswerSummary
from check import check_answer
from app import app, validate_token

@app.get("/answers", response_model=Dict[str,int])
async def get_answers(authorization: str = Header('')):
    """Returns answers submitted by the team.
    """
    team = validate_token(authorization)

    query = select( answers.c.problem, func.count() ) \
              . where(answers.c.team == team) \
              . group_by(answers.c.problem)
    ans = await database.fetch_all(query)
    ret = dict(ans)
    # Fill out zeros in all missing categories.
    for problem in ProblemName:
        if problem.value not in ret:
            ret[problem.value] = 0
    return ret

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
@app.post("/answers/{problem_name}", response_model=Dict[str,Any])
async def set_answer(problem_name: ProblemName,
                     text: str = Body(''),
                     authorization: str = Header('')):
    """Appends the team's answer for the given problem.

    Returns a dictionary containing results from the
    validation.  If 'errors' are present, it contains
    a list of error strings otherwise explaining why
    the answer was not accepted.
    """
    timestamp = datetime.now()
    team = validate_token(authorization)

    replies = check_answer(problem_name, text)
    if 'errors' in replies and len(replies['errors']) > 0:
        return replies
    query = answers.insert().values(
                team = team,
                problem = problem_name.value,
                text = text,
                created_at = timestamp,
                )
    last_record_id = await database.execute(query)

    return replies
