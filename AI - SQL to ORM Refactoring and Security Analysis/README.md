# AI: SQL to ORM Refactoring and Security Analysis

## Objective
Use an AI assistant to refactor a procedural MySQL script written with raw
SQL (`mysql.connector`) into a SQLAlchemy ORM version, then analyse the
security and maintainability benefits.

## Files
| File | Description |
|------|-------------|
| `initial_script.py` | Original procedural script (raw SQL, parameterized queries) |
| `refactored_orm.py` | SQLAlchemy ORM version (declarative `User` model + Session CRUD) |
| `PROMPT.txt` | The exact prompt given to the AI assistant |
| `screenshots/` | Screenshots (s1-s8) of the AI's complete code response; add the explanation screenshot too |

## How to run the refactored version
```bash
pip install sqlalchemy mysql-connector-python python-dotenv
```
Create a `.env` file next to the script (never commit it):
```
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
DB_NAME=example_db
```
Then run `python3 refactored_orm.py`. The demo creates the table, adds a
user, reads it, updates the email, lists all users and deletes the user.

## What changed
- `users` table is described once by the `User` class (SQLAlchemy 2.0
  `DeclarativeBase` and `Mapped` columns) instead of SQL strings.
- Rows are Python objects (`user.email`) instead of tuples (`row[2]`).
- SQLAlchemy binds every value as a parameter, so user input is never
  concatenated into SQL.
- Credentials come from environment variables loaded from `.env`.
- Duplicate usernames are caught as `IntegrityError` (unique constraint).
- Failed operations call `session.rollback()` to keep the session usable.

## Security and professional benefits (summary)
1. **SQL injection protection:** values are always bound parameters.
2. **Less boilerplate:** no hand-written INSERT/UPDATE/DELETE strings.
3. **Maintainability:** renaming a column is one change in the model.
4. **Portability:** the same code runs on MySQL, PostgreSQL or SQLite.
5. **Testability:** swap the database URL for in-memory SQLite in tests.
6. **Transactions:** the Session commits or rolls back as a unit.

## Reflection
See the Google Doc submission for the full reflection.
