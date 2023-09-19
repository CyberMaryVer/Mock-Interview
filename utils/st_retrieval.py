import os
import uuid
import pandas as pd
from loguru import logger


def load_unique_ids():
    """
    This function loads unique ids from the database
    """
    db = pd.read_csv("./db/plans.csv")
    return db["plan_id"].unique().tolist()


def load_interview_plan(plan_id):
    """
    This function loads interview plan from the database
    """
    # If plan_id is not specified, load default plan
    if plan_id == '1':
        plan_type = "screening"
        questions = ["Tell me about yourself.",
                     "What are your strengths?",
                     "What are your weaknesses?",
                     "Why do you want this job?",
                     "Where would you like to be in your career five years from now?",
                     "What's your ideal company?",
                     "What attracted you to this company?",
                     "Why should we hire you?",
                     "What did you like least about your last job?",
                     "When were you most satisfied in your job?",
                     "What can you do for us that other candidates can't?",
                     "What were the responsibilities of your last position?",
                     "Why are you leaving your present job?"]
    else:
        db = pd.read_csv("./db/plans.csv")
        plan = db[db["plan_id"] == plan_id]
        plan_type = plan["plan_type"].tolist()[0]
        questions = plan["question"].tolist()

    return questions, plan_type
