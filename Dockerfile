FROM condaforge/miniforge3
LABEL maintainer='Príscila Lima <pal3 at cin.ufpe.br>'
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt