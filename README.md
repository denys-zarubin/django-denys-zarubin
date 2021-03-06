# Overview Project

Project is API backend with possibility to manage user and teams.

# Deployment

## local
1. Replace .env.TEMPLATE to .env

``` bash
mv .env.TEMPLATE .env
```

2. Run docker-compose up

``` bash
docker-compose up
```

## production
Deployment to production will be done throught docker hub and hook for heroku (required permission access to github).

In the future plans can be done throught Jenkins.

Push image to heroku

```
heroku container:login
```
```
heroku container:push <docker_image_name> --app x1-development
```

# Structure

Docs available with domain

`/docs/`

There you can find discription of all endpoints

# Tests

For tests using `pytests`. To run tests use
```
python -m pytest tests --ds=settings.test  --cov-report=xml --junitxml=/django/pytest.xml
```

