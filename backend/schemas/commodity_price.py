from pydantic import BaseModel


class CommodityPriceBase(BaseModel):
    model_config = {"from_attributes": True}
