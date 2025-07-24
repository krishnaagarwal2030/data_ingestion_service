FROM golang:1.20-alpine

WORKDIR /data_ingestion_app

RUN apk add --no-cache git

COPY data_ingestion_app/ /data_ingestion_app/
RUN go mod download
RUN go get data_ingestion_service

RUN go build -o main .

EXPOSE 8080

CMD ["./main"]
#CMD ["sleep", "1000"]
