from nonebot import require, get_driver, on_command
from nonebot.log import logger
from nonebot.permission import SUPERUSER

import uuid

from .utils import create_heartbeat, create_statuspage, add_page_resource, add_page_section
from .config import Config

env_config = Config(**get_driver().config.dict())

TEAM_TOKEN = env_config.livecheck_team_token
subdomain = env_config.livecheck_statuspage_subdomain

statuspage_generation = on_command("生成服务页面", aliases={"statuspage_generate", "生成页面"}, block=True, priority=12, permission=SUPERUSER)
error_cmd = "请检查命令行提示"

@statuspage_generation.handle()
async def statuspage_generate(TEAM_TOKEN, heartbeat_name, subdomain):
    if TEAM_TOKEN == None:
        logger.opt(colors=True).error(
            "<y>无TEAM_TOKEN</y> "
            )
        statuspage_generate.finish('无TEAM_TOKEN')

    try:
        if heartbeat_name is not list():
            heartbeat_name_list = list()
            heartbeat_name_list.append(heartbeat_name)
        resource_id_list = list()
        heartbeat_url_list = list()
        #创建心跳包检测
        for heartbeat_name in heartbeat_name_list:
            resource_id = await create_heartbeat(TEAM_TOKEN, heartbeat_name=heartbeat_name)
            resource_id_list.append(resource_id[3])
            heartbeat_url_list.append(resource_id[2])
    except Exception as e:
        logger.opt(colors=True).error(
            "<y>心跳包检测</y>创建失败 "+str(e)
            )
        statuspage_generate.finish('心跳包检测创建失败'+error_cmd)

    if subdomain is not str():
        subdomain = uuid.uuid1()
        logger.opt(colors=True).warn(
            "未设置 <y>subdomain</y> ,将以uuid为二级域名"
            )
        
    try:
        status_page_id = await create_statuspage(TEAM_TOKEN, subdomain=subdomain)[4]
    except Exception as e:
        logger.opt(colors=True).error(
            "<y>Status page</y> 页面创建失败 "+str(e)
            )
        statuspage_generate.finish('Status page创建失败'+error_cmd)

    try:
        status_page_section_id = await add_page_section(TEAM_TOKEN, status_page_id)
    except Exception as e:
        logger.opt(colors=True).error(
            "<y>Status page</y> 页面分页创建失败 "+str(e)
            )
        statuspage_generate.finish('Status page分页创建失败'+error_cmd)

    a = await add_page_resource(TEAM_TOKEN, status_page_id, resource_id_list, heartbeat_name_list, status_page_section_id)

    if a[1] == 201:
        logger.opt(colors=True).info(
            "页面创建成功,打开 <y>https://"+str(subdomain)+'.betteruptime.com</y> 访问你的页面!'
            )
        statuspage_generate.finish('页面创建成功,打开 https://'+str(subdomain)+'.betteruptime.com 访问你的页面!')
        