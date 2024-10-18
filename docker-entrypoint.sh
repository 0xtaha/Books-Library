#!/bin/sh
set -e
set -u

if [ -n "${MODE}" ] && [ "${MODE}" = "production" ]; then
  supervisord -n -c /etc/supervisor/conf.d/default.conf
else
  FLASK_RUN_HOST=0.0.0.0 flask run
fi
