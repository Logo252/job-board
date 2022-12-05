# Pull base image
FROM python:3.10

WORKDIR /code/

COPY . /code/

# Install dependencies
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "main.py"]