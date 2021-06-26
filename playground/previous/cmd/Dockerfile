# FROM golang:1.12.3 as builder

# WORKDIR /go/src/backend_demo
# ADD ./backend_demo.go /go/src/backend_demo/
# ADD ./go.mod /go/src/backend_demo/
# RUN go build

FROM ubuntu:18.04

ADD ./backend /root
WORKDIR /root

CMD [ "/root/backend" ]
