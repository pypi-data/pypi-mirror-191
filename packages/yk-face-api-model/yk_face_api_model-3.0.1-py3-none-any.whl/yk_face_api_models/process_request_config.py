""" Process Request Configuration """
from pydantic import BaseModel, Field


class ProcessRequestConfig(BaseModel):
    """ ProcessRequestConfig Model """
    name: str = Field(description="Configuration name")
    value: str = Field(description="Configuration value")
