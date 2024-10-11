FROM python:3.8-slim

# Set non-interactive mode for apt-get to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-opencv \
    libopencv-dev \
    libgtk2.0-dev \
    libcanberra-gtk-module \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# devuser adında bir kullanıcı oluştur ve ona bir home dizini ver
RUN useradd -m -d /home/devuser devuser

# /app dizinine devuser için gerekli izinleri ver
RUN chown -R devuser:devuser /app

# devuser kullanıcısına geç
USER devuser
WORKDIR /app

# Gerekli dosyaları devuser altında kopyala
COPY --chown=devuser:devuser requirements.txt .
COPY --chown=devuser:devuser README.md .
COPY --chown=devuser:devuser logger.py .
COPY --chown=devuser:devuser config.yaml .
COPY --chown=devuser:devuser calibrateCamera.py .
COPY --chown=devuser:devuser /logs/calibration.log .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./calibrateCamera.py"]