from pydantic import BaseModel


class WeatherBase(BaseModel):
    model_config = {"from_attributes": True}
