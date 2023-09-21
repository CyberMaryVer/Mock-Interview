import os
import json
import openai
import tiktoken
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


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
