from pydantic import BaseSettings

class Config(BaseSettings):
    livecheck_hour: int = 1
    livecheck_url: str
    class Config:
        extra = "ignore"
        case_sensitive = False
