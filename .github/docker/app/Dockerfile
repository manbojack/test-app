FROM golang:alpine AS app
WORKDIR /opt
RUN apk add --no-cache gcc musl-dev \
	&& go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.42.1
COPY . .

FROM app
WORKDIR /opt/app
ENTRYPOINT go run main.go
