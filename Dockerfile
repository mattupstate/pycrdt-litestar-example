FROM node:16.15.0-slim as static-build
WORKDIR /usr/src
COPY package* .
RUN npm install
COPY static ./static
COPY webpack.config.js .
RUN npx webpack --mode=production


FROM python:3.12-slim as python-build
WORKDIR /usr/src
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential
ADD pyproject.toml poetry.lock /usr/src/
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi --no-dev && rm pyproject.toml poetry.lock


FROM python:3.12-slim
WORKDIR /app
COPY --from=python-build /usr/src /app
COPY --from=static-build /usr/src/example_app/static/bundles /app/example_app/static/bundles
ADD ./example_app /app/example_app
RUN addgroup --gid 1000 app
RUN adduser app -h /app -u 1000 -G app -DH
USER 1000
EXPOSE 8000
ENTRYPOINT [".venv/bin/python", "-m", "example_app"]
