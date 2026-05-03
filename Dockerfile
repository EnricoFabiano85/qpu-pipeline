FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV OMP_PROC_BIND=true
ENV OMP_PLACES=cores

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libomp-dev \
    clangd \
    python3-dev \
    less \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    pybind11 \
    scikit-build-core

WORKDIR /app

CMD ["/bin/bash"]
