## Setup up Job board

### Virtual env:
- Create: `python3 -m venv /path-to-new-virtual-environment`
- Activate: `source /path-to-new-virtual-environment/bin/activate`
- Deactivate: `deactivate`

### Libraries
- Install libraries from requirements.txt file: `pip install -r requirements.txt`

### Run containers:
`docker-compose up -d`

## Manage DB

### Ensure the table created:
1. Access PostgreSQL DB: `dco exec db psql --username=user_one --dbname=job_board`
2. List of relations: `# \dt`

### Select data from DB table:
1. `dco exec db psql --username=user_one --dbname=job_board`
2. `select * from table;`

## REST API

### API docs
- http://127.0.0.1:8000/docs

## Tests

### Run tests
- From root directory execute: `pytest`

### TO DO:
1. ?
