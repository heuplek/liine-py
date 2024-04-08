# liine-py

Liine Python API task

To run locally:

1. Install the requirements `pip install uvicorn fastapi`
2. Run the following command from the /app directory
   `uvicorn main:app --reload`
3. GET requests can be made to `(http://127.0.0.1:8000/restaurants/{datetime})` The datetime should be in the format `YYYY-MM-DDTHH:MM:SS`
4. Access the swagger documentation at `(http://127.0.0.1:8000/docs#/)`

Docker:

1. Build the docker image using the following command
   `docker build -t liine-py .`
2. Run the docker container using the following command
   `docker run -d --name liine-app1 -p 8000:8000 liine-py`
3. GET requests can be made to `(http://127.0.0.1:8000/restaurants/{datetime})` The datetime should be in the format `YYYY-MM-DDTHH:MM:SS`
4. Access the swagger documentation at `(http://127.0.0.1:8000/docs#/)`

Tests:

1. Run the tests using the following command
   `python -m unittest test_restaurant_data.py`
