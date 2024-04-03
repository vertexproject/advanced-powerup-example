# Start with a release line synapse image
FROM vertexproject/synapse:v2.x.x

COPY pyproject.toml /build/package/pyproject.toml
COPY synmods /build/package/synmods
COPY docker/scripts/bootstrap.sh /build/bootstrap.sh
COPY docker/scripts/entrypoint.sh /vertex/synapse/entrypoint.sh

EXPOSE 4443
EXPOSE 27492

# run our image building bootstrap
RUN ["/build/bootstrap.sh"]

# Set the entrypoint for the container to the server
ENTRYPOINT ["tini", "--", "/vertex/synapse/entrypoint.sh"]

HEALTHCHECK --start-period=10s --retries=1 --timeout=10s --interval=30s CMD python -m synapse.tools.healthcheck -c cell:///vertex/storage/
