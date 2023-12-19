#!/usr/bin/env sh


# Build the nginx container
docker build -t proxycroak-nginx nginx

# Build the proxycroak flask app
docker build -t proxycroak-web .
