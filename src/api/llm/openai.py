import json

from api.endpoints.models import OnboardProject, Questionnaire
from api.llm.models import Prompt, Answer
from api.llm.prompts import GEN_QUESTIONNAIRE_PROMPT, FILL_IN_QUESTIONNAIRE_PROMPT
from api.config.config import OPEN_AI_API_KEY, logger
from openai import OpenAI

client = OpenAI(api_key=OPEN_AI_API_KEY)


def prompt_gen_questionnaire(context: str, template: str) -> Prompt:
    _prompt = template.replace("YOUR_CONTEXT_HERE", context)
    return Prompt(text=_prompt)


def prompt_answer_questions(transcript: str, questions: str, template: str) -> Prompt:
    _prompt = template.replace("TRANSCRIPT_HERE", transcript).replace("QUESTIONNAIRE_HERE", questions)
    return Prompt(text=_prompt)


async def questionnaire(pr: OnboardProject) -> Questionnaire:
    _prompt = prompt_gen_questionnaire(pr.questions, GEN_QUESTIONNAIRE_PROMPT)
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": _prompt.text},
        ]
    )
    resp = response.choices[0].message.content
    logger.debug(f"Questionnaire response: {resp}")
    try:
        q = Questionnaire(questions=json.loads(resp)['questions'])
    except:
        logger.error(f"Failed to create questionnaire for project {pr.name}")
        raise
    return q


async def answer_questions(transcript: str, questions: str) -> [Answer]:
    _prompt = prompt_answer_questions(transcript, questions, FILL_IN_QUESTIONNAIRE_PROMPT)
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": _prompt.text},
        ]
    )
    resp = response.choices[0].message.content
    logger.info(f"Answered questions: {resp}")
    try:
        return [Answer(**a) for a in json.loads(resp)['questions']]
    except:
        logger.error(f"Failed to answer questions")
        return []
