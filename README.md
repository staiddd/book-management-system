# How to start project

### 1. Clone repository
```
git clone https://github.com/staiddd/book-management-system.git
```

### 2. Create `.env` file in the root of the project, for example with the following content
```
POSTGRES_USER=admin
POSTGRES_PASSWORD=1234
POSTGRES_DB=book_management_system
POSTGRES_PORT=65402
POSTGRES_HOST=database

DB_URL=postgresql+asyncpg://admin:1234@database:5432/book_management_system

MODE=DEV
```

### 3. Run docker-compose in the root of the project
```
docker-compose up -d --build
```

### 4. See the documentation made by Swagger in your browser here
```
http://127.0.0.1:8080/docs
```

### All migrations are automatically performed when the container `book_management_system` starts, so you don't need to apply them manually.

<hr>

# How to run tests

### 1. Install test-requirements
```
pip install -r test-requirements.txt
```

### 2. Create `.test.env` file in the root of the project, for example with the following content
```
POSTGRES_USER=admin
POSTGRES_PASSWORD=1234
POSTGRES_DB=book_management_system_test
POSTGRES_PORT=65402
POSTGRES_HOST=database

DB_URL=postgresql+asyncpg://admin:1234@localhost:65402/book_management_system_test

MODE=TEST

REDIS_URL=redis://localhost:6379/0
```
### Data from the `.env` file is replaced with data from the `.test.env` file. This is needed to create a fake database for tests and replace redis_url.

### 3. Run tests
```
pytest -s -v
```