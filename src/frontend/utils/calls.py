from aiohttp import ClientSession, ClientTimeout, ClientResponseError

from config.config import API_URL, logger


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


async def new_questionnaire(project):
    timeout = 10
    logger.debug(f"Uploading new project {project}")
    return await post_data("/questionnaire/new", project, timeout)
