""" Process Multiple Request """
from typing import List, Optional  # noqa: F401
from pydantic import BaseModel, Field
from .process_request_config import ProcessRequestConfig
from .processing_enum import ProcessingEnum


class ProcessMultipleRequest(BaseModel):
    """ ProcessMultipleRequest Model """

    images: List[str] = Field(..., min_items=2, unique_items=True, description="Images to process.")
    processings: Optional[List[ProcessingEnum]] = Field(
        description="Requested biometric processings.",
        default=[ProcessingEnum.detect, ProcessingEnum.analyze, ProcessingEnum.templify],
        unique_items=True,
    )
    configuration: Optional[List[ProcessRequestConfig]] = Field(
        description="Extensible configurations for biometric processing.",
        default=[]
    )
    minimum_score: float = Field(description="Minimum match score.", default=-1, ge=-1)
