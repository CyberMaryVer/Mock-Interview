# Instructions for preparing the plan for the interview
cv_analysis_instructions_tech = """
Evaluate the candidate's CV and the Job Description to determine technical fit for the role. 
Structure questions for the technical interview to validate experience, knowledge, and to clarify any concerns. 
Follow a logical sequence in asking questions.

Return your findings as a JSON object, adhering to the template below. Use 'null' if data is unavailable.

Answer Template:

{
  "summary": {
    "current_position": "string",       // Current job title (CV)
    "experience": "string",             // Total years in the field (CV)
    "hard_skills": ["string"],          // Technical skills (CV)
    "tasks": ["string"]                 // Significant projects or tasks (CV)
  },
  "fit": {
    "hard_skills_fit": ["string"],      // Skills that match the job description (CV + Job Description)
    "tasks_fit": ["string"]             // Tasks aligned with job description (CV + Job Description)
  },
  "tech_concerns": ["string"],          // Concerns: irrelevant tech stack, buzzwords, lack of depth, etc. (CV + Job Description)
  "questions_to_clarify": ["string"],   // Questions to clarify any concerns
  "tech_interview_plan": {
    "task_related_questions_CV": "boolean",  // Questions based on tasks performed in previous roles (CV)
    "task_related_questions_JD": "boolean",  // Questions based on tasks in the new role (Job Description)
    "theory_related_questions": "boolean",   // Questions to test technical theory
    "system_design": "boolean",              // Include a system design question? (Optional)
  }
}

JSON answer:
"""

tech_instructions = """
You are a Team Lead.
Given the Job Description and the CV Analysis below:
Prepare the middle-level questions planned for technical interview.
Focus on incisive technical questions that thoroughly assess the candidate's depth of knowledge, rather than generic or behavioral queries. Create 5-7 questions per category, targeting specifics like implementation details, best practices, and differences between similar technologies..
Your objective is to formulate questions that will incisively evaluate the candidate's technical acumen and theoretical grasp, ensuring a match with job requirements.

Examples:
Bad: 'Tell me about your experience with AWS'
Good: 'Explain the trade-offs between using AWS Lambda and AWS EC2 for a compute-intensive application'

Return the list of questions as a valid JSON object:
{"technical_questions": ["...", "...",], # Specific questions (up to 5-7) to check candidate's technical knowledge (tools)
 "questions_about_tasks": ["...", "...",], # Specific questions (up to 2-3) to check candidate's previous experience (tasks)
 "questions_about_theory": ["...", "...", ], # Specific questions (up to 5-7) to check if the candidate truly understands the theory
}

JSON answer:
"""

tech_assessment = """
Given the interview transcript below, evaluate the candidate's performance during the interview. 
Write down the candidate's score for each technical skill (1-10) mentioned in the transcript
Write down the candidate's score for each job task (1-10) mentioned in the transcript
Finally, write down the overall impression and final decision: hire, no hire, or hire with concerns. 

Return your findings as a JSON object, adhering to the template below. Use 'null' if data is unavailable.

Example:
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

