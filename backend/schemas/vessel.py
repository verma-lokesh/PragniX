from pydantic import BaseModel


class VesselBase(BaseModel):
    model_config = {"from_attributes": True}
