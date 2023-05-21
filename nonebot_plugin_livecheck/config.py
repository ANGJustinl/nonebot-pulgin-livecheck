from typing import Union, Optional
from pydantic import BaseSettings


class Config(BaseSettings):
    livecheck_hour: Optional[int] = 1
    livecheck_url: Optional[Union[str, list[str]]] = []
    livecheck_team_token: Optional[str]
    livecheck_statuspage_subdomain: Optional[str]

    class Config:
        extra = "ignore"
        case_sensitive = False
