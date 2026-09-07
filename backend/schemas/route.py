from pydantic import BaseModel


class RouteBase(BaseModel):
    model_config = {"from_attributes": True}
