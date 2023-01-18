from pydantic import BaseModel


class Plate(BaseModel):
    plate: str


class CreatedPlate(Plate):
    plate_uuid: str

    class Config:
        orm_mode = True
