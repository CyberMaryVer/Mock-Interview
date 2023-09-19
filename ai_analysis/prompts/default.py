cv_analysis_default_instructions = """
Analyze candidate's CV and Job Description. 
Compare the candidate's CV with the Job Description and find out if the candidate is a good fit for the job.
Prepare the questions planned for phone screening interview which will help you to understand if the candidate is a really good fit for this position, and clarify the existing concerns about the candidate if any (True if question is planned, False otherwise).

Return the answer as a valid JSON object (use null if the answer is not available).
Answer Template:
{"summary": {"current_position": "...",  # What is the candidate's current position? (CV)
                "experience": "...", # Candidate's experience in years (CV)
                "education": "...", # Candidate's education (CV)
                "hard_skills": ["...", "...", "..."], # List candidate's hard skills: software, platforms (CV)
                "tasks": ["...", "...", "..."], # List tasks that have been solved by candidate (CV)
                "soft_skills": ["...", "...", "..."]}, # List candidate's soft skills (CV)
"fit":  {"hard_skills_fit": ["...", "...", "..."], # Same or similar hard skills as in the job description (CV + Job Description)
          "tasks_fit": ["...", "...", "..."], # Same or similar tasks as in the job description (CV + Job Description)
          "experience_fit": "...", # Does candidate have the required experience: ['>>','>=','<','<<']? (CV + Job Description)
          "experience_gap": ..., # Are there any gaps? (CV)
"concerns": ["...", "...", "..."], # List any possible concerns about the candidate: motivation, gaps, experience, non-relevant tasks, etc. (CV + Job Description)
"questions_to_clarify": ["...", "...", "..."], # List additional questions to clarify the existing concerns about the candidate if any
"screening_plan": {"salary": True, # What is the candidate's expected salary?
                "motivation_to_change": True, # What is the candidate's motivation to change the job?
                "gaps": ..., # Ask if there are any gaps in the candidate's CV
                "experience_match": ..., # Ask if the candidate's experience is close to the job description
                "experience_with_stack": ..., # Ask if the candidate has experience with the required stack
                "notice_period": True,     # What is the candidate's notice period?
                "candidate_questions": True, # Does candidate have any questions?
                },
}
"""

job_analysis_default_instructions = """
Analyze job description. Summarize job description according to the following template:

Return the answer as a valid JSON object:
{"position_title": "...", # What is the position's title?
 "seniority_level": "...", # What is seniority level of the position (C-level | Senior | Middle | Junior)?
 "experience": "...", # How many years of experience is required for the position?
 "hard_skills": ["...", "...", "..."], # List the main hard skills required for the position (software, platforms, etc.).
 "soft_skills": ["...", "...", "..."], # List the main soft skills required for the position.
 "tasks": ["...", "...", "..."], # List the tasks that candidate should have experience with.
 "must_have_skills": ["...", "...", "..."], # List the must have skills for the position.
 "bonus_skills": ["...", "...", "..."]} # List the bonus skills that nice to have for the position if any.
"""

assesment_default = """
Given the interview transcript below, write a short summary of the interview. 
Evaluate the candidate's strengths and weaknesses, and write down your concerns and recommendations. 
Write down the conclusion and the next steps. 
"""
