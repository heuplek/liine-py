# liine-py

Liine Python API task

To run locally:

1. Install the requirements `pip install uvicorn fastapi`
2. Run the following command from the project directory
   `uvicorn main:app --reload`
3. GET requests can be made to `(http://127.0.0.1:8000/restaurants/{datetime})`

Docker:

1. Build the docker image using the following command
   `docker build -t liine-py .`
2. Run the docker container using the following command
   `docker run -d --name liine-app1 -p 8000:8000 liine-py`
3. GET requests can be made to `(http://127.0.0.1:8000/restaurants/{datetime})`

Tests:

1. Run the tests using the following command
   `python -m unittest test_restaurant_data.py`
