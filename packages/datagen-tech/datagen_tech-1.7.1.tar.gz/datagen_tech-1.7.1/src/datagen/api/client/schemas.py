import enum

from pydantic import BaseModel, Field


class DataResponse(BaseModel):
    generation_name: str = Field(
        description="Generation name provided by Datagen platform. In a format " "of 'Field - <date>."
    )
    generation_id: str = Field(
        description="Unique UUID provided by Datagen platform. With the generation id you'll "
        "be able to query generation_status, stop generation and get download urls"
    )
    dgu_hour: float = Field(description="The DGU Hour cost of the requested generation.")
    renders: int = Field(description="The number of datapoints received in this request.")
    scenes: int = Field(description="The number of scenes received in this request.")


class EGenerationStatus(enum.Enum):
    START = "START"
    IN_PROGRESS = "IN-PROGRESS"
    PENDING = "IN-PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DataResponseStatus(BaseModel):
    estimation_time_ms: int = Field(description="Estimated time in ms to data generation completion.", ge=0)
    status: EGenerationStatus = Field(description="Current status of the generation process.")
    percentage: int = Field(description="The percentage of data generation completion.", ge=0, le=100)
