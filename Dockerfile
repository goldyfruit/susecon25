FROM registry.suse.com/bci/python:3.12.7

ARG ALPHA=false
ARG BUILD_DATE=unknown
ARG VERSION=unknown

LABEL org.opencontainers.image.authors="Gaëtan Trellu"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.description="Just a basic SUSE BCI container image for SUSECON 2025"
LABEL org.opencontainers.image.documentation="https://github.com/goldyfruit/suma-images"
LABEL org.opencontainers.image.source="https://github.com/goldyfruit/suma-images"
LABEL org.opencontainers.image.vendor="SUSE"
LABEL org.opencontainers.image.version="${VERSION}"

WORKDIR /app

RUN zypper --non-interactive in libopenssl1_1 \
    && if [ "${ALPHA}" == "true" ]; then \
    pip install --no-cache-dir fastapi[standard] pydantic --pre; \
    else \
    pip install --no-cache-dir fastapi[standard] pydantic; \
    fi \
    && zypper clean all \
    && mkdir -p /app

CMD ["fastapi", "run", "main.py", "--port", "8000"]
