from aiohttp import ClientSession, ClientTimeout, ClientResponseError
import requests
from config.config import API_URL, logger

from utils.models import NewProjectResponse


async def post_data(endpoint, data, timeout):
    headers = {
        "Content-Type": "application/json",
    }
    try:
        async with ClientSession(timeout=ClientTimeout(total=timeout), raise_for_status=True) as session:
            async with session.post(API_URL + endpoint, headers=headers, json=data) as response:
                result = await response.json()
            return result
    except ClientResponseError as e:
        print(f"Failed to get data: {e.status} {e.message}")
        raise


def post_data_sync(endpoint, data, timeout):
    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(API_URL + endpoint, headers=headers, json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get data: {e.response.status_code} {e.response.text}")
        raise


async def new_questionnaire(project) -> NewProjectResponse:
    timeout = 10
    logger.debug(f"Uploading new project {project}")
    resp = await post_data("/questionnaire/new", project, timeout)
    return NewProjectResponse(**resp)


def new_segment(segment):
    timeout = 10
    logger.debug(f"Uploading new segment {segment}")
    resp = post_data_sync("/questionnaire/segment", segment, timeout)
    return resp
