#!/bin/bash

# Embed the current git commit into version.py
# This could be modified into its own CI step.
python -m vtx_common.tools.replace_commit ./synmods/*/version.py

IMAGENAME=examplepowerup

TAG=${1:-}

if [ ! $TAG ]
then
    echo "Tag not provided, defaulting tag to no tag"
    TAG=''
else
    TAG=":$TAG"
fi

docker build --progress=plain -f docker/release/Dockerfile -t $IMAGENAME$TAG ./
