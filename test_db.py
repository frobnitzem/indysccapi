# File for testing out database queries.
#
import asyncio

from sqlalchemy import Table

from database import open_app, close_app, database, answers
from sqlalchemy import func, select, table, column
#from models import ProblemName, AnswerSummary, Team

async def test1():
    query = answers.select()
    print(query)
    x = await database.fetch_all(query)
    print(x)

async def test2():
    #print(dir(answers))
    query = select( answers.c.problem,
                    func.count() ) \
              . where(answers.c.team == 'UIUC') \
              . group_by(answers.c.problem)
    print(query)
    x = await database.fetch_all(query)
    print(x)

async def main():
    await open_app()
    await test1()
    await test2()
    await close_app()

asyncio.run(main())
