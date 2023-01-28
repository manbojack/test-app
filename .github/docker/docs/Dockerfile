FROM  python:rc-alpine AS build_static
WORKDIR /opt/
COPY . .
WORKDIR /opt/docs
RUN pip install -r requirements.txt && mkdocs build

FROM build_static AS docs
WORKDIR /opt/docs
ENTRYPOINT mkdocs serve --dev-addr 0.0.0.0:8000
