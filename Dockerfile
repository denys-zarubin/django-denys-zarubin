FROM python:alpine as python-base
MAINTAINER Denys Zarubin
LABEL test_image=true

WORKDIR /django
COPY requirements requirements

# Cache this
RUN apk add -U postgresql-dev build-base linux-headers && \
    pip install -r /django/requirements/common.txt && \
    pip install -r /django/requirements/test.txt

# Run tests for new code
COPY . /django
RUN python -m pytest tests --ds=settings.test  --cov-report=xml --junitxml=/django/pytest.xml  && \
    prospector --path=. --profile=/django/prospector.yml

FROM python:alpine
WORKDIR /django

COPY --from=python-base /root/.cache /root/.cache
COPY --from=python-base /django/requirements requirements

# Cache this
RUN apk add -U postgresql-dev build-base linux-headers && \
    pip install -r /django/requirements/common.txt && \
    rm -rf /root/.cache && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Run copy code
COPY --from=python-base /django/ .

EXPOSE 8000

ENTRYPOINT ["/django/entrypoint.sh"]
CMD ["prod"]