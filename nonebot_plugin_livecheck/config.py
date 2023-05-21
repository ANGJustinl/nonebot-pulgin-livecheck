from pydantic import BaseSettings

class Config(BaseSettings):
    livecheck_hour: int = 1
    livecheck_url: list
    livecheck_team_token: str
    livecheck_statuspage_subdomain: str
    class Config:
        extra = "ignore"
        case_sensitive = False
