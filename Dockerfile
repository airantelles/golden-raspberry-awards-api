# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.15
ARG SQLITE_VERSION=3.53.4
ARG SQLITE_AUTOCONF=3530400
ARG SQLITE_SHA3_256=454e45f61c6bd75b7420e7190732dea03ce6639c63ada47bbc592f67fc340338

FROM python:${PYTHON_VERSION}-slim-bookworm AS python-base


FROM node:24.21.0-bookworm-slim AS node-development


FROM python-base AS sqlite-builder

ARG SQLITE_AUTOCONF
ARG SQLITE_SHA3_256

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        openssl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/sqlite

RUN curl --fail --location --silent --show-error \
        --output sqlite-autoconf.tar.gz \
        "https://www.sqlite.org/2026/sqlite-autoconf-${SQLITE_AUTOCONF}.tar.gz" \
    && test "$(openssl dgst -sha3-256 -r sqlite-autoconf.tar.gz | awk '{print $1}')" = "$SQLITE_SHA3_256" \
    && tar --extract --gzip --file sqlite-autoconf.tar.gz --strip-components=1 \
    && ./configure --prefix=/usr/local --disable-static --enable-shared \
    && make --jobs="$(nproc)" \
    && make install DESTDIR=/sqlite-root \
    && install --directory /sqlite-runtime \
    && cp --dereference --preserve=mode \
        /sqlite-root/usr/local/lib/libsqlite3.so.0 \
        /sqlite-runtime/libsqlite3.so.0


# This target contains the exact Python and SQLite runtime used by both the
# production and development images.
FROM python-base AS base

ARG SQLITE_VERSION

COPY --from=sqlite-builder /sqlite-runtime/libsqlite3.so.0 /usr/local/lib/

RUN ldconfig \
    && python -c "import sqlite3; assert sqlite3.sqlite_version == '${SQLITE_VERSION}'"


FROM base AS development

COPY --from=ghcr.io/astral-sh/uv:0.12.15 /uv /uvx /bin/
COPY --from=node-development /usr/local/bin/node /usr/local/bin/
COPY --from=node-development /usr/local/lib/node_modules /usr/local/lib/node_modules

RUN ln --symbolic ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln --symbolic ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx \
    && uv --version | grep --fixed-strings '0.12.15' \
    && node --version | grep --fixed-strings 'v24.21.0' \
    && npx --version

RUN groupadd --gid 1000 developer \
    && useradd --uid 1000 --gid developer --create-home --shell /bin/bash developer

USER developer


FROM base AS dependencies

COPY --from=ghcr.io/astral-sh/uv:0.12.15 /uv /uvx /bin/

ENV UV_PYTHON_DOWNLOADS=0 \
    UV_NO_SYNC=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv --version | grep --fixed-strings '0.12.15' \
    && uv sync --frozen --no-dev --no-install-project --no-editable --compile-bytecode


FROM base AS runtime

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONPATH=/app/src \
    MOVIELIST_CSV_PATH=/app/docs/Movielist.csv \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system app \
    && useradd --system --gid app --create-home --home-dir /app app

COPY --from=dependencies --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app src/app /app/src/app
COPY --chown=app:app docs/Movielist.csv /app/docs/Movielist.csv

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
