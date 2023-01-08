#!/bin/bash

nohup uwsgi --enable-threads --ini run.ini > ./log/uwsgi_run.log 2>&1 &