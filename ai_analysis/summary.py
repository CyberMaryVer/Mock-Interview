import os
import openai
from loguru import logger
from typing import List
from time import time
from pydantic import BaseModel, Field
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

from ai_analysis.openai_tools import num_tokens_from_messages
from ai_analysis.prompts.screening import screening_assessment
from ai_analysis.prompts.tech import tech_assessment

# from dotenv import load_dotenv
# load_dotenv('./../../dev.env')

MODEL_DEFAULT = "gpt-3.5-turbo"
PROMPT_DEFAULT = """
Summarize the following text:
------------
{text}
------------

Write down the summary and the overall impression of the candidate.
Write down the main concerns about the candidate (e.g. overqualified, underqualified, not motivated, etc.).
Finally, write down the final decision: next stage, no next stage, or next stage with concerns.

Answer format:
1. Summary: ...
2. Overall impression: ...
3. Concerns: ...
   a. ...
   b. ...
4. Final decision: ...

Summary:
"""


class ScreeningAssessment(BaseModel):
    short_summary: str = Field(..., title="Short summary of the interview")
    strengths: List[str] = Field(..., title="List candidate's strengths (up to 1-2)")
    weaknesses: List[str] = Field(..., title="List candidate's weaknesses (up to 1-2)")
    concerns: List[str] = Field(..., title="List any possible concerns about the candidate")
    overall_impression: str = Field(..., title="Overall impression of the candidate: positive, neutral, negative")
    next_stage: str = Field(..., title="Is the candidate suitable for the next stage: yes, no, yes with concerns")


class TechAssessment(BaseModel):
    short_summary: str = Field(..., title="Short summary of the interview")
    skills: dict = Field(..., title="Candidate's score for each technical skill (1-10) mentioned in the transcript")
    tasks: List[dict] = Field(..., title="Score for each job task (1-10) mentioned in the transcript and comments")
    overall_impression: str = Field(..., title="Overall impression of the candidate")
    final_decision: str = Field(..., title="Final decision: hire, no hire, or hire with concerns")


def count_tokens(transcript, prompt=PROMPT_DEFAULT):
    messages = [{"role": "system", "content": f"{prompt} \'{transcript}\'"}]
    num_tokens = num_tokens_from_messages(messages)
    print("\033[96mNumber of tokens:", num_tokens, '\033[0m')
    return num_tokens


def get_prompt_object(prompt_text, prompt_variables=None):
    prompt_variables = ['text'] if prompt_variables is None else prompt_variables
    try:
        return PromptTemplate(template=prompt_text, input_variables=prompt_variables)
    except Exception as e:
        raise ValueError(f"Invalid prompt type: {e}")


def convert_text_to_docs(text, chunk_size=1200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    return text_splitter.create_documents([text])


def get_reduced_summary(transcript, api_key, mock_type='tech', prompt_text=PROMPT_DEFAULT, temperature=0.):
    prompt = PromptTemplate.from_template(prompt_text)
    llm = ChatOpenAI(temperature=temperature, model_name=MODEL_DEFAULT, openai_api_key=api_key)

    chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        question_prompt=prompt,
        return_intermediate_steps=False,
        input_key="input_documents",
        output_key="output_text",
    )
    docs = convert_text_to_docs(transcript)
    result = chain({"input_documents": docs}, return_only_outputs=True)

    return result, 0


def get_refined_summary(transcript, api_key, mock_type='tech', prompt_text=PROMPT_DEFAULT, temperature=0.):
    # if mock_type == 'tech':
    #     parser = PydanticOutputParser(pydantic_object=TechAssessment)
    # elif mock_type == 'screening':
    #     parser = PydanticOutputParser(pydantic_object=ScreeningAssessment)

    prompt = PromptTemplate.from_template(prompt_text)
    llm = ChatOpenAI(temperature=temperature, model_name=MODEL_DEFAULT, openai_api_key=api_key)

    refine_template = (
        "Your goal is to produce a precise final structured assessment with scores and comments\n"
        "We have provided an existing assessment up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing assessment by adding more details\n"
        "(only if needed and not changing the document structure) using the context below.\n\n"
        "------------\n"
        "{text}\n"
        "------------\n\n"
        "If the context isn't useful, return the original summary."
    )
    refine_prompt = PromptTemplate.from_template(refine_template)
    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=False,
        input_key="input_documents",
        output_key="output_text",
    )
    docs = convert_text_to_docs(transcript)
    result = chain({"input_documents": docs}, return_only_outputs=True)

    # try:
    #     parsed_output = parser.parse(result["output_text"])
    # except Exception as e:
    #     parsed_output = None

    return result, 0


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv('./../dev.env')

    # test_doc = './../db/interview_93729ee5-16f1-472f-9fec-af218ac95dcd.txt'
    test_doc = './../db/interview_2d757354-e06c-4752-ad33-4549569d0949.txt'
    api_key = os.getenv("OPENAI_API_KEY")
    print(api_key[:6] + "******************" + api_key[-6:])

    with open(test_doc, 'r') as f:
        txt = f.read()

    tok_count = count_tokens(txt + PROMPT_DEFAULT)
    start = time()
    print("Starting...")
    # summary, parsed = get_refined_summary(txt, api_key=api_key, prompt_text=PROMPT_DEFAULT)
    summary, parsed = get_reduced_summary(txt, api_key=api_key, prompt_text=PROMPT_DEFAULT)
    print(f"Elapsed time: {start - time():.2f} seconds")

    try:
        for sent in summary['output_text'].split('.'):
            print(sent)
    except Exception as e:
        print(e)
        print(summary)

    print(f"\033[93mParsed: {parsed}\033[0m")
    print(f"\033[93mNumber of tokens: {tok_count}\033[0m")
