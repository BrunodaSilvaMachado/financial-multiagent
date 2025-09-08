from pydantic import BaseModel
from typing import Union, List

class RunRequest(BaseModel):
    ticker: Union[str,List[str]]
    horizon: str = "7d"
    risk: str = "medium"
    exchange: str = "br"  # 'br' for Brazilian market, 'us' for US market
