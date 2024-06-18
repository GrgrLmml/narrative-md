#!/usr/bin/env bash


DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml up -d --build --remove-orphans --wait

