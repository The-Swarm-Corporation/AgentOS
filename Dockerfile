# syntax=docker/dockerfile:1.4
# Build stage
FROM python:3.13-slim-bullseye AS builder

# Set build arguments and environment variables
ENV WORKSPACE_DIR="agent_workspace" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install security updates and build dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /${WORKSPACE_DIR}

# Copy only requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies with uvicorn and its extras
RUN pip install --no-cache-dir -r requirements.txt uvicorn[standard] gunicorn

# Runtime stage
FROM python:3.13-slim-bullseye AS runtime

# Set runtime arguments
ARG AGENT_USER=agent
ARG AGENT_GROUP=agent
ARG AGENT_UID=10001
ARG AGENT_GID=10001

# Set environment variables
ENV WORKSPACE_DIR="agent_workspace" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/${WORKSPACE_DIR}:${PATH}" \
    AGENT_API_PORT=8000 \
    WORKERS=4 \
    TIMEOUT=120 \
    GRACEFUL_TIMEOUT=30 \
    KEEP_ALIVE=5 \
    MAX_REQUESTS=10000 \
    MAX_REQUESTS_JITTER=1000 \
    LOG_LEVEL=warning

# Install security updates and runtime dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user and group
RUN groupadd -g ${AGENT_GID} ${AGENT_GROUP} && \
    useradd -u ${AGENT_UID} -g ${AGENT_GROUP} -s /sbin/nologin -M ${AGENT_USER}

# Create and set permissions for workspace
WORKDIR /${WORKSPACE_DIR}
RUN mkdir -p /${WORKSPACE_DIR}/data /${WORKSPACE_DIR}/logs

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Copy application code
COPY --chown=${AGENT_USER}:${AGENT_GROUP} agent_api agent_api/

# Create uvicorn config
RUN echo '{\n\
    "workers": ${WORKERS},\n\
    "timeout": ${TIMEOUT},\n\
    "graceful_timeout": ${GRACEFUL_TIMEOUT},\n\
    "keepalive": ${KEEP_ALIVE},\n\
    "max_requests": ${MAX_REQUESTS},\n\
    "max_requests_jitter": ${MAX_REQUESTS_JITTER},\n\
    "log_level": "${LOG_LEVEL}",\n\
    "access_log": "/agent_workspace/logs/access.log",\n\
    "error_log": "/agent_workspace/logs/error.log",\n\
    "proxy_headers": true,\n\
    "forwarded_allow_ips": "*"\n\
}' > /${WORKSPACE_DIR}/uvicorn.json

# Set proper permissions
RUN chown -R ${AGENT_USER}:${AGENT_GROUP} /${WORKSPACE_DIR} && \
    chmod -R 550 /${WORKSPACE_DIR} && \
    chmod -R 770 /${WORKSPACE_DIR}/data /${WORKSPACE_DIR}/logs

# Switch to non-root user
USER ${AGENT_USER}:${AGENT_GROUP}

# Expose port
EXPOSE ${AGENT_API_PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${AGENT_API_PORT}/health || exit 1

# Use tini as init system
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start uvicorn with production settings
CMD ["uvicorn", \
     "agent_api.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4", \
     "--proxy-headers", \
     "--forwarded-allow-ips", "*", \
     "--access-log", \
     "--log-level", "warning", \
     "--timeout-keep-alive", "5", \
     "--limit-max-requests", "10000"]