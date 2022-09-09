#!/bin/sh
cd /home/ubuntu/Hash-Kit/hashkit_services/ && gunicorn -b 0.0.0.0:8000 hashkit_api:application