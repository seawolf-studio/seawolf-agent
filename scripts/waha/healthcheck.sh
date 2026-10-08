#!/bin/bash
# Vigilante de salud — disparado por cron cada 30 min. No reinicia nada: solo vigila y avisa.
set -a
. /opt/waha/filtro.env
set +a
/usr/bin/python3 /opt/waha/healthcheck.py
