FROM python:3.8-slim

# Set non-interactive mode for apt-get to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Switch to root to install system packages
USER root

RUN apt-get update && apt-get install -y \
    python3-opencv \
    libopencv-dev \
    libgtk2.0-dev \
    libcanberra-gtk-module \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to the non-root user
USER devuser
WORKDIR /home/devuser

COPY --chown=devuser:devuser requirements.txt ./
COPY logger.py .
COPY calibrateCamera.py .
COPY config.yaml .
COPY data /app/data

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./calibrateCamera.py"]
