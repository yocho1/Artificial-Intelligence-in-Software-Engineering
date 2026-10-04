"""Initial procedural script using raw SQL (mysql.connector)."""
import mysql.connector
from mysql.connector import Error


def get_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="example_db"
    )


def create_user(db_cursor, username, email):
    """Create a new user safely using parameterized queries."""
    if not username or not email:
        print("Username and email are required.")
        return
    sql = "INSERT INTO users (username, email) VALUES (%s, %s)"
    try:
        db_cursor.execute(sql, (username, email))
        print(f"User '{username}' created successfully.")
    except Error as e:
        print(f"Error creating user: {e}")


def get_user_by_username(db_cursor, username):
    """Return one user row (or None) matching the username."""
    sql = "SELECT id, username, email FROM users WHERE username = %s"
    try:
        db_cursor.execute(sql, (username,))
        return db_cursor.fetchone()
    except Error as e:
        print(f"Error fetching user: {e}")
        return None


def update_user_email(db_cursor, username, new_email):
    """Update the email of an existing user."""
    sql = "UPDATE users SET email = %s WHERE username = %s"
    try:
        db_cursor.execute(sql, (new_email, username))
        print(f"{db_cursor.rowcount} row(s) updated.")
    except Error as e:
        print(f"Error updating user: {e}")


def delete_user(db_cursor, username):
    """Delete a user by username."""
    sql = "DELETE FROM users WHERE username = %s"
    try:
        db_cursor.execute(sql, (username,))
        print(f"{db_cursor.rowcount} row(s) deleted.")
    except Error as e:
        print(f"Error deleting user: {e}")


def list_users(db_cursor):
    """Return all users as a list of rows."""
    try:
        db_cursor.execute("SELECT id, username, email FROM users")
        return db_cursor.fetchall()
    except Error as e:
        print(f"Error listing users: {e}")
        return []
