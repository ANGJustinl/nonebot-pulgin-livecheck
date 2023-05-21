import os
import httpx
import json
from .config import Config
from nonebot import get_driver, require
from nonebot.log import logger

__help_plugin_name__ = "bot存活检测"
__help_version__ = "0.2-dev1"
__usage__ = """
向目标url发送心跳包以证明存活
""".strip()

env_config = Config(**get_driver().config.dict())

try:
    scheduler = require("nonebot_plugin_apscheduler")
    from nonebot_plugin_apscheduler import scheduler
except Exception:
    scheduler = None

logger.opt(colors=True).info(
    "已检测到软依赖<y>nonebot_plugin_apscheduler</y>, <g>开启Bot存活检测</g>"
    if scheduler
    else "未检测到软依赖<y>nonebot_plugin_apscheduler</y>，<r>禁用Bot存活检测</r>"
)

if not os.path.exists("data/livecheck"):
    os.makedirs("data/livecheck")
    logger.opt(colors=True).info("无url存储目录, 已在bot主目录 创建<y>data/livecheck</y>文件夹")


async def plugin_livecheck(url: str):
    async with httpx.AsyncClient(timeout=None) as client:
        resp = await client.get(
            url,
        )
        if resp.is_success is not True:
            logger.opt(colors=True).error("发送心跳包失败")
        logger.opt(colors=True).info("已发送心跳包")


if scheduler:
    url_list = list()
    url_list_cfg = env_config.livecheck_url
    with open("data/livecheck/livecheck_url.json", "r") as f:
        try:
            url_list_json = json.load(f)
        except Exception:
            url_list_json = []
    try:
        url_list.append(url_list_cfg)
        url_list.append(url_list_json)
        logger.opt(colors=True).info("<y>目标url</y>检录完成 " + str(url_list))
    except Exception as e:
        logger.opt(colors=True).error("<y>目标url</y>检录错误 " + str(e))
    if url_list is None:
        logger.opt(colors=True).error("无 <y>livecheck_url</y> 设置")
        raise ValueError
    else:
        hour = env_config.livecheck_hour
        z = zip(url_list, range(len(url_list)))
        for url, i in z:
            logger.opt(colors=True).info(
                "已设定于每 <y>{str(hour)}</y> 向 <y>{str(url)}</y> 定时发送心跳包"
            )
            scheduler.add_job(
                plugin_livecheck,
                "interval",
                hours=hour,
                id=f"plugin_livecheck_{i}",
                args=[url],
            )
