#!/usr/bin/env bash

host=default
cp *.sh stage
vagrant scp stage $host:
vagrant ssh $host --command 'mv stage/* ~'
vagrant ssh $host --command 'mv stage stage.$(date +%s)'
