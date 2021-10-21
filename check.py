from typing import Dict, Any
from models import ProblemName, AnswerSummary

check_dict = {}

# Wrapper to simplify isolating problem checks.
# It doesn't do anything special to the function at all.
def answer(problem_name : ProblemName):
    def decorator(f):
        #print(f"creating decorator for {problem_name}")
        # This wrapper is not really called.  Instead, we
        # store it in a lookup table for validating 'problem_name'.
        check_dict[problem_name] = f
        def wrapper(answer : str) -> Dict[str,Any]:
            return f(answer)
        return wrapper
    return decorator

@answer(ProblemName.HPL)
def check_hpl(answer : str) -> Dict[str,Any]:
    return {}

@answer(ProblemName.HPCG)
def check_hpcg(answer : str) -> Dict[str,Any]:
    return {}

@answer(ProblemName.Gromacs)
def check_gromacs(answer : str) -> Dict[str,Any]:
    return {}

@answer(ProblemName.JohnTheRipper)
def check_jtr(answer : str) -> Dict[str,Any]:
    return {}

@answer(ProblemName.Mystery)
def check_mystery(answer : str) -> Dict[str,Any]:
    return {}

def check_answer(problem_name : ProblemName, answer : str) \
                                            -> Dict[str,Any]:
    """Provide feedback for the given answer.

    If the 'errors' key is returned it should contain a
    list of strings explaining the error.

    Returning a response without an 'errors' key (or with
    an empty errors list) means the answer is OK.

    The error messages should be VERY informative, since
    answers containing errors will not be counted (not added to DB).
    """
    if problem_name in check_dict:
        return check_dict[problem_name](answer)
    return {}

