from typing import List, Dict, Any

from fastapi import Header, HTTPException
from sqlalchemy import func, select

from config import server_config
from database import database, answers
from server import app, validate_token
from models import ProblemName, Answer

def validate_admin(authorization) -> None:
    # Throw an error unless the authorization token belongs to admin.
    team = validate_token(authorization)
    if team != 'admin':
        raise HTTPException(
            status_code=404,
            detail="Admin Token Required",
            headers={"X-Error": "authentication error"},
        )

def fill_answer_stats(ans):
    ans = dict(ans)
    ret = []
    # Fill out zeros in all missing categories.
    for problem in ProblemName:
        ret.append(ans.get(problem.value, 0))
    return ret

async def full_stats():
    ret = {}
    cfg = server_config()
    for team in cfg.teams:
        if team.name in ["admin"]:
            continue
        query = select( answers.c.problem, func.count() ) \
                  . where(answers.c.team == team.name) \
                  . group_by(answers.c.problem)
        ans = await database.fetch_all(query)
        ret[team.name] = fill_answer_stats(ans)

    return {'problems': [p.value for p in ProblemName],
            'counts': ret
           }

@app.get("/admin/answers/{team_name}/{problem_name}",
         response_model=List[Answer])
async def get_full_answer(team_name: str,
                          problem_name: ProblemName,
                          authorization: str = Header('')):
    validate_admin(authorization)
    query = answers.select().where(answers.c.team == team_name) \
                            .where(answers.c.problem == problem_name.value)
    return await database.fetch_all(query)


@app.get("/admin/answers")#, response_model=Dict[str,Any])
async def get_full_stats(authorization: str = Header('')):
    validate_admin(authorization)

    return await full_stats()
