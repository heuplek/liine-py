# liine-py

Liine Python API task

TEMP To run locally instructions

1. Install the requirements `pip install -r requirements.txt`
2. Create config.properties postgres properties:
   [DataBaseSection]
   dbname=
   dbuser=
   dbpassword=
3. Run the following command from the project directory
   `uvicorn main:app --reload`
4. GET requests can be made to `(http://127.0.0.1:8000/restaurants/{datetime})`
