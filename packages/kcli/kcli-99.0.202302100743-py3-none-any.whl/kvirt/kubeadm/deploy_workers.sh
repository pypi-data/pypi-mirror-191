#!/usr/bin/env bash

export PATH=/root:$PATH
test -f /etc/profile.d/kcli.sh && source /etc/profile.d/kcli.sh
pre.sh
{% if eksd %}
eksd.sh
{% endif %}
workers.sh
