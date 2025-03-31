FROM continuumio/miniconda3:latest
WORKDIR /app
RUN conda install -y numpy pandas matplotlib scipy \
    && pip install --no-cache-dir ngsolve \
    && conda clean -afy
COPY . /app

RUN chmod +x run.sh

CMD ["./dockerRun.sh"]