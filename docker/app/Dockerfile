FROM python:3.10.6-alpine3.16 as base
COPY . .
WORKDIR /src

FROM base as builder
RUN apk add --update build-base \
    && mkdir /install \
    && pip install --no-cache -r requirements.txt --prefix=/install \
    && find /install -name '__pycache__' 2>/dev/null | xargs rm -rf

FROM base as runner
EXPOSE 5000
COPY --from=builder /install /usr/local
ENV APP_USER='anonymous' \
    APP_GROUP='anonymous' \
    FLASK_APP='main' \
    PYTHONDONTWRITEBYTECODE=1 \
    POSTGRES_HOST='db' \
    POSTGRES_DB='default_db' \
    POSTGRES_USER='default_user' \
    POSTGRES_PASSWORD='default_password'
RUN addgroup ${APP_GROUP} || true \
    && adduser --system --no-create-home ${APP_USER} --ingroup ${APP_GROUP} \
    && chown ${APP_USER}:${APP_GROUP} -R ${PWD}
USER ${APP_USER}
CMD ["/usr/local/bin/python", "-B", "-m", "flask", "run", "--host=0.0.0.0"]