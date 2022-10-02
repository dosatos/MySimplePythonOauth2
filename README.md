# Install

Install packages

```
make init
```

# To run integration tests

Configure AWS:

```
echo 'SECRET_SALT=02-Oct-2022' >> .env
echo 'AWS_ACCESS_KEY_ID='$(aws configure get aws_access_key_id) >> .env
echo 'AWS_SECRET_ACCESS_KEY='$(aws configure get aws_secret_access_key) >> .env
echo 'AWS_SESSION_TOKEN='$(aws configure get aws_session_token) >> .env
echo 'AWS_DEFAULT_REGION='eu-central-1 >> .env
```

Integration tests:

```
make itests
```

# To generate RSA keys

```
openssl genrsa -out jwt-key 4096
openssl rsa -in jwt-key -pubout > jwt-key.pub
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
