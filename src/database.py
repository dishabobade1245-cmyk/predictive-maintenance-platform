import os

# Use Render's DATABASE_URL in production.
# Use individual variables for local development.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Render may provide the URL with the postgres:// scheme.
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg2://",
            1
        )
else:
    DATABASE_URL = (
        f"postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_USER', 'postgres')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB', 'predictive_maintenance')}"
    )


from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)


def get_connection():
    return engine.raw_connection()