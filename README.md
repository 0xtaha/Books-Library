## for Runing locally :
1. run the command `python -m pip install poetry`
2. go to project root dir
3. run the command `poetry config virtualenvs.in-project true`
4. run the command `poetry install`
6. fill the required variables on `.env` and export them to your enviorment
6. start up the database `docker compose up databse cache -d`
5. run the command `flask run`

## for runing on docker
1. add the required env variables to app service on docker compose
2. run the command `docker compose up`
