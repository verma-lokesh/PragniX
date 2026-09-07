from pydantic import BaseModel


class BunkerPriceBase(BaseModel):
    model_config = {"from_attributes": True}
