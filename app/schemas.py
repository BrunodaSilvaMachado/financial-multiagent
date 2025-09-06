from pydantic import BaseModel

class RunRequest(BaseModel):
    ticker: str
    horizon: str = "7d"
    risk: str = "medium"
