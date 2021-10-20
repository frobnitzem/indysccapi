from pydantic import BaseModel, SecretStr
from datetime import datetime

from enum import Enum

#class AnswerIn(BaseModel):
#    team: str
#    problem: str
#    text: str

class AnswerSummary(BaseModel):
    team: str
    problem: str
    created_at: datetime

class Answer(BaseModel):
    id: int
    team: str
    problem: str
    text: str
    created_at: datetime

class ProblemName(str, Enum):
    HPL = "HPL"
    HPCG = "HPCG"
    Gromacs = "Gromacs"
    JohnTheRipper = "JohnTheRipper"
    Mystery = "Mystery"

# These are tokens that each team will
# use to authenticate to the API.
class Team(BaseModel):
    name: str
    token: SecretStr
