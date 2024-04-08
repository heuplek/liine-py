# 
FROM python:3.9

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./app /app


ENV PYTHONPATH "${PYTHONPATH}:/app"

# 
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]