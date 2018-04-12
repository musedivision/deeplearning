###
### copied base from paperspace/fastai-docker but didnt want all their layers
###
FROM nvidia/cuda:9.0-base

LABEL com.nvidia.volumes.needed="nvidia_driver"

RUN echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list

RUN apt-get update && apt-get install -y --allow-downgrades --no-install-recommends \
         build-essential \
         cmake \
         git \
         curl \
         vim \
         ca-certificates \
         libnccl2=2.0.5-3+cuda9.0 \
         libnccl-dev=2.0.5-3+cuda9.0 \
         python-qt4 \
         libjpeg-dev \
	 zip \
	 unzip \
         libpng-dev &&\
     rm -rf /var/lib/apt/lists/*