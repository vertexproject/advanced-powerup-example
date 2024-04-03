#!/bin/bash

set -x
set -e

if [ -d /build/package ]; then
    cd /build/package
    python -m pip install --break-system-packages vtx-common
    SYN_LOG_LEVEL=DEBUG python -m vtx_common.tools.buildpkg synmods/*/assets/*.yaml
    python -m pip install --break-system-packages /build/package
fi

rm -rf /build
