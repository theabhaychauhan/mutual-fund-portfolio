Directions to use on Local - 
Edit the .env file as per your credentials
In alembic.ini:65 edit your Postgres creds.
Either Change the DB in .env file or run the script using py create_db
alembic upgrade head
uvicorn main:app --reload
