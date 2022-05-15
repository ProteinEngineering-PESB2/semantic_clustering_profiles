FROM python:3.9-buster

WORKDIR /app
COPY ./requisites ./requisites
RUN ["pip3", "install", "-r", "./requisites/requirements.txt"]
ENV PATH="/app/requisites/blast/ncbi-blast-2.13.0+/bin:${PATH}"
ENV BLASTDB="/app/requisites/blastdb"

CMD ["python3", "./src/main.py"]