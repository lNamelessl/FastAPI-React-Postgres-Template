# Use Python 3.12
FROM python:3.12-slim

# Install system dependencies (curl for uv, build dependencies for any C-extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin:${PATH}"

# Copy only dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# Sync dependencies
RUN uv sync --frozen

# Copy the rest of the application
COPY . .

# Railway uses the PORT env var. 
# We remove the commas and brackets to ensure the shell properly expands ${PORT}
EXPOSE 8000

# Using uv run ensures we are in side the virtual environment uv created
CMD uv run uvicorn ./app.main:app --host 0.0.0.0 --port ${PORT:-8000}