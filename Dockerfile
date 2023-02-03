# Pull base image
FROM python:3.10

# Ensures that the output Django writes to the terminal comes out in real time without being buffered somewhere.
# This makes your Docker logs useful and complete.
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

COPY . /code/

# Install dependencies
RUN pip install -r requirements.txt

# expose port 8000
EXPOSE 8000

CMD ["gunicorn", "main:app", "--bind", ":8000", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--reload"]
