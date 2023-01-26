FROM python:3.10.6-alpine3.16 as base
COPY . .
WORKDIR /src

FROM base as builder
RUN apk add --update build-base \
    && mkdir /install \
    && pip install --no-cache -r requirements.txt --prefix=/install && rm -rf __pycache__

FROM base as runner
EXPOSE 8000
COPY --from=builder /install /usr/local
ENV APP_USER='anonymous' \
    APP_GROUP='anonymous' \
    K8S_EMPTY_DIR='/uploads'
RUN mkdir ${K8S_EMPTY_DIR} || true \
    && addgroup ${APP_GROUP} || true \
    && adduser --system --no-create-home ${APP_USER} --ingroup ${APP_GROUP} \
    && chown ${APP_USER}:${APP_GROUP} -R ${K8S_EMPTY_DIR} ${PWD}
USER ${APP_USER}
CMD ["python3", "-B", "main.py"]
