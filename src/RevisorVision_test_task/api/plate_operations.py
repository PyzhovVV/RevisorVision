from typing import List

from fastapi import APIRouter, Depends

from RevisorVision_test_task.models.auth import User
from RevisorVision_test_task.models.plate_operations import CreatedPlate, Plate
from RevisorVision_test_task.services.auth import get_current_user
from RevisorVision_test_task.services.plate_operations import OperationService

router = APIRouter(
    prefix='/plates'
)


@router.get('/{count}')
def generate_plate(
        count: int,
        service: OperationService = Depends(),
        # user: User = Depends(get_current_user)
):
    return service.generate_plate(count=count)


@router.get('/find/{plate_uuid}', response_model=CreatedPlate)
def get_plate(
        plate_uuid,
        service: OperationService = Depends(),
        # user: User = Depends(get_current_user)
):
    return service.get_plate(uuid=plate_uuid)


@router.post('/{plate}', response_model=CreatedPlate)
def add_plate(
        plate,
        service: OperationService = Depends(),
        # user: User = Depends(get_current_user)
):
    return service.add_plate(plate=plate)
