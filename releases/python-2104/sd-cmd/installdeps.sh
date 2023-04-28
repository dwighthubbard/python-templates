#!/bin/bash
# Copyright 2023, Yahoo Inc.
# Licensed under the terms of the Apache 2.0 license.  See the LICENSE file in the project root for terms

# Bootstrap python
if [ ! -e "$BASE_PYTHON" ]; then
    if [ "PYTHON_BOOTSTRAP_SKIP_SCREWDRIVERCD" = "" ]; then
        PYTHON_BOOTSTRAP_SKIP_SCREWDRIVERCD="True"
    fi
    sd-cmd exec python-2304/python_bootstrap@latest
    . /tmp/python_bootstrap.env
fi

export LOGDIR="$SD_ARTIFACTS_DIR/logs/sd-cmd"
export LOGFILE="$LOGDIR/installdeps.log"
if [ ! -e "LOGDIR" ]; then
    mkdir -p "$LOGDIR"
fi

SUDO_CMD="sudo -E "
USER_ID=`id -u`
if [ "${USER_ID}" = "0" ]; then
    SUDO_CMD=""
fi

if [ "$TERM" = "" ]; then
    export TERM="ansi"
fi

set -o pipefail
sd-cmd exec python-2104/pypirun@stable screwdrivercd screwdrivercd_install_deps | tee -a $LOGFILE
