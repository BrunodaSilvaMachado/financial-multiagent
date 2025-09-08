from pydantic import BaseModel

class RunRequest(BaseModel):
    ticker: str
    horizon: str = "7d"
    risk: str = "medium"
    exchange: str = "br"  # 'br' for Brazilian market, 'us' for US market
