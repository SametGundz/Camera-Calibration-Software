FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    python3-opencv \
    libopencv-dev \
    libgtk2.0-dev \
    libcanberra-gtk-module \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
COPY logger.py .
COPY calibrateCamera.py .
COPY config.yaml .
COPY data ./data

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./calibrateCamera.py"]
