#!/bin/bash

set -e

virtualenv env
source env/bin/activate
make install
