# Install

Install packages
```
poetry install
```

Configure AWS:
```
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
export AWS_SESSION_TOKEN=$(aws configure get aws_session_token)
```

# To format

```
make format
```

# To build package

```
make build
```

## To run linters only

```
make lint
```

## To run linters only

```
make tests
```
