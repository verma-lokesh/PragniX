from pydantic import BaseModel


class PortBase(BaseModel):
    model_config = {"from_attributes": True}
