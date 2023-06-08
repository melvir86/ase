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
car_2 = Car(vehicleId = 'nZXB8ZHz', latitude = '51.5080898', longitude = '-0.07620836346036469', place = 'Tower of London')
car_3 = Car(vehicleId = 'Tkwu74WC', latitude = '51.5425649', longitude = '-0.00693080308689057', place = 'Westfield Stratford City')
car_4 = Car(vehicleId = '5KWpnAJN', latitude = '51.519821199999996', longitude = '-0.09397523701275332', place = 'The Barbican Centre')
car_5 = Car(vehicleId = 'uf5ZrXYw', latitude = '51.5133798', longitude = '-0.0889552', place = 'The Bank of England')
car_6 = Car(vehicleId = 'VMerzMH8', latitude = '51.5253378', longitude = '-0.033435', place = 'Mile End Station')
car_7 = Car(vehicleId = '8efT67Xd', latitude = '51.54458615', longitude = '-0.0161905117168855', place = 'Queen Elizabeth Olympic Park')

print(car_1)
print(car_2)

engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
  session.add(car_1)
  session.add(car_2)
  session.add(car_3)
  session.add(car_4)
  session.add(car_5)
  session.add(car_6)
  session.add(car_7)
  session.commit()
  session.close()

with Session(engine) as sess:
  statement = select(Car).where(Car.vehicleId == 'mXfkjrFw')
  result = sess.exec(statement).first()
  print(result)
  sess.close()

