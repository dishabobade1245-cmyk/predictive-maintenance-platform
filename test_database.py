from src.database import get_connection

connection = get_connection()

print("Database connected successfully!")

connection.close()
print("Database connection closed.")