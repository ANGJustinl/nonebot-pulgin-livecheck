import httpx

TEAM_TOKEN = 'ka6xJpfnxeaeRjAvNvxNvxj3'

async def get_monitors(TEAM_TOKEN):
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        url='https://betteruptime.com/api/v2/monitors'
        resp = await client.post(
            url, headers=f"Authorization: Bearer {TEAM_TOKEN}"
        )
        result = resp.is_success
        return result


get_monitors(TEAM_TOKEN)