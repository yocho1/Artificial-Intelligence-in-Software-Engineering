"""Refactored version using the SQLAlchemy ORM (AI-generated, reviewed)."""
import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# Load variables from .env
load_dotenv()


# ---------------------------------------------------------
# Database configuration
# ---------------------------------------------------------

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "example_db")

if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD environment variable is required.")


DATABASE_URL = (
    f"mysql+mysqlconnector://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ---------------------------------------------------------
# SQLAlchemy setup
# ---------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------
# User model
# ---------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, "
            f"username={self.username!r}, "
            f"email={self.email!r})"
        )


# ---------------------------------------------------------
# Database initialization
# ---------------------------------------------------------

def create_tables() -> None:
    """Create all tables defined by the ORM models."""
    Base.metadata.create_all(engine)


# ---------------------------------------------------------
# Create user
# ---------------------------------------------------------

def create_user(
    session: Session,
    username: str,
    email: str,
) -> Optional[User]:
    """Create and persist a new user."""

    if not username or not email:
        raise ValueError("Username and email are required.")

    user = User(
        username=username.strip(),
        email=email.strip(),
    )

    try:
        session.add(user)
        session.commit()

        # Refresh the object so generated values such as id are available.
        session.refresh(user)

        return user

    except IntegrityError:
        session.rollback()
        print(f"Username '{username}' already exists.")
        return None

    except SQLAlchemyError as exc:
        session.rollback()
        print(f"Database error creating user: {exc}")
        return None


# ---------------------------------------------------------
# Get user by username
# ---------------------------------------------------------

def get_user_by_username(
    session: Session,
    username: str,
) -> Optional[User]:
    """Return a user by username, or None if not found."""

    try:
        statement = select(User).where(User.username == username)

        return session.scalar(statement)

    except SQLAlchemyError as exc:
        session.rollback()
        print(f"Database error retrieving user: {exc}")
        return None


# ---------------------------------------------------------
# Update user email
# ---------------------------------------------------------

def update_user_email(
    session: Session,
    username: str,
    new_email: str,
) -> Optional[User]:
    """Update the email address of a user."""

    if not new_email:
        raise ValueError("New email is required.")

    try:
        user = session.scalar(
            select(User).where(User.username == username)
        )

        if user is None:
            print(f"User '{username}' not found.")
            return None

        user.email = new_email.strip()

        session.commit()
        session.refresh(user)

        return user

    except SQLAlchemyError as exc:
        session.rollback()
        print(f"Database error updating user: {exc}")
        return None


# ---------------------------------------------------------
# Delete user
# ---------------------------------------------------------

def delete_user(
    session: Session,
    username: str,
) -> bool:
    """Delete a user by username."""

    try:
        user = session.scalar(
            select(User).where(User.username == username)
        )

        if user is None:
            print(f"User '{username}' not found.")
            return False

        session.delete(user)
        session.commit()

        return True

    except SQLAlchemyError as exc:
        session.rollback()
        print(f"Database error deleting user: {exc}")
        return False


# ---------------------------------------------------------
# List users
# ---------------------------------------------------------

def list_users(session: Session) -> list[User]:
    """Return all users ordered by ID."""

    try:
        statement = select(User).order_by(User.id)

        return list(session.scalars(statement).all())

    except SQLAlchemyError as exc:
        session.rollback()
        print(f"Database error listing users: {exc}")
        return []


# ---------------------------------------------------------
# Example application
# ---------------------------------------------------------

def main() -> None:
    # Create the users table if it doesn't exist.
    create_tables()

    # Session is responsible for transactions.
    with Session(engine) as session:

        # Create
        user = create_user(
            session,
            username="achraf",
            email="achraf@example.com",
        )

        if user:
            print("Created:", user)

        # Read
        user = get_user_by_username(
            session,
            "achraf",
        )

        if user:
            print("Found:", user)

        # Update
        updated_user = update_user_email(
            session,
            "achraf",
            "new-email@example.com",
        )

        if updated_user:
            print("Updated:", updated_user)

        # List
        users = list_users(session)

        print("\nAll users:")
        for user in users:
            print(user)

        # Delete
        deleted = delete_user(
            session,
            "achraf",
        )

        print("\nDeleted:", deleted)


if __name__ == "__main__":
    main()
