from typing import Optional

from sqlmodel import Field, SQLModel, Session, create_engine, select

import decimal
from decimal import Decimal

class Car(SQLModel, table=True):
  #id: Optional[int] = Field(default=None, primary_key=True)
  vehicleId: str = Field(default=None, primary_key=True)
  latitude: Decimal
  longitude: Decimal
  place: str

car_1 = Car(vehicleId = 'mXfkjrFw', latitude = '51.5090562', longitude = '-0.1304571', place = '??? (A surprise)')
car_2 = Car(vehicleId = 'nZXB8ZHz', latitude = '51.5080898', longitude = '-0.07620836346036469', place = '	Tower of London')

print(car_1)
print(car_2)

engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
  session.add(car_1)
  session.add(car_2)
  session.commit()

with Session(engine) as sess:
  statement = select(Car).where(Car.vehicleId == 'mXfkjrFw')
  result = sess.exec(statement).first()
  print(result)

