# DataScope Enhanced Standalone - Docker Configuration
# Multi-stage build: React frontend + Python backend

# Stage 0: Build React frontend
FROM node:22-alpine AS frontend-builder
WORKDIR /frontend
COPY cybersecurity-threat-dashboard/package.json cybersecurity-threat-dashboard/pnpm-lock.yaml ./
RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm install --frozen-lockfile
COPY cybersecurity-threat-dashboard/ .
RUN pnpm build

# Stage 1: Build Python dependencies
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VERSION=1.0.0
ARG VCS_REF

# Add metadata
LABEL maintainer="DataScope Team <team@datascope-enhanced.com>" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="DataScope Enhanced" \
      org.label-schema.description="Multi-Domain Intelligence Platform" \
      org.label-schema.url="https://datascope-enhanced.com" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/your-org/datascope-enhanced" \
      org.label-schema.vendor="DataScope Team" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r /tmp/requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DEBIAN_FRONTEND=noninteractive

# Create non-root user
RUN groupadd --gid 1000 datascope && \
    useradd --uid 1000 --gid datascope --shell /bin/bash --create-home datascope

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Chrome dependencies
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    # Additional utilities
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/cache /app/reports /app/data /app/logs && \
    chown -R datascope:datascope /app

# Copy application code
COPY --chown=datascope:datascope . /app/

# Copy configuration files
COPY --chown=datascope:datascope .env.example /app/.env

# Install ChromeDriver
RUN python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()" || \
    echo "ChromeDriver installation failed, will try at runtime"

# Switch to non-root user
USER datascope

# Expose ports
EXPOSE 5000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/api/v1/status || exit 1

# Copy built frontend into static directory
COPY --from=frontend-builder /frontend/dist /app/static

# Default command — serve Flask with frontend
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "main:app"]

# Development stage
FROM production as development

# Switch back to root for development tools
USER root

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
RUN pip install pytest pytest-cov black flake8 ipython jupyter

# Switch back to datascope user
USER datascope

# Override command for development
CMD ["python", "enhanced_main.py", "--debug"]

