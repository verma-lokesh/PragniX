from pydantic import BaseModel


class MarketSignalBase(BaseModel):
    model_config = {"from_attributes": True}
