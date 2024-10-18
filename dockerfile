FROM python:3.12 AS base

ARG build_env=prod
ARG http_proxy
ARG https_proxy
ARG no_proxy
ARG app_user=api

ENV TZ=Africa/Cairo \
    LANG=C.UTF-8 \
    APP_LOG_DIR=/var/log/app \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    MODE=production

RUN apt-get update  \
    && apt-get install -y tzdata supervisor jq \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime  \
    && echo $TZ > /etc/timezone  \
    && adduser --system --group --uid 1000 "${app_user}"  \
    && mkdir -p ${APP_LOG_DIR}  \
    && chown -R ${app_user}:${app_user} ${APP_LOG_DIR}


RUN apt-get update  \
    && apt-get install --no-install-recommends -y  \
      uwsgi \
      uwsgi-plugin-python3 \
      libadns1-dev  \
      libpq-dev  \
      build-essential \
      python3-dev \
    && pip install poetry pyuwsgi


WORKDIR /app
COPY --chown=${app_user}:${app_user} docker-entrypoint.sh /
COPY --chown=${app_user}:${app_user} ["wsgi.py", "./"]
COPY --chown=${app_user}:${app_user} ["pyproject.toml", "poetry.lock", "./" ]
COPY --chown=${app_user}:${app_user} ["src", "./src"]
COPY --chown=${app_user}:${app_user} ["supervisor/", "/etc/supervisor/conf.d/"]

RUN chown -R ${app_user}:${app_user} . \
    && poetry config virtualenvs.create false  \
    && if [ "${build_env}" != "dev" ]; then  \
      poetry install --no-interaction --no-ansi || exit 1; \
      rm -rf poetry.lock pyproject.toml ; \
      apt-get purge --auto-remove  \
        && apt-get clean  \
        && rm -rf /var/lib/apt/lists/*; \
    else \
      poetry install --no-interaction --no-ansi || exit 1; \
    fi;
  
USER ${app_user}

ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]
