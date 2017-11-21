#!/usr/bin/env bash
docker build -t base -f Dockerfile.base .
docker build -t instagram .
docker run --rm -it -p 8013:80 instagram