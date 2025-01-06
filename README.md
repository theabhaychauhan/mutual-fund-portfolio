## Directions to Use Locally

1. **Edit `.env` File**  
   Update the `.env` file with your database credentials and other required environment variables. Example:  
   ```env
   DATABASE_URL=postgresql+psycopg2://username:password@localhost/dbname
   RAPIDAPI_KEY=your-rapidapi-key
   RAPIDAPI_HOST=your-rapidapi-host
   
2. Update alembic.ini Configuration
In the alembic.ini file, navigate to line 65 and edit the PostgreSQL credentials as per your setup.
Example:
sqlalchemy.url = postgresql+psycopg2://username:password@localhost/dbname

3. Create the Database (if necessary)
If the database does not already exist, you can either:

Change the DATABASE_URL in .env to point to an existing database.
Or, run the create_db script to set up the database:
python create_db.py

4. Run Database Migrations
Apply the Alembic migrations to set up the database schema:
alembic upgrade head

5. Start the Application
Start the FastAPI application on your local development server:
uvicorn main:app --reload
