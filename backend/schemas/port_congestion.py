from pydantic import BaseModel


class PortCongestionBase(BaseModel):
    model_config = {"from_attributes": True}
