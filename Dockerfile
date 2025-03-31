FROM continuumio/miniconda3
WORKDIR /app
COPY . /app
RUN chmod +x run.sh
SHELL ["/bin/bash", "-c"]
CMD ["./run.sh"]