# Instructions for preparing the plan for the interview
cv_analysis_instructions_tech = """
Evaluate the candidate's CV and the Job Description to determine technical fit for the role. 
Structure questions for the technical interview to validate experience, knowledge, and to clarify any concerns. 
Follow a logical sequence in asking questions.

JOB DESCRIPTION:
----------------
{job}
----------------

CV ANALYSIS:
----------------
{cv}
----------------

Return your findings as a JSON object, adhering to the template below. Use 'null' if data is unavailable.

Answer Template:

{
  "summary": {
    "current_role": "string",       // Current job title (CV)
    "experience": "string",             // Total years in the field (CV)
    "hard_skills": ["string"],          // Technical skills (CV)
    "tasks": ["string"]                 // Significant projects or tasks (CV)
  },
  "fit": {
    "hard_skills_fit": ["string"],      // Skills that match the job description (CV + Job Description)
    "tasks_fit": ["string"]             // Tasks aligned with job description (CV + Job Description)
  },
  "tech_concerns": ["string"],          // Concerns: irrelevant tech stack, buzzwords, lack of depth, etc. (CV + Job Description)
  "tech_interview_plan": {
    "task_related_questions_CV": "boolean",  // Include questions based on tasks performed in previous roles? (for Junior & Middle roles)
    "task_related_questions_JD": "boolean",  // Include questions based on tasks in the new role? (for all roles)
    "theory_related_questions": "boolean",   // Include questions to test technical theory? (for all roles)
    "system_design": "boolean",              // Include a system design question? (Only for Senior roles)
  }
}

JSON answer:
"""

tech_instructions = """
You are a Team Lead.
You are looking for a {seniority} {role} to join your team.

1. Prepare the questions for technical interview.
This job requires such skills as {skills} and experience with such tasks as {tasks}.
Ask questions to validate the candidate's experience and knowledge.
There are some key points that distinguish an experienced {seniority} {role} from an applicant who simply prepared well for the interview. 
Add a question that is very difficult to Google the answer to, but easy to answer if you have experience.
Here are some questions to test candidate's practical knowledge and experience. Some of them are tricky.

2. For each question, provide the desired brief answer and a bonus answer with a more detailed explanation
Example:
Q: Is it possible to use BERT to generate text? Why yes/no?
A: No, BERT is designed for classification problems, it is not a generative model.
Bonus: BERT can be adapted for such tasks, but it was not originally intended for text generation and there are more suitable models for this. 

3. Return the list of questions as a valid JSON object:
{"technical_questions": [
                    {"Q": "...", A: "...", Bonus: "..."}, 
                    {"Q": "...", A: "...", Bonus: "..."}, ...], # questions (up to 5-7) to check candidate's practical technical knowledge
 "questions_about_tasks": [
                    {"Q": "...", A: "...", Bonus: "..."}, 
                    {"Q": "...", A: "...", Bonus: "..."}, ...], # questions (up to 2-3) to check candidate's previous experience (tasks)
 "questions_about_theory": [
                    {"Q": "...", A: "...", Bonus: "..."}, 
                    {"Q": "...", A: "...", Bonus: "..."}, ...] # questions (up to 5-7) to check if the candidate truly understands the theory
}

JSON answer:
"""

tech_assessment = """
Given the interview transcript below, evaluate the candidate's performance during the interview. 
Write down the candidate's score for each technical skill (1-10) mentioned in the transcript
Write down the candidate's score for each job task (1-10) mentioned in the transcript and provide comments
Finally, write down the overall impression and final decision: hire, no hire, or hire with concerns. 

Return the final answer as a valid JSON object. Use 'null' if data is unavailable.


Transcript:
------------
{text}
------------

"""

tech_assessment_format = """
Format Example:
{  "short_summary": "...", # Short summary of the interview
  "skills": {"python": 10, "sql": 7, "aws": 3, "fastapi": 2, "pytorch": 9}, # Candidate's score for each technical skill
  "tasks": [
             {"Deploying a model": 8, "Comment": "Candidate answered the question correctly, demonstrated good knowledge of AWS and Docker"},
             {"Building a data pipeline": 5, "Comment": "Candidate struggled with the question, but demonstrated good knowledge of SQL and Python"},
             {"Big Data Processing": 3, "Comment": "Candidate struggled with the question, demonstrated lack of knowledge of Spark and Hadoop"},
             {"Data Labelling": 2, "Comment": "Candidate answered the question incorrectly, demonstrated lack of knowledge of main principles of data labelling"},
            ],
 "overall_impression": "string", # Overall impression of the candidate
 "final_decision": "string" # Final decision: hire, no hire, or hire with concerns
}


JSON answer:
"""