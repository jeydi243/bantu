# Use an official Python runtime as a parent image
FROM python:3.13-alpine3.22

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy the dependency files
COPY pyproject.toml requirements.txt uv.lock* ./

# Install dependencies
RUN uv pip sync --no-cache requirements.txt --system

# Copy the rest of the application code
COPY db/ ./db/
COPY handlers/ ./handlers/
COPY main.py .

# Command to run the application
CMD ["python", "main.py"]
