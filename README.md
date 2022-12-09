## Setup up Job board

### Create environment file
- Copy `.env.example` to `.env`
- Update the environment variables

### Run containers:

`docker-compose up -d`. It will create API, DB, and DB admin containers

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

## Deployment

### Deployment to GCP
- Create GCP account
- Install gcloud CLI: https://cloud.google.com/sdk/docs/install
- `gcloud init`
- Check project ID: `gcloud config get-value project`
- Build container image using Cloud Build: `gcloud builds submit --tag gcr.io/PROJECT-ID/api`
- Deploy container image to Cloud Run using env variables: 
`gcloud run deploy --image gcr.io/PROJECT-ID/api --platform managed --update-env-vars POSTGRES_USER=quickstart-user,POSTGRES_PASSWORD=quickstart-password,POSTGRES_SERVER=34.69.206.97,POSTGRES_PORT=5432,POSTGRES_DB=job_board,POSTGRES_DB_DRIVER=postgresql+pg8000`
- Check deployment: `gcloud run services list`

### TO DO
- 