## Setup up Job board

### Virtual env:

- Create: `python3 -m venv /path-to-new-virtual-environment`
- Activate: `source /path-to-new-virtual-environment/bin/activate`
- Deactivate: `deactivate`

### Libraries

- Install libraries from requirements.txt file: `pip install -r requirements.txt`

### Run containers:

`docker-compose up -d`

### Run server:

- From root directory execute this command: `uvicorn main:app --reload`. Alternative way: `python3 main.py`

## REST API

### API docs

- http://127.0.0.1:8000/docs

## Job chat using websocket. 

### Job chat endpoint. 
Accessing this endpoint in browser you will create new websocket connection and be able to send messages 
which will be broadcasted to all participants.

- http://127.0.0.1:8000/job-chat

## Manage DB

### Ensure the table created:

1. Access PostgreSQL DB: `dco exec db psql --username=user_one --dbname=job_board`
2. List of relations: `# \dt`

### Select data from DB table:

1. `dco exec db psql --username=user_one --dbname=job_board`
2. `select * from table;`

### Access PhAdmin to manage DB through web-based GUI
1. Access `http://localhost:8080/`
2. Fill username and password (from docker-compose.yml)
      PGADMIN_DEFAULT_EMAIL
      PGADMIN_DEFAULT_PASSWORD
3. Create new server:
- Add your server name
- Host name/address: `postgres_container`
- Port: `5432`
- Username: `user_one`
- Password: `user_one`

## Tests

### Run tests

- From root directory execute: `pytest`

### TO DO
- Update websocket functionality to be able to send personal messages to specific user by 
specifying message (which won't be seen by others) and participant ID.
- It will be needed to update job_chat.html:
New form can be created for this in HTML and function in JS accordingly to handle passed message and participant ID.
- It will be needed to update route_websocket.py, connection_manager.py files to handle new personal messages
