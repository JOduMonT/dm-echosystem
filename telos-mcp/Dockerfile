FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
curl \
git \
&& rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy TELOS MCP server code
COPY telos_mcp_server.py /app/

# Create context directory
RUN mkdir -p /app/context

# Create non-root user
RUN useradd -m -u 1000 telosuser && \
chown -R telosuser:telosuser /app
USER telosuser

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
CMD curl -f http://localhost:3001/health || exit 1

# Default command
CMD ["python", "telos_mcp_server.py"]