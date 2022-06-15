# FastAPI Users

## Technologies

### Basic

- Python
- FastAPI
- HTTP Basic Auth
- PostgreSQL
- Redis
- Prometheus

### Code Style
- black
- isort
- flake8
- pylint

### Tests
- pytest

## Installation

- Clone the GitHub repository
```bash
// http:
git clone https://github.com/nikitunkun/FastAPIUsers.git
// ssh:
git clone git@github.com:nikitunkun/FastAPIUsers.git
```
- Navigate to the project folder
```bash
cd FastAPIUsers
```

## Usage

- Configure .env.dist

| Environment variable | Value                                      |
|:--------------------:|--------------------------------------------|
| POSTGRES_HOST        | PostgreSQL Host                            |
| POSTGRES_PORT        | PostgreSQL Port                            |
| POSTGRES_USER        | PostgreSQL Username                        |
| POSTGRES_PASSWORD    | PostgreSQL Password                        |
| POSTGRES_DB          | PostgreSQL Database Name                   |
| REDIS_HOST           | PostgreSQL Password                        |
| REDIS_PORT           | PostgreSQL Database Name                   |

- Copy .env.dist to .env
```bash
cp .env.dist .env
```
- Run
```bash
docker-compose up --build
```

## Linters and Formatter

```bash
make format
make lint
```

## Tests

- Run docker-compose
```bash
docker-compose up -d
```
- Run tests
```bash
docker-compose run api make test
```

## Endpoints

- **/docs**
Swagger Scheme

- **/redoc**
Swagger Scheme

- **/metrics**
Prometheus Metrics

- **/dummy** *[ GET ]*
Health-Check

- **/user/create** *[ POST ]*
Create User

- **/user/find** *[ GET ]*
Find Users by username

- **/user/** *[ GET ]*
Get user by ID or get authorized User info

- **/user/** *[ PUT ]*
Update User info

- **/user/** *[ DELETE ]*
Delete User

## Enjoy 🙃