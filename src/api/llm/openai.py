import json

from api.endpoints.models import OnboardProject, Questionnaire
from api.llm.models import Prompt
from api.llm.prompts import GEN_QUESTIONNAIRE_PROMPT
from api.config.config import OPEN_AI_API_KEY, logger
from openai import OpenAI

client = OpenAI(api_key=OPEN_AI_API_KEY)


def prompt(context: str, template: str) -> Prompt:
    _prompt = template.replace("YOUR_CONTEXT_HERE", context)
    return Prompt(text=_prompt)


async def questionnaire(pr: OnboardProject) -> Questionnaire:
    _prompt = prompt(pr.questions, GEN_QUESTIONNAIRE_PROMPT)
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
