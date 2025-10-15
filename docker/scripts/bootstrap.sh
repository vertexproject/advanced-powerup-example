#!/bin/bash

set -x
set -e

if [ -d /build/package ]; then
    cd /build/package
    SYN_LOG_LEVEL=DEBUG python -m synapse.tools.storm.pkg.doc synmods/*/assets/*.yaml
    python -m pip install --break-system-packages /build/package
fi

rm -rf /build
