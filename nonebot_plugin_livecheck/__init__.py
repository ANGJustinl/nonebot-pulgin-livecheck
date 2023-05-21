import httpx
from config import Config
from nonebot import get_driver, require
from nonebot.log import logger

__help_plugin_name__ = "bot存活检测"
__help_version__ = "0.1"
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


async def plugin_livecheck(url: str):
    async with httpx.AsyncClient(timeout=None) as client:
        resp = await client.get(
            url,
        )
        if resp.is_success is not True:
            logger.opt(colors=True).error("发送心跳包失败")
        logger.opt(colors=True).info("已发送心跳包")


if scheduler:
    url_list = env_config.livecheck_url
    if url_list is not list():
        url_list = list().append(url_list)
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
