from pydantic import BaseModel


class CommodityBase(BaseModel):
    model_config = {"from_attributes": True}
