import re
from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from random import choice

from RevisorVision_test_task.database import get_session
from RevisorVision_test_task.models.plate_operations import Plate
from RevisorVision_test_task.tables import Plates


class OperationService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.numbers = [str(x) for x in range(10)]
        self.letters = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']

    def generate_plate(self, count: int = 1) -> str | list:
        list_of_plates = []
        for _ in range(count):
            list_of_plates.append(
                ''.join
                    (
                    [choice(self.letters), ] +
                    [choice(self.numbers) for _ in range(3)] +
                    [choice(self.letters) for _ in range(2)] +
                    [choice(self.numbers) for _ in range(choice([2, 3]))]
                )
            )
        return list_of_plates

    def get_plate(self, uuid: str = None) -> Plate:
        if uuid:
            plate = (
                self.session.query(Plates).
                filter_by(plate_uuid=uuid).
                first()
            )
            if not plate:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Ошибка, данного номера нет в базе данных',
                )
            return plate
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Ошибка, введите ID номера',
            )

    def add_plate(self, plate=None) -> Plates:
        plate = str(plate)
        if plate and re.findall(
                r'''^(([АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{1,2})(\d{2,3})|
                (\d{4}(?<!0000)[АВЕКМНОРСТУХ]{2})(\d{2})|(\d{3}(?<!000)(C?D|
                [ТНМВКЕ])\d{3}(?<!000))(\d{2}(?<!00))|([ТСК][АВЕКМНОРСТУХ]{2}\d{3}(?<!000))(\d{2})|
                ([АВЕКМНОРСТУХ]{2}\d{3}(?<!000)[АВЕКМНОРСТУХ])(\d{2})|([АВЕКМНОРСТУХ]\d{4}(?<!0000))(\d{2})|
                (\d{3}(?<!000)[АВЕКМНОРСТУХ])(\d{2})|(\d{4}(?<!0000)[АВЕКМНОРСТУХ])(\d{2})|([АВЕКМНОРСТУХ]{2}\d{4}(?<!0000))(\d{2})|
                ([АВЕКМНОРСТУХ]{2}\d{3}(?<!000))(\d{2,3})|(^Т[АВЕКМНОРСТУХ]{2}\d{3}(?<!000)\d{2,3}))''',
                plate
        ):  # страшно, но это работает
            operation = Plates(plate=plate, created_at=datetime.utcnow())
            self.session.add(operation)
            self.session.commit()
            return operation
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Ошибка, некорректные данные',
            )
