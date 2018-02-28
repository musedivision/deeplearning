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

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

ENV PATH /opt/conda/bin:$PATH



FROM depedencies as fastai

# activate env and start the notebook

#RUN cd ~/fastai && \
#	/bin/bash -c 'conda env update'


FROM fastai

WORKDIR /home

ADD ./src /home/.
RUN echo "c.NotebookApp.password = '${PASSWORD}'" >> /home/.jupyter/jupyter_notebook_config.py

#ADD  ../../.fastai/environment.yml /home/environment.yml
RUN /bin/bash -c 'conda env update'



RUN /bin/bash -c 'source activate fastai \
	&& pip install ipywidgets \
	&& jupyter nbextension enable --py widgetsnbextension --sys-prefix'

EXPOSE 8888

CMD ["/bin/bash -c","jupyter", "notebook"]