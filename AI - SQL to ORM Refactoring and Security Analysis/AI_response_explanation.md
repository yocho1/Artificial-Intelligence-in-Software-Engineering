## .env and dependencies

Keep credentials outside the Python source:

```
DB_USER=root
DB_PASSWORD=your_real_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=example_db
```

Also add .env to .gitignore:

```
.env
__pycache__/
*.pyc
```

Install dependencies:

```
pip install sqlalchemy mysql-connector-python python-dotenv
```

## 2. Step-by-step usage

### Step 1 - Create the MySQL database

The database itself can be created in MySQL:

```
CREATE DATABASE example_db;
```

SQLAlchemy then handles the users table:

```
Base.metadata.create_all(engine)
```

The resulting table is conceptually:

```
users
--------------------------------
id          INT PRIMARY KEY
username    VARCHAR(100) NOT NULL UNIQUE
email       VARCHAR(255) NOT NULL
```

The ORM model is the source of truth for the Python application's table definition.

### Step 2 - Configure the connection

Instead of hard-coding password="yourpassword", the application reads DB_PASSWORD = os.getenv("DB_PASSWORD") and constructs the SQLAlchemy connection URL. This prevents credentials from being embedded directly in source code. For production, you would normally provide these environment variables through your deployment platform's secret/environment-variable system rather than committing a .env file.

### Step 3 - Create a user

```
with Session(engine) as session:
    user = create_user(
        session,
        "john",
        "john@example.com",
    )

    print(user)
```

SQLAlchemy handles the actual INSERT. You don't manually write INSERT INTO users (...) VALUES (...). The Python object represents the database row:

```
user = User(
    username="john",
    email="john@example.com",
)
```

### Step 4 - Query the user

```
with Session(engine) as session:
    user = get_user_by_username(
        session,
        "john",
    )

    if user:
        print(user.username)
        print(user.email)
```

The important ORM expression is select(User).where(User.username == username). SQLAlchemy converts that expression into the appropriate SQL and binds username as a parameter.

### Step 5 - Update

```
with Session(engine) as session:
    user = update_user_email(
        session,
        "john",
        "john.new@example.com",
    )

    print(user)
```

Rather than manually constructing an UPDATE statement, you modify the mapped Python object (user.email = new_email) and commit (session.commit()). SQLAlchemy detects the change and generates the appropriate UPDATE.

### Step 6 - Delete

```
with Session(engine) as session:
    success = delete_user(
        session,
        "john",
    )

    print(success)
```

The ORM operation is simply session.delete(user) followed by session.commit().

### Step 7 - List users

```
with Session(engine) as session:
    users = list_users(session)

    for user in users:
        print(user.id, user.username, user.email)
```

The query select(User).order_by(User.id) returns ORM User objects rather than raw database tuples.

## 3. Security and professional benefits

### A. SQL injection protection

The biggest security improvement is that SQLAlchemy separates SQL structure from user-provided values. A vulnerable implementation might do this:

```
username = input("Username: ")

query = f"""
    SELECT * FROM users
    WHERE username = '{username}'
"""

cursor.execute(query)
```

An attacker could provide ' OR '1'='1, producing something equivalent to:

```
SELECT * FROM users
WHERE username = '' OR '1'='1'
```

The condition is always true, potentially exposing every user. With SQLAlchemy:

```
statement = select(User).where(
    User.username == username
)

user = session.scalar(statement)
```

username is treated as data, not executable SQL. Conceptually, SQLAlchemy sends something similar to SELECT ... FROM users WHERE username = ? with the actual username supplied separately as a bound parameter. That is the important security boundary.

### B. Parameter binding

The original code already had one good security practice:

```
sql = """
    INSERT INTO users (username, email)
    VALUES (%s, %s)
"""

cursor.execute(sql, (username, email))
```

That is parameterized SQL. So it would be incorrect to say that the original INSERT is automatically vulnerable to SQL injection. mysql.connector parameter binding protects the values in that query. The advantage of SQLAlchemy is that parameter binding becomes the normal behavior of the ORM, through User(username=username, email=email) and select(User).where(User.username == username). You don't have to manually construct SQL strings for ordinary CRUD operations.

Important: SQLAlchemy does not magically make every possible query safe. Raw SQL can still be dangerous if you concatenate untrusted input into it. The safe pattern remains parameter binding.

### C. Better maintainability

Imagine your application eventually has User, Order, Product, Invoice, Payment, Customer, Address and Subscription. With raw SQL, you may end up maintaining INSERT, SELECT, UPDATE, DELETE, JOIN and WHERE strings throughout your application. With SQLAlchemy, your database structure is represented by Python models (class User(Base), class Product(Base), class Order(Base)). Relationships, constraints, indexes, queries and business logic can be expressed using a consistent Python API. That becomes significantly easier to maintain as the application grows.

### D. Readability

Compare the raw version:

```
sql = """
    SELECT id, username, email
    FROM users
    WHERE username = %s
"""

cursor.execute(sql, (username,))
row = cursor.fetchone()
```

with the ORM version:

```
statement = select(User).where(
    User.username == username
)

user = session.scalar(statement)
```

The second version describes the operation in terms of the application's domain: select a User whose username equals this value. That is especially useful when working on larger backend systems.

### E. ORM objects represent database entities

With raw SQL, you commonly receive tuples or dictionaries (row[0], row[1], row[2]). With SQLAlchemy you use user.id, user.username and user.email. This gives the application a proper domain representation. It also makes code completion, type checking and IDE navigation much better.

### F. Transactions and rollback

A particularly important improvement is explicit transaction management:

```
try:
    session.add(user)
    session.commit()

except SQLAlchemyError:
    session.rollback()
```

If the transaction fails, the session must be rolled back before it can safely continue. That is why the CRUD functions use session.rollback() in their except blocks. The unique constraint unique=True on username means attempting to create "john" twice results in a database integrity error. We catch it with except IntegrityError and roll back, rather than leaving the transaction in a failed state.

### G. Database portability

The original application is tightly coupled to mysql.connector and the MySQL-specific %s parameter syntax. SQLAlchemy provides an abstraction over the database layer. The same model can generally work with MySQL, PostgreSQL, SQLite, SQL Server and Oracle by changing the engine and driver configuration. For example, mysql+mysqlconnector://... could become postgresql+psycopg://... while the ORM model and much of the application code remain unchanged. There can still be database-specific differences, but SQLAlchemy dramatically reduces the amount of application code tied directly to one database engine.

### H. Less boilerplate

With the original approach, CRUD operations require you to manually manage the connection, cursor, SQL string, parameters, execute(), fetchone(), fetchall(), commit(), rollback() and close(). The ORM gives you higher-level operations: session.add(user), session.commit(), session.scalar(statement) and session.delete(user). This is not just about having fewer lines of code. It gives the application a consistent transaction and data-access model.

### I. Constraints belong at the database level

The model defines a primary key on id, a unique, non-null username (String(100)) and a non-null email (String(255)). This is important because application validation alone is not enough. For example, checking if username: does not prevent two concurrent requests from creating the same username. The database's unique=True constraint provides the actual integrity guarantee.

### One production improvement

For a real application, I would go one step further and use Alembic for database migrations rather than relying on Base.metadata.create_all(engine). create_all() is excellent for a small project, prototype, or initial setup. In production, migrations give you controlled changes such as adding users, adding email_verified, adding created_at, adding indexes and changing constraints, without destroying or recreating existing production data.
