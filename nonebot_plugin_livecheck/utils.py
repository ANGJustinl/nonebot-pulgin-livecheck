import httpx
from json import loads

async def create_heartbeat(TEAM_TOKEN, heartbeat_name):
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        url='https://betteruptime.com/api/v2/heartbeats'
        headers={'Authorization': f'Bearer {TEAM_TOKEN}'}
        data = {'name':heartbeat_name, 'period':7200, 'email':True, 'push':True, 'grace':1000}
        resp = await client.post(url, headers=headers, data=data)
        status = resp.is_success
        result = resp.text
        data_out = loads(result)
        url_out = data_out["data"]["attributes"]["url"] # 难看的取值
        resource_id = data_out["data"]["id"]
        return [status, result, url_out, resource_id]

async def create_statuspage(TEAM_TOKEN, subdomain):
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        url='https://betteruptime.com/api/v2/status-pages'
        headers={'Authorization': f'Bearer {TEAM_TOKEN}'}
        data = {
            'company_name':'Nonebot服务状态',
            'company_url':'https://github.com/ANGJustinl/nonebot-pulgin-livecheck',
            'logo_url':'https://nb2.baka.icu/logo.png',
            'timezone':'Asia/Shanghai',
            'history':90,
            'subdomain':subdomain
            }
        resp = await client.post(url, headers=headers, data=data)
        status = resp.is_success
        result = resp.text
        data_out = loads(result) # 难看的取值
        if status is False:
            return data_out
        domain = str(subdomain) + ".betteruptime.com"
        status_page_id = data_out["data"]["id"]
        return [status, result, data_out, domain, status_page_id]
    
async def add_page_section(TEAM_TOKEN, status_page_id):
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        url=f'https://betteruptime.com/api/v2/status-pages/{status_page_id}/sections'
        headers={'Authorization': f'Bearer {TEAM_TOKEN}'}
        data = {'name':'自动生成服务状态'}
        resp = await client.post(url, headers=headers, data=data)
        status = resp.is_success
        result = resp.text
        try:
            section_id = loads(result)["data"]["id"] # 难看的取值
            return section_id
        except:
            return [status, result]

async def add_page_resource(TEAM_TOKEN, status_page_id, resource_id_list, heartbeat_name_list, status_page_section_id,):
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        url=f'https://betteruptime.com/api/v2/status-pages/{status_page_id}/resources'
        headers={'Authorization': f'Bearer {TEAM_TOKEN}'}
        z = zip(resource_id_list, heartbeat_name_list)
        for resource_id, heartbeat_name in z:
            data = {'status_page_section_id':status_page_section_id,'resource_id':resource_id, 'resource_type':'Heartbeat', 'public_name':heartbeat_name}
            resp = await client.post(url, headers=headers, data=data)
            status = resp.is_success
            if status is not True:
                result = resp.text
                return [status, result]
            result = resp.status_code
        return [status, result]

