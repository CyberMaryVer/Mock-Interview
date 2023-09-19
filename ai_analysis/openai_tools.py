import os
import json
import openai
from loguru import logger

OPENAI_KEY = os.getenv('OPENAI_API_KEY', None)


def openai_response(messages, api_key=None, with_content=False):
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=messages,
                                                api_key=api_key)
        msg = response.choices[0].message
        if with_content:
            return msg
        return msg.content
    except openai.error.AuthenticationError as e:
        # Handle authentication error here
        logger.error(f"OpenAI API authentication error: {e}")
        raise e
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        logger.error(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        logger.error(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass


def openai_response_with_validation(messages, api_key):
    is_json = False
    while not is_json:
        try:
            json_response = openai_response(messages, api_key)
            json.loads(json_response)
            is_json = True
            return json_response
        except openai.error.AuthenticationError as e:
            raise e
        except Exception as e:
            logger.error(f"JSON Validation Error: {e}. Retrying...")


def openai_response_for_text(prompt, api_key):
    messages = [
        {"role": "system", "content": "You are an experienced hiring manager. "},
        {"role": "user", "content": prompt}]
    return openai_response(messages, api_key)


def check_if_key_valid(api_key):
    try:
        openai.api_key = api_key
        openai.Engine.list()
        return True
    except openai.error.AuthenticationError as e:
        return False
    except Exception as e:
        logger.error(f"Error: {e}")
        return False
