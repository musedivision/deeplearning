#FROM jupyter/minimal-notebook
#
#USER root
#
## install git and clean out after install
#RUN apt-get -yq dist-upgrade \
# && apt-get install -yq --no-install-recommends \
#    git \
#	 wget \
# && apt-get clean \
# && rm -rf /var/lib/apt/lists/*
#
### download fast ai
#RUN git clone https://github.com/fastai/fastai.git
#
#RUN cd fastai
#RUN conda env update
#
## install dependencies
#RUN source activate fastai
#
#
#ADD ./src /home/jovyan/.
#
#EXPOSE 8888
#
#CMD ["jupyter", "notebook"]





# install python
#RUN apt-get update
#RUN apt-get install -yq --no-install-recommends \
#  software-properties-common vim \
# && add-apt-repository ppa:jonathonf/python-3.6
#
#RUN apt-get update
#
#RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
#RUN apt-get install -y git
#
#RUN apt-get clean \
# && rm -rf /var/lib/apt/lists/*
#
## update pip
#RUN python3.6 -m pip install pip --upgrade
#RUN python3.6 -m pip install wheel




FROM nvidia/cuda

# update the apt -get
RUN apt-get -yq dist-upgrade \
 && apt-get update \
 && apt-get install -yq --no-install-recommends \
    git \
	 wget \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

#USER root

#RUN set -e \
# && set -o xtrace \
# && DEBIAN_FRONTEND=noninteractive
#
#RUN sudo rm /etc/apt/apt.conf.d/*.*
#RUN sudo apt update
#RUN sudo apt install unzip -y
#RUN sudo apt -y upgrade --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"
#RUN sudo apt -y autoremove
#
#RUN sudo apt -y install --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" qtdeclarative5-dev qml-module-qtquick-controls
#RUN sudo add-apt-repository ppa:graphics-drivers/ppa -y
#RUN sudo apt update
#RUN mkdir downloads
#RUN cd ~/downloads/
#wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
#sudo dpkg -i cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
#sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
#sudo apt update
#sudo apt install cuda -y

#RUN wget https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
#RUN bash Anaconda3-5.0.1-Linux-x86_64.sh -b

#cd
#git clone https://github.com/fastai/fastai.git
#cd fastai/
#echo 'export PATH=~/anaconda3/bin:$PATH' >> ~/.bashrc
#export PATH=~/anaconda3/bin:$PATH
#source ~/.bashrc
#conda env update
#echo 'source activate fastai' >> ~/.bashrc
#source activate fastai
#source ~/.bashrc



FROM nvidia/cuda as base

# update the apt -get
RUN apt-get -yq dist-upgrade \
 && apt-get update \
 && apt-get install -yq --no-install-recommends \
    git \
	wget \
	software-properties-common \
	bzip2 \
	ca-certificates \
	sudo \
	locales \
	fonts-liberation \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


FROM base as depedencies

ENV SHELL=/bin/bash

RUN wget --no-check-certificate https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
RUN /bin/bash -c bash Anaconda3-5.0.1-Linux-x86_64.sh -b

ENV PATH=~/anaconda3/bin:$PATH

FROM depedencies as fastai

RUN cd
RUN git clone https://github.com/fastai/fastai.git
RUN cd fastai/

# activate env and start the notebook
FROM fastai

RUN /bin/bash -c conda env update	
RUN /bin/bash -c source activate fastai

RUN /bin/bash -c pip install ipywidgets
RUN /bin/bash -c jupyter nbextension enable --py widgetsnbextension --sys-prefix

RUN /bin/bash -c jupyter notebook