###
### copied base from paperspace/fastai-docker but didnt want all their layers
###
FROM bconda

WORKDIR /fastai

RUN git clone https://github.com/fastai/fastai.git .
RUN ls && /opt/conda/bin/conda env create
RUN /opt/conda/bin/conda clean -ya

ENV PATH /opt/conda/envs/fastai/bin:$PATH
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV USER fastai