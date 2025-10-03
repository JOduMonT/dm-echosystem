FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install fabric-mcp
RUN pip install fabric-mcp

# Create non-root user
RUN useradd -m -u 1000 fabricuser
USER fabricuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Default command
CMD ["fabric-mcp", "--http-streamable", "--host", "0.0.0.0", "--port", "3000", "--mcp-path", "/mcp"]