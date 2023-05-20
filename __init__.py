from nonebot import require, get_driver
from nonebot.log import logger

from .config import Config
from .get import get

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
    "已检测到软依赖<y>nonebot_plugin_apscheduler</y>, <g>开启存活检测</g>"
    if scheduler
    else "未检测到软依赖<y>nonebot_plugin_apscheduler</y>，<r>禁用存活检测</r>"
)


async def plugin_livecheck(check_url: str):
    resp = await get(url=check_url)
    if resp.is_success is not True:
        logger.opt(colors=True).error(
            f"发送心跳包失败"
            )

    logger.opt(colors=True).info(
                f"已发送心跳包"
            )

if scheduler:
    hour = env_config.livecheck_hour
    url = env_config.livecheck_url
    logger.opt(colors=True).info(
            f"已设定于每 <y>{str(hour)}</y> 向 <y>{str(url)}</y> 定时发送心跳包"
        )
    
    scheduler.add_job(
        plugin_livecheck, "interval",
        hours=hour, id=f"plugin_livecheck", args=[url]
        )
