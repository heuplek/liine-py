import datetime
from fastapi import FastAPI
import models
from data.dataParse import parseData
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

models.Base.metadata.create_all(bind=engine)
session = Session(engine)
session.query(models.Hours).delete()
session.commit()
data = parseData()
#print(data)
try:
    session.execute(models.Hours.__table__.insert(), data)
    session.commit()
except Exception as e:
    print("didn't work", e)
    session.rollback()
finally:
    session.close()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the restaurant API!"}


@app.get("/restaurants/{date}")
async def find_restaurants(date: datetime.datetime = None):
    time = date.time()
    session = Session(engine)
    queryStr = f"Select hours.id, hours.restaurant from hours where day = extract(dow from date '{date}') and '{time}' > hours.open_hour and '{time}' < hours.close_hour;"

    open_restaurants = session.query(models.Hours).from_statement(text(queryStr)).all()
    session.close()
    response = []
    for restaurant in open_restaurants:
        response.append(restaurant.restaurant)
    return {"open_restaurants": response}