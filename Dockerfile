FROM python:3.10.6-alpine3.16 as base

FROM base as builder
RUN mkdir /install
COPY . .
WORKDIR /src
RUN apk add --update build-base \
    && pip install --no-cache -r requirements.txt --prefix=/install && rm -rf __pycache__

FROM base as runner
EXPOSE 8000
COPY --from=builder /install /usr/local
WORKDIR src
COPY src ./
ENV APP_USER='anonymous' \
    APP_GROUP='anonymous' \
    K8S_EMPTY_DIR='/uploads'
RUN mkdir ${K8S_EMPTY_DIR} || true \
    && addgroup ${APP_GROUP} || true \
    && adduser --system --no-create-home ${APP_USER} --ingroup ${APP_GROUP} \
    && chown ${APP_USER}:${APP_GROUP} -R ${K8S_EMPTY_DIR} ${PWD}
USER ${APP_USER}
CMD ["python3", "-B", "main.py"]
