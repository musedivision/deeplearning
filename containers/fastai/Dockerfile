###
### copied base from paperspace/fastai-docker but didnt want all their layers
###

FROM deep_cudaconda


WORKDIR /fastai

RUN git clone https://github.com/fastai/fastai.git .
RUN ls && /opt/conda/bin/conda env create
RUN /opt/conda/bin/conda clean -ya

ENV PATH /opt/conda/envs/fastai/bin:$PATH
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV USER fastai


CMD source activate fastai
CMD source ~/.bashrc

WORKDIR /data

RUN ln -s /data/ /fastai/courses/dl1/

#RUN curl http://files.fast.ai/data/dogscats.zip --output dogscats.zip
#RUN unzip -d . dogscats.zip
#RUN rm dogscats.zip


#RUN ls -la /notebooks/courses/dl1/data/
WORKDIR /notebooks

RUN chmod -R a+w /notebooks

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]