# NOTES:
# The container for this component must use python 3.8 (or 3.9?) as the
# version of the package onnxruntime that is in the requirements.txt
# of the Bytetrack repository is set to a version that is compatible
# only with that python version.
FROM nvidia/cuda:11.7.0-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

# Install system tools
RUN apt-get update && apt-get -y install \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt -y install \
    software-properties-common

RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt update && apt -y install \
    build-essential \
    python3.8 python3.8-dev python3-pip python3.8-distutils python3.8-venv \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# Install poetry
RUN python -m pip install poetry==1.1.8

# Copy over python dependency specifications
COPY pyproject.toml poetry.lock /

# Install python dependencies
RUN poetry config virtualenvs.create false && \
    poetry config experimental.new-installer false && \
    python -m pip install numpy==1.23.5 cython && \
    poetry export --output requirements-poetry.txt && \
    python -m pip install -r requirements-poetry.txt && \
    # poetry install --no-dev -v && \
    python -m pip install lap==0.4.0 cython_bbox==0.1.3 git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI

# Install ByteTrack
RUN git clone https://github.com/ifzhang/ByteTrack.git
COPY tools/demo_track.py /ByteTrack/tools/demo_track.py
COPY requirements.txt /ByteTrack/requirements.txt
WORKDIR /ByteTrack

RUN python -m pip install -r requirements.txt && python setup.py develop

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Copy sample video
COPY friends-Scene-008.mp4 .
