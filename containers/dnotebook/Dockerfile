###
### copied base from paperspace/fastai-docker but didnt want all their layers
###
FROM cfastai

CMD source activate fastai
CMD source ~/.bashrc
CMD jupyter serverextension enable --py jupyterlab --sys-prefix

# WORKDIR /data 

# RUN ln -s /data/ /fastai/courses/dl1/

#RUN curl http://files.fast.ai/data/dogscats.zip --output dogscats.zip
#RUN unzip -d . dogscats.zip
#RUN rm dogscats.zip


#RUN ls -la /notebooks/courses/dl1/data/
WORKDIR /notebooks

RUN chmod -R a+w /notebooks
# RUN jupyter serverextension enable --py jupyterlab --sys-prefix
# RUN cat ~/.jupyter/nbconfig/notebook.json

# seperate new dependency downloads so they can be cached
# TODO

# should upload made images to docker hub so can downlaod them
# will it build local if there is no uploaded image?


RUN /bin/bash -c 'pip install ipywidgets  \
    jupyterthemes \
    && python -m spacy download en \
    && jupyter nbextension enable --py widgetsnbextension  --sys-prefix \
    && jupyter nbextension enable collapsible_headings/main \
    '
    #  && pip install jupyterlab \
    # && jupyter nbextension enable --py jupyterlab  --sys-prefix'


CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]