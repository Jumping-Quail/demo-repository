FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install specific versions of pip and mediapipe first
RUN pip install --no-cache-dir pip==23.3.1
RUN pip install --no-cache-dir mediapipe==0.8.7.3

# Try to install openhands with --no-dependencies
RUN pip install --no-cache-dir --no-dependencies openhands

# Install required dependencies manually
RUN pip install --no-cache-dir \
    numpy==1.19.5 \
    albumentations==0.5.2 \
    tqdm==4.59.0 \
    omegaconf==2.1.0 \
    pytorch-lightning==1.4.8 \
    pytorchvideo==0.1.1 \
    hydra-core==1.1.0 \
    torch==1.9.0

# Set the entrypoint
ENTRYPOINT ["python", "-m", "openhands.cli.main"]
