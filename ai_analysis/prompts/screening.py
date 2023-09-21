# Instructions for preparing the plan for the interview
cv_analysis_instructions_screening = """
Analyze the candidate's CV and the Job Description to assess suitability for the role. 
Prepare questions for a phone screening interview to clarify any concerns. 
Return your findings as a well-structured JSON object. Use 'null' if information is unavailable. 

JOB DESCRIPTION:
----------------
{job}
----------------

CV ANALYSIS:
----------------
{cv}
----------------

Answer Template:

{
  "summary": {
    "current_role": "string",  // Current role (CV)
    "experience": "float",        // Total years of experience (CV)
    "education": "string",         // Educational background (CV)
    "hard_skills": ["string"],     // Technical skills (CV)
    "tasks": ["string"],           // Completed tasks or projects (CV)
    "soft_skills": ["string"]      // Interpersonal skills (CV)
  },
  "fit": {
    "hard_skills_fit": ["string"],  // Matching technical skills (CV + Job Description)
    "tasks_fit": ["string"],         // Matching tasks (CV + Job Description)
    "experience_fit": "string",      // Experience fit: ['>>','>=','<','<<'] (CV + Job Description)
    "experience_gap": "boolean"      // Presence of career gaps (CV)
  },
  "concerns": ["string"],            // Potential issues: motivation, gaps, etc. (CV + Job Description)
  "questions_to_clarify": ["string"],// Questions to resolve concerns
  "screening_plan": {
    "salary": "boolean",                // Query candidate's salary expectation
    "motivation_to_change": "boolean",  // Query reason for job change
    "gaps": "boolean",                  // Inquire about career gaps
    "experience_match": "boolean",      // Confirm experience relevance
    "experience_with_stack": "boolean", // Confirm tech stack familiarity
    "notice_period": "boolean",         // Determine notice period
    "candidate_questions": "boolean"    // Ask if the candidate has any questions
  }
}

JSON answer:
"""

screening_instructions = """
You are a recruiter. 
Given the Job Description below, create a list of 5-7 questions to check job requirements.

Given the CV Analysis below:
Prepare the questions planned for phone screening interview which will help you to understand if the candidate is a really good fit.
Note: you don't need to ask technical questions during the screening interview, just check the candidate's experience and motivation.
Note: don't ask very general questions like "What soft skills do you have?" or "What are your strengths and weaknesses?". Be specific.

Return the list of questions as a valid JSON object:
{"icebreaker": ["..."], # Icebreaker question to start the interview (up to 1-2)
  "questions_to_check_motivation": ["...", "...",], # List of questions (up to 1-2) to check motivation to change the job
  "questions_to_check_fit": ["...", "...", "...", ], # List of main questions (up to 1-2) to check job requirements
  "questions_to_clarify": ["...", "...", ] # List additional questions (up to 2-4) to clarify the existing concerns about the candidate
}

JSON answer:
"""

screening_assessment = """
Given the interview transcript below, evaluate the candidate's performance during the interview. 
Evaluate candidate's soft skills, write down any possible concerns (e.g. motivation, cultural fit, unclear impact etc.).
Write down the candidate's strengths and weaknesses. 
Write down the overall impression of the candidate.
Finally, write down the candidate's final decision: next stage, no next stage, or next stage with concerns.

Transcript:
------------
{text}
------------

Return the final answer as a valid JSON object:

"""

scr_assessment_format = """
Format Example:
{   "short_summary": "...", # Short summary of the interview
    "strengths": ["...", "...",], # List candidate's strengths (up to 1-2)
    "weaknesses": ["...", "...",], # List candidate's weaknesses (up to 1-2)
    "concerns": ["...", "...",], # List any possible concerns about the candidate
    "overall_impression": "...", # Overall impression of the candidate: positive, neutral, negative
    "next_stage": "...", # Is the candidate suitable for the next stage: yes, no, yes with concerns
}

JSON answer:
"""