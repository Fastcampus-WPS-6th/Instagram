#!/usr/bin/env bash
docker build -t base -f Dockerfile.base .
docker tag base azelf/base
docker push azelf/base