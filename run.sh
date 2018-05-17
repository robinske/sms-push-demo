#!/bin/bash

virtualenv env
source env/bin/activate

gunicorn push:app
