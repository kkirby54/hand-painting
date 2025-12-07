FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
# We copy pyproject.toml. uv.lock might not exist if we are in a workspace, 
# so we attempt to copy it but don't fail if missing (by copying current dir content later or using a trick)
# A common trick is to copy both, but if uv.lock is missing, it fails.
# Instead, we'll just copy pyproject.toml first.
COPY pyproject.toml .
# If uv.lock exists in the context, we'd want it. 
# Since we can't easily conditionally copy, we will rely on uv sync to generate it if missing.
# However, for reproducibility, we usually want the lockfile.
# Given the workspace constraint, we'll skip explicit uv.lock copy here and rely on the next COPY .
# But we want to cache dependencies.
# We can try to copy uv.lock if it exists.
# For now, let's just copy pyproject.toml and run sync. 
# If uv.lock is in the directory, it will be copied in the next step, but that's too late for the cache layer.
# We will assume for now that we might not have uv.lock and just run uv sync.

# Install dependencies (this layer will be cached if pyproject.toml doesn't change)
# We run sync to install deps. without --frozen so it generates lockfile if missing.
RUN uv sync || true

COPY . .

# Run sync again to ensure everything is installed and environment is ready (and to pick up code changes if any editable installs)
RUN uv sync

# Create data directory
RUN mkdir -p /app/data

# Run the application
CMD ["uv", "run", "main.py"]
